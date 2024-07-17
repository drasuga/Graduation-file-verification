from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Submission,Student
from .forms import SubmissionForm, StudentRegistrationForm
from django.core.mail import send_mass_mail, send_mail
from django.conf import settings


# def student_register(request):
#     if request.method == 'POST':
#         form = StudentRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('submission_list')
#     else:
#         form = StudentRegistrationForm()
#     return render(request, 'submissions/register.html', {'form': form})
def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        print("Form data:", request.POST)
        if form.is_valid():
            print("Form is valid")
            print("Cleaned data:", form.cleaned_data)
            try:
                user = form.save()
                print("User saved:", user)
                student = Student.objects.get(user=user)
                print("Student saved:", student)
                print("Student details:")
                for field in student._meta.fields:
                    print(f"{field.name}: {getattr(student, field.name)}")
                login(request, user)
                return redirect('submission_list')
            except Exception as e:
                print("Error:", str(e))
                form.add_error(None, "An error occurred while creating your account. Please try again.")
        else:
            print("Form errors:", form.errors)
    else:
        form = StudentRegistrationForm()
    return render(request, 'submissions/register.html', {'form': form})

@login_required
def submit_file(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user.student
            submission.save()
            return redirect('submission_list')
    else:
        form = SubmissionForm()
    return render(request, 'submissions/submit_file.html', {'form': form})
    




def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('verify_submissions')
        else:
            messages.error(request, 'Invalid login credentials or insufficient permissions.')
    return render(request, 'submissions/admin_login.html')

@user_passes_test(lambda u: u.is_staff)
def verify_submissions(request):

    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        action = request.POST.get('action')
        submission = get_object_or_404(Submission, id=submission_id)
        submission.highschool_certificate = 'highschool_certificate' in request.POST
        submission.secondary_certificate = 'secondary_certificate' in request.POST
    
        if action == 'verify':
            submission.is_verified = True
            submission.verification_notes = request.POST.get('verification_notes', '')
            submission.save()
            messages.success(request, f'Submission {submission_id} has been verified.')
        elif action == 'reject':
            submission.is_rejected = True
            submission.verification_notes = request.POST.get('verification_notes', '')
            submission.save()
            messages.success(request, f'Submission {submission_id} has been rejected and removed.')
        
    
    unverified_submissions = Submission.objects.filter(is_verified=False)
    return render(request, 'submissions/verify_submissions.html', {'submissions': unverified_submissions})

# @user_passes_test(lambda u: u.is_staff)
# def notify_verified_submissions(request):
#     verified_submissions = Submission.objects.filter(is_verified=True, certificates_available=True, notified=False)
#     for submission in verified_submissions:
#         send_mail(
#             'Certificates Available',
#             'Your certificates are now available for collection.',
#             'from@example.com',
#             [submission.student.user.email],
#             fail_silently=False,
#         )
#         submission.notified = True
#         submission.save()
#     messages.success(request, f'{verified_submissions.count()} students have been notified.')
#     return redirect('verify_submissions')

# @user_passes_test(lambda u: u.is_staff)
# def set_certificates_available(request):
#     if request.method == 'POST':
#         Submission.objects.filter(is_verified=True).update(certificates_available=True)
#         messages.success(request, 'All verified submissions have been notified of certificate availability.')
#     return render(request, 'submissions/set_certificates_available.html')


# @user_passes_test(lambda u: u.is_staff)
# def set_certificates_available(request):
#     if request.method == 'POST':
#         verified_submissions = Submission.objects.filter(is_verified=True, certificates_available=False)
        
#         emails = []
#         for submission in verified_submissions:
#             subject = "Certificates Available for Collection"
#             message = f"Dear {submission.student.user.username},\n\nYour certificates are now available for collection. Please visit our office to collect them.\n\nBest regards,\nAdmin Team"
#             from_email = settings.DEFAULT_FROM_EMAIL
#             recipient_list = [submission.student.user.email]
#             emails.append((subject, message, from_email, recipient_list))
#         send_mass_mail(emails)
#         verified_submissions.update(certificates_available=True)
#         messages.success(request, 'All verified submissions have been notified of certificate availability.')
#     return render(request, 'submissions/set_certificates_available.html')


@user_passes_test(lambda u: u.is_staff)
def set_certificates_available(request):
    verified_submissions = Submission.objects.filter(is_verified=True, certificates_available=False)
    
    if request.method == 'POST':
        selected_ids = request.POST.getlist('submissions')
        emails = []
        for submission in Submission.objects.filter(id__in=selected_ids):
            subject = "Certificates Available for Collection"
            message = f"Dear {submission.student.name},\n\nYour certificates are now available for collection. Please visit our office to collect them.\n\nBest regards,\nAdmin Team"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [submission.student.email]
            emails.append((subject, message, from_email, recipient_list))
        send_mass_mail(emails)
        Submission.objects.filter(id__in=selected_ids).update(certificates_available=True)
        messages.success(request, f'{len(selected_ids)} submissions have been marked as certificates available.')
        return redirect('set_certificates_available')

    context = {
        'verified_submissions': verified_submissions
    }
    return render(request, 'submissions/certificates_available.html', context)


@login_required
def submission_list(request):
    submissions = Submission.objects.filter(student=request.user.student)
    submission = submissions.last()
   
    return render(request, 'submissions/submission_list.html', {'submission':submission})

import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .models import Student, Submission

@user_passes_test(lambda u: u.is_staff)
def download_student_details(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_details.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Student ID', 'Email', 'Programme', 'Session', 'Registration Number', 
                     'Birth Date', 'Birth Location', 'Year of Admission', 'Admission Number', 'Phone Number'])

    students = Student.objects.all()
    for student in students:
        writer.writerow([student.name, student.student_id, student.email, student.programme, 
                         student.session, student.registration_number, student.birth_date, 
                         student.birth_location, student.year_of_admission, student.admission_number, 
                         student.phone_number])

    return response

