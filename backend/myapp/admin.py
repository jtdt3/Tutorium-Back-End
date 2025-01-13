from django.contrib import admin
from .models import StudentUser, TutorApplication, TutorProfile, BookmarkedTutors, TutorReview

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

@admin.register(TutorReview)
class TutorReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'tutor', 'rating', 'comment', 'created_at')
    search_fields = ('student__first_name', 'student__last_name', 'tutor__user__first_name', 'tutor__user__last_name', 'comment')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        """
        Customize the queryset to include related student and tutor data for better performance in the admin.
        """
        return super().get_queryset(request).select_related('student', 'tutor', 'tutor__user')