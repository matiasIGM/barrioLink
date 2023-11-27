
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
<<<<<<< HEAD
from .models import  CustomUser, JuntaDeVecinos, CommunitySpace, Publicacion
=======
from .models import  CustomUser, JuntaDeVecinos, CommunitySpace, Publicacion, Crearsol
>>>>>>> dev_matias
from datetime import datetime 
from django import forms
from .models import Publicacion
from .models import Crearsol


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
        fields = ["email", "password1", "password2", "rut", "birth_date", "celular", "nombres", "apellidos", "numero_documento","region", "comuna", "calle", "numero_domicilio"]
        
    #Validación registro de email       
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = CustomUser.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"El correo {email} ya se encuentra registado.")


    
class RegisterFormStep2(UserCreationForm):
    nro_documento = forms.CharField(max_length=12, required=True, label="Nro_Documento")
    region = forms.CharField(max_length=100, required=True, label="Región")
    comuna = forms.CharField(max_length=100, required=True, label="Comuna")
    calle = forms.CharField(max_length=255, required=True, label="Calle")
    numero_domicilio = forms.CharField(max_length=10, required=True, label="Número Domicilio")

    fields = ["email", "password1", "password2", "rut", "birth_date", "celular", "nombres", "apellidos"]

class RegisterForm2(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["numero_documento","region", "comuna", "calle", "numero_domicilio"]
    
    

class CustomUserAdminRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "is_hoa_admin"]

#Configuracion de Junta de Vecinos 
class JuntaDeVecinosForm(forms.ModelForm):
    class Meta:
        model = JuntaDeVecinos
        fields = '__all__'
        
        widgets = {
            'foundation_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
        
#Espacio comunitarios        
class CommunitySpaceForm(forms.ModelForm):
    space_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = CommunitySpace
        fields = ['name', 'description', 'max_capacity']
        


#  Crea una vista y un formulario para que el usuario administrador pueda crear nuevas publicaciones
class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'contenido']
<<<<<<< HEAD
=======
        fields = ['contenido']
        exclude = ['fecha_publicacion'] 
>>>>>>> dev

class SolPublicacionForm(forms.ModelForm):
    class Meta:
        model = Crearsol
        fields = ['contenido']
        exclude = ['fecha_publicacion'] 
<<<<<<< HEAD

=======
        
        
#Editar usuarios
class UsersUpdateForm(forms.ModelForm):
    user_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['nombres', 'apellidos', 'celular','calle']

#Editar perfil
class ProfileUpdateForm(forms.ModelForm):
    user_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['nombres', 'apellidos', 'celular','calle','email','birth_date']
>>>>>>> dev_matias
