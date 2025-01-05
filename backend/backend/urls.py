"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import signup, application, tutor_profile_status, tutor_approve_status, save_tutor_profile, get_tutor_profile, get_student_user_data, search_tutors, tutor_details, signin, send_tutor_request_email, bookmark_tutor, is_tutor_bookmarked, unbookmark_tutor, get_bookmarked_tutors

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', signup, name='signup'),
    path('api/application', application, name='application'),
    path('api/tutor-approve-status/', tutor_approve_status, name='tutor_approve_status'),
    path('api/tutor-profile-status/', tutor_profile_status, name='tutor_profile_status'),
    path('api/tutor-profile/', save_tutor_profile, name='save_tutor_profile'),
    path('api/tutor-profile-read/', get_tutor_profile, name='get_tutor_profile'),
    path('api/student-user/', get_student_user_data, name='get_student_user_data'),
    path('api/search-tutors/', search_tutors, name='search_tutors'),
    path('api/tutor-details/<int:tutor_id>/', tutor_details, name='tutor-details'),
    path('api/signin/', signin, name='signin'),
    path('api/tutor-request-email/', send_tutor_request_email, name='send-tutor-request-email'),
    path('api/bookmark-tutor/', bookmark_tutor, name='bookmark_tutor'),
    path('api/is-tutor-bookmarked/', is_tutor_bookmarked, name='is_tutor_bookmarked'),
    path('api/unbookmark-tutor/', unbookmark_tutor, name='unbookmark_tutor'),
    path('api/bookmarked-tutors/', get_bookmarked_tutors, name='get_bookmarked_tutors'),


]
