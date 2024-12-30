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

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Profile"

