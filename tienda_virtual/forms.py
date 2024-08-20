from django import forms
#from django.contrib.auth.models import User
from users.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(label='Usuario',required=True, min_length=4, max_length=40,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'id': 'username'}))
    email = forms.EmailField(label='Correo',required=True, widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                        'id': 'email',
                                                                        'placeholder': 'example@gmail.com'}))
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                            'id':'password'}))
    password2 = forms.CharField(label='Confirmar contraseña', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario ya se encuentra en uso')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo ya se encuentra en uso')
        return email

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'Las contraseñas no coinciden')
    
    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password')
        )