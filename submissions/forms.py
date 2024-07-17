from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Submission
from django.utils import timezone

class StudentRegistrationForm(UserCreationForm):
    student_id = forms.CharField(max_length=20, help_text='Enter your student ID')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')
    programme = forms.CharField(max_length=100, help_text='Enter your programme')
    session = forms.CharField(max_length=50, help_text='Enter your session')
    registration_number = forms.CharField(max_length=50, help_text='Enter your registration number')
    name = forms.CharField(max_length=100, help_text='Enter your full name')
    birth_date = forms.DateField(help_text='Enter your birth date')
    birth_location = forms.CharField(max_length=100, help_text='Enter your birth location')
    year_of_admission = forms.IntegerField(help_text='Enter your year of admission')
    admission_number = forms.CharField(max_length=50, help_text='Enter your admission number')
    phone_number = forms.CharField(max_length=20, help_text='Enter your phone number')

    class Meta:
        model = User
        fields = ('username', 'student_id', 'password1', 'password2', 'email', 'programme', 'session', 'registration_number',
                  'name', 'birth_date', 'birth_location', 'year_of_admission', 'admission_number', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            student_data = {
                'user': user,
                'student_id': self.cleaned_data.get('student_id'),
                'email': self.cleaned_data.get('email'),
                'programme': self.cleaned_data.get('programme'),
                'session': self.cleaned_data.get('session'),
                'registration_number': self.cleaned_data.get('registration_number'),
                'name': self.cleaned_data.get('name'),
                'birth_date': self.cleaned_data.get('birth_date'),
                'birth_location': self.cleaned_data.get('birth_location'),
                'year_of_admission': self.cleaned_data.get('year_of_admission'),
                'admission_number': self.cleaned_data.get('admission_number'),
                'phone_number': self.cleaned_data.get('phone_number'),
            }
            student, created = Student.objects.update_or_create(
                user=user,
                defaults=student_data
            )
            print("Student created:", created)
            print("Student details:")
            for key, value in student_data.items():
                print(f"{key}: {value}")
            print("Saved student details:")
            for field in student._meta.fields:
                print(f"{field.name}: {getattr(student, field.name)}")
        return user
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     if commit:
    #         user.save()
    #         Student.objects.create(user=user, student_id=self.cleaned_data['student_id'])
    #     return user
    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
# class StudentRegistrationForm(UserCreationForm):
#     student_id = forms.CharField(max_length=20, help_text='Enter your student ID')

#     class Meta:
#         model = User

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['highschool_certificate', 'secondary_certificate']
        widgets = {
            'highschool_certificate': forms.CheckboxInput,
            'secondary_certificate': forms.CheckboxInput
        }

    def clean(self):
        cleaned_data = super().clean()
        if not any(cleaned_data.values()):
            raise forms.ValidationError("At least one document must be selected.")
        return cleaned_data