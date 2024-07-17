from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_file, name='submit_file'),
    path('list/', views.submission_list, name='submission_list'),
    path('register/', views.student_register, name='student_register'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('verify-submission/', views.verify_submissions, name='verify_submission'),
    path('set-certificates-available/', views.set_certificates_available, name='set_certificates_available'),
    path('certificates-available/', views.set_certificates_available, name='certificates_available'),
    path('download-student-details/', views.download_student_details, name='download_student_details'),
    path('download-verified-submissions/', views.download_verified_submissions, name='download_verified_submissions'),
    path('download-available-certificates/', views.download_available_certificates, name='download_available_certificates'),
    path('verify-submissions/', views.verify_submissions_list, name='verify_submissions'),
    path('verify-submission/<int:submission_id>/', views.verify_submission_detail, name='verify_submission_detail'),

]