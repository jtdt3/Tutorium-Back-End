from django.db import models

class StudentUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_type})"

class TutorApplication(models.Model):  # Changed name to be more specific
    APPROVE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    
    user = models.OneToOneField(StudentUser, on_delete=models.CASCADE)
    approve_status = models.CharField(max_length=20, choices=APPROVE_STATUS_CHOICES, default='pending')