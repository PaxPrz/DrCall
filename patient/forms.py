from django import forms
from .models import Patient
from main.models import User
from django.contrib.auth.forms import UserCreationForm

class PatientCreationForm(UserCreationForm):
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(str(self.cleaned_data['email'])+' already exists!')
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['name', 'username', 'contact', 'gender', 'email', 'password1', 'password2']


class PatientUpdateForm(forms.ModelForm):
    name = forms.CharField(label="Name", max_length=50, required=False)
    location = forms.CharField(label="Location", max_length=50, required=False)
    dob = forms.DateField(label="Date of Birth", required=False)
    contact = forms.CharField(label="Contact no.", max_length=15, required=False)
    profile_pic = forms.ImageField(label="Profile Picture", required=False)

    class Meta:
        model = Patient
        fields = ['name', 'location', 'dob', 'contact', 'profile_pic']

class ProfileSearchForm(forms.Form):
    name = forms.CharField(required=False)