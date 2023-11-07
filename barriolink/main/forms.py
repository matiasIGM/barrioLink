from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, CustomUser, JuntaDeVecinos
from datetime import datetime 
from django import forms
from .models import Publicacion


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))


class RegisterFormStep1(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")
    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(
            years=range(datetime.now().year - 100, datetime.now().year),
        )
    )

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2", "rut", "birth_date", "celular", "nombres", "apellidos"]

class RegisterForm2(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email","numero_documento", "region", "comuna", "calle", "numero_domicilio"]        


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]

class CustomUserAdminRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "is_hoa_admin"]

class JuntaDeVecinosForm(forms.ModelForm):
    class Meta:
        model = JuntaDeVecinos
        fields = '__all__'

#  Crea una vista y un formulario para que el usuario administrador pueda crear nuevas publicaciones
class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'contenido']

