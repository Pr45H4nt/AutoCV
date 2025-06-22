from django import forms
from .models import Resume, Education, Experience, PersonalInfo, SkillCategory, Skill, AchievementsCertifications, Projects
from django.forms import inlineformset_factory


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title',]

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = '__all__'
        exclude = ['resume',]
    
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Full Name',
                'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Address',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone Number',
                'class': 'form-control'
            }),
            'website': forms.URLInput(attrs={
                'placeholder': 'Personal Website',
                'class': 'form-control'
            }),
            'github_username': forms.TextInput(attrs={
                'placeholder': 'GitHub Username',
                'class': 'form-control'
            }),
            'github_link': forms.URLInput(attrs={
                'placeholder': 'GitHub Profile Link',
                'class': 'form-control'
            }),
            'linked_in_username': forms.TextInput(attrs={
                'placeholder': 'LinkedIn Username',
                'class': 'form-control'
            }),
            'linked_in_link': forms.URLInput(attrs={
                'placeholder': 'LinkedIn Profile Link',
                'class': 'form-control'
            }),
            'position_title': forms.TextInput(attrs={
                'placeholder': 'Position Title (e.g., Software Developer)',
                'class': 'form-control'
            }),
            'summary': forms.Textarea(attrs={
                'placeholder': 'Write a brief summary about yourself',
                'class': 'form-control',
                'rows': 4
            }),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institute', 'field_of_study', 'start_date', 'end_date', 'gpa', 'currently_studying']


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'position', 'start_date', 'end_date', 'description', 'currently_working']



class Achievecertiform(forms.ModelForm):
    class Meta:
        model = AchievementsCertifications
        fields = ['title',]


class Projectsform(forms.ModelForm):
    class Meta:
        model = Projects
        fields = '__all__'
        exclude = ['resume', ]


        