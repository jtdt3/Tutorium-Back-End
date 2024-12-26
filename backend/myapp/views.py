from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from .models import StudentUser
import json

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