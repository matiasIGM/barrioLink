from django.shortcuts import render, redirect
from .forms import RegisterFormStep1, PostForm, RegisterForm2, CustomUserAdminRegistrationForm, Post, JuntaDeVecinosForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import  CustomUser, JuntaDeVecinos, Comuna, Region  # Importar el modelo de usuario personalizado
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding  import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core import serializers
import logging
from django.contrib import messages

# @login_required(login_url="/login")
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Las credenciales son válidas, inicia sesión al usuario.
            login(request, user)
            # Redirige al perfil después del inicio de sesión, pero también verifica si es admin.
            if user.is_hoa_admin:
                return render(request, 'adm/profile/profile.html')
            else:
                return render(request, 'profile/profile.html')
        else:
            # Las credenciales son inválidas, muestra un mensaje de error o redirige a la página de inicio de sesión.
            messages.error(request, "Credenciales inválidas. Por favor, inténtalo de nuevo.")
            return render(request, 'registration/login.html')  # Agrega la línea para volver a la página de inicio de sesión
    return render(request, 'registration/login.html')


def users_admin_view(request):
    # Lógica de tu vista
    return render(request, 'adm/users_admin.html')



def sign_up(request):
    if request.method == 'POST':
        form = RegisterFormStep1(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Convierte la fecha en una cadena
            data['birth_date'] = data['birth_date'].strftime('%Y-%m-%d')
            request.session['registro_primer_paso'] = data
            return redirect('registro_segundo_paso')
    else:
        form = RegisterFormStep1()
    return render(request, 'registration/sign_up.html', {'form': form})



# def sign_up_2(request):  
#      form = RegisterForm2(request.POST)
#      if form.is_valid():
#             datos_primer_paso = request.session.get('registration/sign_up.html', {})
#             datos_segundo_paso = form.cleaned_data
#             datos_primer_paso.update(datos_segundo_paso)
#             user = CustomUser(**datos_primer_paso)
#             user.save()
#             del request.session['registration/sign_up.html']
#             return redirect('login')
#      else:
#         form = RegisterForm2()
#      return render(request, 'registration/sign_up_step_2.html', {'form': form})

logger = logging.getLogger(__name__)

    
def signup(request, step=None):
    datos_primer_paso = {}
    if step == "step1":
        if request.method == 'POST':
            form = RegisterFormStep1(request.POST)
            if form.is_valid():
                # Almacena los datos del paso 1 en la sesión
                request.session['registro_primer_paso'] = form.cleaned_data
                return redirect('signup', step='step2')
        else:
            form = RegisterFormStep1()
        template = 'registration/sign_up.html'
    
    elif step == "step2":
        datos_primer_paso = request.session.get('registro_primer_paso', {})
        form = RegisterForm2(request.POST)

        if request.method == 'POST':
            if form.is_valid():
                datos_segundo_paso = form.cleaned_data
                datos_primer_paso.update(datos_segundo_paso)
                email = datos_primer_paso['email']

                # Registrar un mensaje en la consola para verificar los datos antes de guardarlos
                logger.info(f"Datos a registrar: {datos_primer_paso}")

                user, created = CustomUser.objects.get_or_create(email=email, defaults=datos_primer_paso)

                if created:
                    user.save()  # Guardar el nuevo usuario solo si se crea
                    del request.session['registro_primer_paso']  # Limpiar datos del primer paso
                    return redirect('login')
                else:
                    # Mostrar un mensaje de error al usuario indicando que el correo electrónico ya está en uso
                    form.add_error('email', 'Este correo electrónico ya está registrado.')
            else:
                # Registrar errores específicos en la consola
                for field, errors in form.errors.items():
                    for error in errors:
                        logger.warning(f"Error en el campo {field}: {error}")

        else:
            form = RegisterForm2()
        template = 'registration/sign_up_step_2.html'
    
    else:
        return HttpResponse("Paso no válido")

    return render(request, template, {
        'form': form,
        'nombre_completo': f"{datos_primer_paso.get('nombres', '')} {datos_primer_paso.get('apellidos', '')}",
        'rut': datos_primer_paso.get('rut', '')
    })


#Función para retornar todos los usuarios no admin
def filter_user_adm(request):
    usuarios = CustomUser.objects.all(is_hoa_admin=False)
    
    for usuario in usuarios:
        print(f"Usuario: {usuario.username}, Nombres: {usuario.nombres}, Apellidos: {usuario.apellidos}, Email: {usuario.email}")
    
    context = {'usuarios': usuarios}
    return render(request, 'adm/users_admin.html', context)



def certificado(request):
    return render('ruta certificado/certificado.html')

#Renderizar home del sitio
def home(request):
     return render(request, 'main/home.html')