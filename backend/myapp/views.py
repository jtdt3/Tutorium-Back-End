'''from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        # Parse and print the received data
        data = json.loads(request.body)
        print("Received Data:", data)

        # Respond back with success message
        return JsonResponse({'message': 'Data received successfully!'}, status=200)
    
    return JsonResponse({'message': 'Invalid request method.'}, status=400)'''

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import StudentUser
import json

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create a new StudentUser instance
            student = StudentUser.objects.create(
                first_name=data['firstName'],
                last_name=data['lastName'],
                email=data['email'],
                password=data['password']  # Consider hashing this in a real app
            )

            return JsonResponse({'message': 'User created successfully!', 'user_id': student.id}, status=201)

        except Exception as e:
            return JsonResponse({'message': 'Failed to create user', 'error': str(e)}, status=400)
    
    return JsonResponse({'message': 'Invalid request method.'}, status=400)
