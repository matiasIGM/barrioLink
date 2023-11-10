from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterFormStep1, RegisterFormStep2, CustomUserAdminRegistrationForm, Post, JuntaDeVecinosForm, CommunitySpaceForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import  CustomUser, JuntaDeVecinos, Comuna, Region, CommunitySpace, Resident  # Importar el modelo de usuario personalizado
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
                return render(request, 'account/adm/profile.html')
            else:
                return render(request, 'account/users/profile.html')
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




def signup(request):
    form = RegisterFormStep1()  # Mueve la inicialización del formulario fuera del bloque if

    if request.method == 'POST':
        form = RegisterFormStep1(request.POST)
        if form.is_valid():
            # Imprime los datos del POST por consola
            print("Datos del POST:", request.POST)
            user = form.save()
            return redirect('login')
    else:
        form = RegisterFormStep1()

    return render(request, 'registration/sign_up.html', {'form': form})

# def signup(request):
#     Formulario de Datos Básicos
#     form_step1 = RegisterFormStep1()

#     Formulario de Datos de Residencia (Paso 2)
#     form_step2 = RegisterFormStep2()

#     if request.method == 'POST':
#         if 'step1_submit' in request.POST:
#             Procesar el formulario de Datos Básicos
#             form_step1 = RegisterFormStep1(request.POST)
#             if form_step1.is_valid():
#                 user = form_step1.save(commit=False)
#                 Puedes realizar operaciones adicionales con 'user' aquí si es necesario
#                 user.save()

#                 Redirigir al formulario de Datos de Residencia (Paso 2)
#                 return redirect('signup_step2')

#         elif 'step2_submit' in request.POST:
#             Procesar el formulario de Datos de Residencia
#             form_step2 = RegisterFormStep2(request.POST)
#             if form_step2.is_valid():
#                 Obtener el usuario creado en el paso 1
#                 user = CustomUser.objects.latest('id')

#                 Fusionar los datos del formulario de Datos de Residencia
#                 user.numero_documento = form_step2.cleaned_data['nro_documento']
#                 user.region = form_step2.cleaned_data['region']
#                 user.comuna = form_step2.cleaned_data['comuna']
#                 user.calle = form_step2.cleaned_data['calle']
#                 user.numero_domicilio = form_step2.cleaned_data['numero_domicilio']

#                 Puedes realizar operaciones adicionales con 'user' aquí si es necesario
#                 user.save()

#                 Redirigir a la página de inicio de sesión
#                 return redirect('login')
#     print("Datos del POST:", request.POST)    

#     return render(request, 'registration/sign_up.html', {'form_step1': form_step1, 'form_step2': form_step2})


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


def reservation(request):
    return render(request, 'account/users/reservations.html')

def profileUser(request):
    return render(request, 'account/users/profile.html')


#  User Functions 
#==============================================================
def userDocuments(request):
    return render(request, 'account/users/documents.html')

def newsPublish(request):
    return render(request, 'account/users/news_publish.html')

def userProfile(request):
    return render(request, 'account/users/profile.html')

def userReservation(request):
    return render(request, 'account/users/reservations.html')

# Admin User Functions 
#==============================================================
def adminPublish(request):
    return render(request, 'account/adm/news_publish.html')

def adminPublishValidation(request):
    return render(request, 'account/adm/news_validation.html')

def adminNotifications(request):
    return render(request, 'account/adm/notifications.html')

def adminProfile(request):
    return render(request, 'account/adm/profile.html')

def adminUserList(request):
    return render(request, 'account/adm/user_list.html')

def adminUserValidation(request):
    return render(request, 'account/adm/user_validation.html')


def def_validation_view(request):
    # Obtener todos los usuarios donde is_hoa_admin sea False y is_active sea True
    users = CustomUser.objects.filter(is_hoa_admin=False, is_active=True)
    
    # Guardar los usuarios en el contexto
    context = {'users': users}

    return render(request, 'account/adm/user_validation.html', context)


def adminValidateReservations(request):
    return render(request, 'account/adm/reservations.html')

def userProfileConfig(request):
    return render(request, 'account/adm/reservation_config.html')


def adminProfileConfig(request):
    return render(request, 'account/adm/profile_settings.html')


@login_required
def hoaConfig(request):
    try:
        # Obtener el residente asociado al usuario actual
        resident = Resident.objects.get(user=request.user.id)
        # Obtener los datos de la Junta de Vecinos relacionados con el residente
        hoa_data = resident.hoa
    except Resident.DoesNotExist:
        # Manejar el caso en el que el usuario no tiene un residente asociado
        hoa_data = None

    # Imprimir información en la consola
    # print("ID del usuario actual:", request.user.id)
    # print("Residente asociado:", resident)
    # print("Datos de la Junta de Vecinos:", hoa_data)

    # Pasar datos al contexto
    context = {'hoa_data': hoa_data}

    # Renderizar la página con el contexto
    return render(request, 'account/adm/hoa_config.html', context)
   

@login_required
def adminConfigPlaces(request):
    # Listar todos los espacios comunitarios
    community_spaces = CommunitySpace.objects.all()
    
    # Imprimir el resultado de la consulta en la consola
    # for space in community_spaces:
    #     print(f'Nombre: {space.name}, Descripción: {space.description}, Capacidad Máxima: {space.max_capacity}')

    context = {'community_spaces': community_spaces}
    # if request.method == 'POST':
    #     form = CommunitySpaceForm(request.POST)
    #     space_id = request.POST.get('space_id')

    #     if space_id:
    #         # Actualizar un espacio comunitario existente
    #         space = CommunitySpace.objects.get(pk=space_id)
    #         form = CommunitySpaceForm(request.POST, instance=space)
    #     elif form.is_valid():
    #         # Crear un nuevo espacio comunitario
    #         form.save()

    #     return redirect('admin_places')

    # else:
    #     form = CommunitySpaceForm()

    return render(request, 'account/adm/reservation_config.html', context)






