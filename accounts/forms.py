from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
    }))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            qs = User.objects.filter(username=username)
            if not qs.exists():
                raise forms.ValidationError('User does not exists')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Invalid password')
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user is not active')
        return super().clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
    }))
    password2 = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }))

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Passwords are not identical, please, try again!')
        return data['password2']