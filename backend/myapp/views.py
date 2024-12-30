from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from .models import StudentUser, TutorApplication, TutorProfile
from django.conf import settings
import json
import boto3
import logging
import re


logger = logging.getLogger(__name__)


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Fallback to default value if userType is not provided
            user_type = data.get('userType', '')  # Default to ''

            # Create a new user
            student = StudentUser.objects.create(
                first_name=data['firstName'],
                last_name=data['lastName'],
                email=data['email'],
                password=data['password'],  # Consider hashing this in production
                user_type=user_type
            )

            return JsonResponse({'message': 'User created successfully!', 'user_id': student.id}, status=201)

        except Exception as e:
            return JsonResponse({'message': 'Failed to create user', 'error': str(e)}, status=400)

    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def get_student_user_data(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'User ID is required'}, status=400)

        try:
            student_user = StudentUser.objects.get(id=user_id)
            return JsonResponse({
                'first_name': student_user.first_name,
                'last_name': student_user.last_name,
                'email': student_user.email,
            }, status=200)
        except StudentUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def application(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            email = data.get('email', '')
            question_one = data.get('questionOne', '')
            question_two = data.get('questionTwo', '')

            # Validate required fields
            if not email or not question_one or not question_two:
                return JsonResponse({'error': 'All fields are required.'}, status=400)
            

                        # Get the StudentUser instance
            try:
                student = StudentUser.objects.get(email=email)
            except StudentUser.DoesNotExist:
                return JsonResponse({'error': 'User not found.'}, status=404)

            # Create or update the application with just the foreign key and status
            TutorApplication.objects.update_or_create(
                user=student,
                defaults={
                    'approve_status': 'pending'
                }
            )

            # Email 1: Send to your own email with the form data
            subject_to_self = "New Tutor Application Received"
            message_to_self = (
                f"Tutor Application Submitted:\n\n"
                f"Email: {email}\n\n"
                f"Why do you think you can be a tutor? List your school and experience:\n"
                f"{question_one}\n\n"
                f"List Your Qualifications. Have you ever worked with a different tutoring app?:\n"
                f"{question_two}\n\n"
            )

            sender_email = "help.tutorium@gmail.com"  # Your Gmail address
            your_email = "help.tutorium@gmail.com"  # Your email to receive the form data

            send_mail(subject_to_self, message_to_self, sender_email, [your_email])

            # Email 2: Send to the applicant (recipient email) with a confirmation
            subject_to_recipient = "Your Tutor Application Submission"
            message_to_recipient = (
                f"Dear Applicant,\n\n"
                f"Thank you for submitting your application to become a tutor. Here is a summary of your submission:\n\n"
                f"Why do you think you can be a tutor? List your school and experience:\n"
                f"{question_one}\n\n"
                f"List Your Qualifications. Have you ever worked with a different tutoring app?:\n"
                f"{question_two}\n\n"
                f"We will review your application and get back to you shortly.\n\n"
                f"Best regards,\nThe Tutorium Team"
            )

            recipient_email = email  # Use the submitted email as the recipient

            send_mail(subject_to_recipient, message_to_recipient, sender_email, [recipient_email])

            # Return success response
            return JsonResponse({'message': 'Application received successfully!'}, status=200)

        except Exception as e:
            # Handle any errors
            return JsonResponse({'error': str(e)}, status=500)

    # If not a POST request, return a 405 Method Not Allowed
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def tutor_approve_status(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'User ID is required'}, status=400)

        try:
            tutor_application = TutorApplication.objects.get(user_id=user_id)
            return JsonResponse({'approve_status': tutor_application.approve_status}, status=200)
        except TutorApplication.DoesNotExist:
            return JsonResponse({'approve_status': None}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt  # Remove csrf_exempt in production and secure the endpoint
def tutor_profile_status(request):
    if request.method == 'GET':
        try:
            # Retrieve the user_id from query parameters
            user_id = request.GET.get('user_id')

            if not user_id:
                return JsonResponse({'error': 'User ID is required'}, status=400)

            # Check if a TutorProfile exists for the given user_id
            try:
                tutor_profile = TutorProfile.objects.get(user_id=user_id)
                return JsonResponse({'profile_complete': tutor_profile.profile_complete}, status=200)
            except TutorProfile.DoesNotExist:
                return JsonResponse({'profile_complete': None}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def save_tutor_profile(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            bio = request.POST.get('bio')
            subjects = request.POST.get('subjects')  # Comma-separated string
            location = request.POST.get('location')
            language = request.POST.get('language')  # Comma-separated string
            profile_picture = request.FILES.get('profilePic')
            existing_profile_picture = request.POST.get('existingProfilePic')

            if not user_id:
                return JsonResponse({'error': 'User ID is required'}, status=400)

            try:
                user = StudentUser.objects.get(id=user_id)
            except StudentUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            # Determine the profile picture URL
            profile_pic_url = None
            if profile_picture:
                # Upload new profile picture to S3
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                )
                bucket_name = 'your-s3-bucket-name'
                file_name = f"tutor-profile-pics/{profile_picture.name}"
                s3.upload_fileobj(
                    profile_picture,
                    bucket_name,
                    file_name,
                )
                profile_pic_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
            elif existing_profile_picture:
                # Use the existing profile picture URL
                profile_pic_url = existing_profile_picture

            # Update or create the tutor profile
            profile, created = TutorProfile.objects.update_or_create(
                user=user,
                defaults={
                    'bio': bio,
                    'subjects': subjects,
                    'location': location,
                    'language': language,
                    'profile_picture': profile_pic_url,
                    'profile_complete': 'yes',
                }
            )

            return JsonResponse({'message': 'Profile saved successfully!'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def get_tutor_profile(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')

            if not user_id:
                return JsonResponse({'error': 'User ID is required'}, status=400)

            try:
                tutor_profile = TutorProfile.objects.get(user_id=user_id)
                return JsonResponse({
                    'bio': tutor_profile.bio,
                    'profile_picture': tutor_profile.profile_picture,
                    'subjects': tutor_profile.subjects,
                    'location': tutor_profile.location,
                    'language': tutor_profile.language,
                    'profile_complete': tutor_profile.profile_complete
                }, status=200)
            except TutorProfile.DoesNotExist:
                return JsonResponse({'error': 'Profile not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
