from django.db import models
from django.contrib.auth.models import User
from django.utils import dates, timezone
from datetime import date, datetime


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    programme = models.CharField(max_length=100, blank=False, null=True)
    session = models.CharField(max_length=50, blank=False, null=True)
    registration_number = models.CharField(max_length=50, default=0, null=True, blank=False)
    name = models.CharField(max_length=100, blank=False, null=True)
    birth_date = models.DateField(default=timezone.now)
    birth_location = models.CharField(max_length=100, blank=False, null=True)
    year_of_admission = models.IntegerField(default=0, null=True, blank=False)
    admission_number = models.CharField(max_length=50, null=True, blank=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return f"{self.user.username if self.user else 'No user'} ({self.student_id})"

class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    birth_certificate = models.FileField(upload_to='static/documents/', null=True, blank=True)
    highschool_certificate = models.BooleanField(default= False)
    secondary_certificate = models.BooleanField(default= False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True)
    certificates_available = models.BooleanField(default=False)

    def __str__(self):
        return f"Submission by {self.student} on {self.timestamp}"
    



