from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Sexes, SkillLevels
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms.fields import EmailField
from django.forms.widgets import EmailInput
from django.forms.widgets import PasswordInput
from django.forms.forms import Form

class CustomProfileCreationForm(UserCreationForm):
    # email = EmailField(label='Email Address', required=True, widget=EmailInput(attrs={'class': 'form-control'}))
    # password1 = forms.CharField(label='Password', widget=PasswordInput(attrs={'class': 'form-control'}))
    # password2 = forms.CharField(label='Confirm Password', widget=PasswordInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(label='Middle Name', required=False, widget=forms.TextInput(attrs={'class': 'form-control border-2 border-gray-300'}))
    birth_date = forms.DateField(label='Birth Date', required=True, widget=forms.widgets.DateInput(attrs={'class': 'form-control border-2 border-gray-300', 'type': 'date'}))
    sex = forms.ChoiceField(label='Sex', choices=[('', 'Select...')] + list(Sexes.choices), required=True, widget=forms.Select(attrs={'class': 'form-control border-2 border-gray-300'}))
    skill_level = forms.ChoiceField(label='Skill Level', choices=[('', 'Select...')] + list(SkillLevels.choices), required=True, widget=forms.Select(attrs={'class': 'form-control border-2 border-gray-300'}))
    # phone_number = forms.CharField(label='Phone Number', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    school_or_club = forms.CharField(label='School/Club Name', required=False, widget=forms.TextInput(attrs={'class': 'form-control border-2 border-gray-300'}))
    usawkf_id = forms.CharField(label='USAWKF ID', required=False, widget=forms.TextInput(attrs={'class': 'form-control border-2 border-gray-300'}))

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')
        help_texts = {
            'username': "Letters, digits and @/./+/-/_ only.",

        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        self.fields['email'].widget.attrs.update({'placeholder': 'someone@example.com'})

        # Add CSS classes to the fields
        self.fields['username'].widget.attrs.update({'class': 'form-control border-2 border-gray-300'})
        self.fields['email'].widget.attrs.update({'class': 'form-control border-2 border-gray-300'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control border-2 border-gray-300'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control border-2 border-gray-300'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control border-2 border-gray-300'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control border-2 border-gray-300'})
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Please enter a valid email address.')
        
        if User.objects.filter(email=email).exists() or Profile.objects.filter(email=email).exists():
            raise ValidationError('This email is already in use.')
        
        return email
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date > timezone.now().date():
            raise ValidationError('Please enter a valid birth date.')
        
        return birth_date
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(user=user, 
                                   first_name=self.cleaned_data['first_name'],
                                   middle_name=self.cleaned_data['middle_name'],
                                   last_name=self.cleaned_data['last_name'],
                                   birth_date=self.cleaned_data['birth_date'],
                                   sex=self.cleaned_data['sex'],
                                   skill_level=self.cleaned_data['skill_level'],
                                   email=self.cleaned_data['email'],
                                #    phone_number=self.cleaned_data['phone_number'],
                                   school_or_club=self.cleaned_data['school_or_club'],
                                   usawkf_id=self.cleaned_data['usawkf_id']
                                   )

        return user

