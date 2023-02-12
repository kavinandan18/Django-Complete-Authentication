from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile
from django import forms

from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth import get_user_model

User = get_user_model()

class Signupform(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':'email',
            'id':'email',
            'type':'email',
            'placeholder':'Enter a valid email address',
            })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':'password1',
            'id':'password1',
            'type':'password',
            'placeholder':'Enter Password',
            })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':'password2',
            'id':'password2',
            'type':'password',
            'placeholder':'Enter Confirm Password',
            })
        
    class Meta:
        model = User
        fields = ('email','password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('password2')
        if password != confirm_password:
            raise forms.ValidationError("Password should be same" ,code= "invalid")

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':'email',
            'id':'email',
            'type':'email',
            'placeholder':'Enter a valid email address',
            })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':'password',
            'id':'password',
            'type':'password',
            'placeholder':'Enter valid Password',
            })
    class Meta:
        model = User
        fields = ('email', 'password',)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','first_name','last_name','location')

        widgets = {
            'first_name': forms.TextInput(
				attrs={
                    'placeholder':'Enter First Name...',
					'class': 'form-control',
					}
			),
            'last_name':forms.TextInput(
                attrs={
                    'placeholder':'Enter Last Name...',
					'class': 'form-control',
                }
            ),
            'email':forms.EmailInput(
                attrs={
                    'placeholder':'Enter vaild Email Address...',
					'class': 'form-control', 
                }
            ),
            'location':forms.TextInput(
                attrs={
                    'placeholder':'Loction',
					'class': 'form-control',
                }
            ),
        }

class ProfileEditForm(forms.ModelForm):
    dob = forms.DateField(
    widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
)





    gender = forms.ChoiceField(
        choices=Profile.GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'mobile': forms.TextInput(
                attrs={
                    'placeholder': 'Enter vaild Mobile Number...',
                    'class': 'form-control',
                }
            ),
            
            'bio': forms.Textarea(
                attrs={
                    'placeholder': 'Describe about you...',
                    'class': 'form-control',
                    'rows': 5,
                    'columns': 10
                }
            ),
            'avatar': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['gender'].initial = self.instance.gender



class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': "Old Password"})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "New Password"})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "New Password"})
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('new_password1')
        confirm_password = cleaned_data.get('new_password2')
        if password != confirm_password:
            raise forms.ValidationError("password should be same" ,code= "invalid")


class PasswordResetEmailForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'required':'',
            'name':'email',
            'id':'email',
            'type':'email',
            'placeholder':'Enter a valid email address',
            })

class NewSetPasswordForm(SetPasswordForm):
    error_css_class = 'error'
    required_css_class = 'required'

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        ),
        label="New password",
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        ),
        label="Confirm password",
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password1')
        confirm_password = cleaned_data.get('new_password2')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")