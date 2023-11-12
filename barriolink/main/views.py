from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterFormStep1, RegisterFormStep2, CustomUserAdminRegistrationForm, PublicacionForm, JuntaDeVecinosForm, CommunitySpaceForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import  CustomUser, JuntaDeVecinos, Comuna, Region, CommunitySpace, Resident, Publicacion  # Importar el modelo de usuario personalizado
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
import telegram
from reportlab.pdfgen import canvas
from django.utils import timezone




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

def adminDocuments(request):
    return render(request, 'account/adm/documents.html')
#Generación de certificado de residencia
#==============================================================
def load_certificate_content():
    with open('templates/account/messages/residencia.txt', 'r', encoding='utf-8') as file:
        certificate_content = file.read()
    return certificate_content

def generate_pdf(request):
    try:
        # Obtener el residente asociado al usuario actual
        resident = Resident.objects.get(user=request.user)
        # Obtener los datos de la Junta de Vecinos relacionados con el residente
        hoa_data = resident.hoa
        # Obtener los datos del usuario
        user_data = request.user
    except (Resident.DoesNotExist, CustomUser.DoesNotExist):
        # Manejar el caso en el que el usuario no tiene un residente asociado
        hoa_data = None
        user_data = None

    response = PDFResponse(response_type='inline', filename=f'{user_data.username}_certificate.pdf')
    p = canvas.Canvas(response)

    # Cargar el contenido del certificado desde el archivo
    certificate_content = load_certificate_content()

    # Reemplazar las variables del certificado con los datos reales
    certificate_content = certificate_content.format(
        hoa_name=hoa_data.hoa_name if hoa_data else '',
        rut_hoa=hoa_data.rut if hoa_data else '',
        legal_address=hoa_data.legal_address if hoa_data else '',
        resident_name=f'{user_data.nombres} {user_data.apellidos}' if user_data else '',
        rut_resident=user_data.rut if user_data else '',
        comuna=user_data.comuna if user_data else '',
        street=user_data.calle if user_data else '',
        house_number=user_data.numero_domicilio if user_data else '',
        phone=user_data.celular if user_data else '',
        today=timezone.now().strftime('%Y-%m-%d')  # Usa timezone.now() para obtener la fecha actual
    )

    # Agregar el contenido del certificado al PDF
    lines = certificate_content.split('\n')
    y_position = 800
    for line in lines:
        p.drawString(100, y_position, line)
        y_position -= 20

    p.showPage()
    p.save()

    return render(request, 'account/adm/hoa_config.html')

#====================================================================================================

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


#Configuración de datos de la junta de vecinos
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
   
   
#Administración de espacios comunes.

#Listar todos los espacios comunitarios
@login_required
def adminConfigPlaces(request):
    # Listar todos los espacios comunitarios
    community_spaces = CommunitySpace.objects.all()

    context = {'community_spaces': community_spaces}
  
    return render(request, 'account/adm/reservation_config.html', context)

#Registrar Espacios Comunitarios
def registerPlace(request):
    form = CommunitySpaceForm()
    
    if request.method == 'POST':
        form = CommunitySpaceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Espacio registrado!')
            return redirect('/placesConfig/')
        else:
            messages.error(request, 'Error en el formulario. Por favor, verifica los datos.')
    else:
        form = CommunitySpaceForm()

    return render(request, 'account/adm/reservation_config.html', {'form': form})


#Eliminar Espacios Comunitarios
def deletePlace(request, id):
    place = CommunitySpace.objects.get(id=id)
    place.delete()

    messages.success(request, 'Espacio Comunitario eliminado!')

    return redirect('/placesConfig/')

#Actualizar Espacios Comunitarios
def updatePlace(request, id):
    place = get_object_or_404(CommunitySpace, id=id)

    if request.method == 'POST':
        form = CommunitySpaceForm(request.POST, instance=place)
        if form.is_valid():
            form.save()
            messages.success(request, 'Espacio Comunitario actualizado!')
            return redirect('admin_places')
        else:
            messages.error(request, 'Error en el formulario. Por favor, verifica los datos.')
    else:
        form = CommunitySpaceForm(instance=place)

    return render(request, 'account/adm/update_place_modal.html', {'form': form, 'place': place})




# crea una vista para el formulario y la página donde el usuario administrador completara la información
def publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST)
        if form.is_valid():
            publicacion = form.save()
            # Triggea el evento para enviar un mensaje a través del bot de Telegram
            enviar_mensaje_telegram(publicacion.titulo, publicacion.contenido)
            return redirect('ruta_de_redireccion')
    else:
        form = PublicacionForm()
    return render(request, 'account/adm/news_publish.html', {'form': form})

# usuario solicitud de publicacion de noticia
def solnoticias(request): 
    return render(request, 'account/users/news_publish.html')


# validacion de solicitudes de publicacion de noticias 
def validationoticias(request): 
    return render(request, 'account/adm/news_validation.html')
