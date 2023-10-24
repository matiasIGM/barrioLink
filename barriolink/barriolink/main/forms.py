from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, CustomUser
from datetime import datetime 


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))

class RegisterForm(UserCreationForm): # formulario para utilizar ModelForm
    email = forms.EmailField(required=True, label="Correo Electrónico")

    # Personalización del formato de entrada para birth_date
    birth_date = forms.DateField(
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type':'date', 'max': datetime.now().date()}))
     

    class Meta:
        model = CustomUser   # Utiliza el modelo de usuario personalizado
        fields = ["email", "password1", "password2", "rut", "birth_date", "celular", "nombres", "apellidos"]
        


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]