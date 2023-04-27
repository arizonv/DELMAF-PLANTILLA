from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserAdminCreationForm(UserCreationForm):
    # Añade las clases de estilo de Bootstrap a los widgets del formulario
    username = forms.CharField(max_length=15)
    name = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=20)
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1', 'password2']
