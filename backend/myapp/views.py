from django.http import JsonResponse
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
    
    return JsonResponse({'message': 'Invalid request method.'}, status=400)