@user_passes_test(lambda u: u.is_staff)
def download_verified_submissions(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="verified_submissions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Student ID', 'Submission Date', 'Verification Notes'])

    submissions = Submission.objects.filter(is_verified=True)
    for submission in submissions:
        writer.writerow([submission.student.name, submission.student.student_id, 
                         submission.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 
                         submission.verification_notes])

    return response

@user_passes_test(lambda u: u.is_staff)
def download_available_certificates(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="available_certificates.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Student ID', 'Programme', 'Session'])

    submissions = Submission.objects.filter(is_verified=True, certificates_available=True)
    for submission in submissions:
        writer.writerow([submission.student.name, submission.student.student_id, 
                         submission.student.programme, submission.student.session])

    return response


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Submission

@user_passes_test(lambda u: u.is_staff)
def verify_submissions_list(request):
    unverified_submissions = Submission.objects.filter(is_verified=False, is_rejected=False)
    context = {
        'submissions': unverified_submissions
    }
    return render(request, 'submissions/verify_submissions_list.html', context)

@user_passes_test(lambda u: u.is_staff)
def verify_submission_detail(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        submission.highschool_certificate = 'highschool_certificate' in request.POST
        submission.secondary_certificate = 'secondary_certificate' in request.POST
        
        if action == 'verify':
            submission.is_verified = True
            submission.verification_notes = request.POST.get('verification_notes', '')
            submission.save()
            messages.success(request, f'Submission {submission_id} has been verified.')
        elif action == 'reject':
            submission.is_rejected = True
            submission.verification_notes = request.POST.get('verification_notes', '')
            submission.save()
            messages.success(request, f'Submission {submission_id} has been rejected.')
        
        return redirect('verify_submissions')
    
    context = {
        'submission': submission

    }
    return render(request, 'submissions/verify_submission_detail.html', context)


