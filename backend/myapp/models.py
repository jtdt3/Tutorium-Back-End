from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class TwoFactorCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
 
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
 
    ###
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.approve_status}"
 
    def save(self, *args, **kwargs):
        # Check if the approve_status is updated to 'approved'
        if self.approve_status == 'approved':
            # Create or get a TutorProfile for the user
            TutorProfile.objects.get_or_create(user=self.user)
 
            # Update the user's user_type to 'tutor' if not already
            if self.user.user_type != 'tutor':
                self.user.user_type = 'tutor'
                self.user.save()
 
        super().save(*args, **kwargs)
 
 
# class TutorProfile(models.Model):
#     user = models.OneToOneField('StudentUser', on_delete=models.CASCADE)
#     bio = models.TextField(blank=True)
#     profile_picture = models.URLField(max_length=500, blank=True, null=True)  # Changed to URLField
#     subjects = models.CharField(max_length=255, blank=True)
#     location = models.CharField(max_length=255, blank=True)
#     language = models.CharField(max_length=255, blank=True)
#     profile_complete = models.CharField(
#         max_length=3,
#         choices=[('yes', 'Yes'), ('no', 'No')],
#         default='no'
#     )
 
#     def __str__(self):
#         return f"{self.user.first_name} {self.user.last_name}'s Profile"
 
class TutorProfile(models.Model):
    user = models.OneToOneField('StudentUser', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)  # Changed to URLField
    subjects = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=255, blank=True)
    profile_complete = models.CharField(
        max_length=3,
        choices=[('yes', 'Yes'), ('no', 'No')],
        default='no'
    )
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  # Add this field
 
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Profile"
 
 
class BookmarkedTutors(models.Model):
    student_id = models.IntegerField()  # Or use models.ForeignKey if linked to a User model
    tutor_id = models.IntegerField()
 
    def __str__(self):
        return f"Student {self.student_id} bookmarked Tutor {self.tutor_id}"
 
class TutorReview(models.Model):
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE)
    rating = models.IntegerField()  # Rating as an integer (e.g., 1-5)
    comment = models.TextField()  # Review text
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Review by {self.student.first_name} {self.student.last_name} for {self.tutor.user.first_name} {self.tutor.user.last_name}"
 