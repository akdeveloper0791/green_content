from django import forms


class SignupForm(forms.Form):
    first_name=forms.CharField(max_length=20)
    last_name=forms.CharField(max_length=20)
    email=forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())

class LoginForm(forms.Form):
   email = forms.EmailField()
   password = forms.CharField(widget = forms.PasswordInput())