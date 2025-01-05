from django.contrib import admin
from .models import StudentUser, TutorApplication, TutorProfile, BookmarkedTutors

@admin.register(StudentUser)
class StudentUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'user_type')

@admin.register(TutorApplication)
class TutorApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'approve_status')
    list_filter = ('approve_status',)
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        for application in queryset:
            application.approve_status = 'approved'
            application.save()
    approve_selected.short_description = "Mark selected applications as approved"

@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_complete')


# Register the BookmarkedTutors model
@admin.register(BookmarkedTutors)
class BookmarkedTutorsAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'tutor_id')  # Display these fields in the admin list view
    search_fields = ('student_id', 'tutor_id')  # Enable search by student_id and tutor_id
    list_filter = ('student_id',)  # Add filter for student_id