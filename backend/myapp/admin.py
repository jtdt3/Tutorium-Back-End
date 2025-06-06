from django.contrib import admin
from .models import StudentUser, TutorApplication, TutorProfile, BookmarkedTutors, TutorReview, TutorAnalyticsView, RequestFormInfo

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
    list_display = (
        'user',
        'bio',
        'gender',
        'hourly_rate',
        'subjects',
        'location',
        'language',
        'profile_complete',
        'average_rating',
    )
    fields = (
        'user',
        'bio',
        'gender',
        'hourly_rate',
        'subjects',
        'location',
        'language',
        'profile_picture',
        'profile_complete',
        'average_rating',
    )


# Register the BookmarkedTutors model
@admin.register(BookmarkedTutors)
class BookmarkedTutorsAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'tutor_id')  # Display these fields in the admin list view
    search_fields = ('student_id', 'tutor_id')  # Enable search by student_id and tutor_id
    list_filter = ('student_id',)  # Add filter for student_id


@admin.register(TutorReview)
class TutorReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'tutor_id', 'rating', 'comment', 'created_at')
    search_fields = ('student_id', 'tutor_id', 'rating')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)
    
@admin.register(TutorAnalyticsView)
class TutorAnalyticsViewAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'viewer', 'timestamp', 'view_count')
    search_fields = ('tutor__user__first_name', 'tutor__user__last_name', 'viewer__first_name', 'viewer__last_name')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

@admin.register(RequestFormInfo)
class RequestFormInfoAdmin(admin.ModelAdmin):
    list_display = ('requesterFirstName', 'requesterLastName', 'requesterEmail', 'requesterDescription', 'tutorID', 'created_at')
    search_fields = ('requesterFirstName', 'requesterLastName', 'requesterEmail', 'tutorID')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
