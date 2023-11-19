from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterFormStep1, RegisterFormStep2, CustomUserAdminRegistrationForm, PublicacionForm, JuntaDeVecinosForm, CommunitySpaceForm, SolPublicacionForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import  CustomUser, ResidenceCertificate, Comuna, Region, CommunitySpace, Resident, JuntaDeVecinos, Crearsol  # Importar el modelo de usuario personalizado
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding  import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core import serializers
from django.contrib import messages
import telegram
from django.utils import timezone
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.template import defaultfilters
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from . email_utils import *
import json



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


#==========================
#render correo de test
def view_email(request):
    return render(request, 'account/email/rejection_account_email.html')


def def_validation_view(request):
    # Obtener todos los usuarios donde is_hoa_admin sea False y is_active sea True
    users = CustomUser.objects.filter(is_hoa_admin=False, is_active=False)
    
    # Guardar los usuarios en el contexto
    context = {'users': users}

    return render(request, 'account/adm/user_validation.html', context)

#Función para validar activación de cta de usuario
def activate_user(request, user_id):
    # Obtén el objeto CustomUser o devuelve un error 404 si no existe
    custom_user = get_object_or_404(CustomUser, id=user_id)
    # Cambia el estado de is_active a True
    custom_user.is_active = True
    # Llama a la función para enviar el correo de activación exitosa
    activation_email_rendered(custom_user)
    # Guarda los cambios en la base de datos
    custom_user.save()
    messages.error(request, "Usuario activado correctamente")
    # Puedes devolver una respuesta JSON si lo deseas
    return JsonResponse({'message': 'Usuario activado correctamente'})

# def denegar_usuario(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_id = data.get('user_id')
#         motivo = data.get('motivo')

#         # Obtén el objeto CustomUser o devuelve un error 404 si no existe
#         custom_user = get_object_or_404(CustomUser, id=user_id)

#         # Cambia el estado de is_active a False
#         custom_user.is_active = False
#         custom_user.save()

#         # Envía el correo de rechazo
#         reject_email_rendered(custom_user, motivo)

#         # Devuelve una respuesta JSON si es necesario
#         return JsonResponse({'message': 'Usuario denegado correctamente'})
#     else:
#         # Devuelve una respuesta de error si la solicitud no es de tipo POST
#         return JsonResponse({'error': 'Método no permitido'}, status=405)

def denegar_usuario(request):
    try:
        user_id = int(request.POST.get('user_id', ''))
        motivo = request.POST.get('motivo', '')

        # Asegúrate de que user_id sea un número válido
        if not user_id:
            return JsonResponse({'error': 'El ID del usuario no es un número válido.'}, status=400)

        # Resto de la lógica para denegar al usuario...

        return JsonResponse({'success': 'Usuario denegado correctamente.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
     
    
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

    # Pasar datos al contexto
    context = {'hoa_data': hoa_data}

    # Renderizar la página con el contexto
    return render(request, 'account/adm/hoa_config.html', context)

@login_required                                                                                
def editHoaConfig(request, hoa_id):
    # Obtener los datos de la Junta de Vecinos para editar
    hoa_data = get_object_or_404(JuntaDeVecinos, hoa_id=hoa_id)
    hoa_data.formatted_foundation_date = defaultfilters.date(hoa_data.foundation_date, "d-m-Y")
    return render(request, 'account/adm/hoa_config.html', {'hoa_data': hoa_data, 'editable': True})

@login_required                                                                                
def updateHoaConfig(request, hoa_id):                               
    # Obtener los datos de la Junta de Vecinos a actualizar
    hoa_data = get_object_or_404(JuntaDeVecinos, hoa_id=hoa_id)
    if request.method == 'POST':
        
        # Procesar el formulario con los datos actualizados
        form = JuntaDeVecinosForm(request.POST, instance=hoa_data)
        
        if form.is_valid():
            
                    # Guardar los cambios si el formulario es válido
            form.save()
                    # Mostrar mensaje de éxito
            messages.success(request, 'Cambios guardados exitosamente.')
                    # Redirigir a la vista de configuración
            return redirect('admin_hoa')
        else:
            # Mostrar mensaje de error si hay problemas en el formulario
            print("Errores en el formulario:", form.errors)
            messages.error(request, 'Error en el formulario. Por favor, corrige los errores.')
    else:
            # Formulario para mostrar los datos actuales
            form = JuntaDeVecinosForm(instance=hoa_data)
    
    return render(request, 'account/adm/hoa_config.html', {'hoa_data': hoa_data, 'editable': True, 'form': form})
#===================================================================================================
   
#Administración de espacios comunes.

#Listar todos los espacios comunitarios
@login_required
def adminConfigPlaces(request):
    # Listar todos los espacios comunitarios
    community_spaces = CommunitySpace.objects.all()

    context = {'community_spaces': community_spaces}
  
    return render(request, 'account/adm/reservation_config.html', context)



def editCommunitySpace(request, space_id):
    space = get_object_or_404(CommunitySpace, id=space_id)
    form = CommunitySpaceForm(instance=space)
    return render(request, 'account/adm/edit_form.html', {'form': form, 'space_id': space_id})


def updateCommunitySpace(request, space_id):
    space = get_object_or_404(CommunitySpace, id=space_id)
    form = CommunitySpaceForm(request.POST, instance=space)
    if form.is_valid():
        form.save()
        return redirect('/placesConfig/')
    return JsonResponse({'error': 'Invalid form data'})


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
#==============================================================
def publicacion(request):# crea una vista para el formulario y la página donde el usuario administrador completara la información
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


# validacion de solicitudes de publicacion de noticias 
def validationoticias(request): 
    solicitudes = Crearsol.objects.all()

    filtro = request.GET.get('filtro', None)

    #filtr0 según el parámetro 'filtro'
    if filtro == 'nueva':
        solicitudes = Crearsol.objects.filter(estado='nueva')
    elif filtro == 'validada':
        solicitudes = Crearsol.objects.filter(estado='validada')
    elif filtro == 'eliminada':
        solicitudes = Crearsol.objects.filter(estado='eliminada')
    else:
        solicitudes = Crearsol.objects.all()

    # Configura la paginación
    paginator = Paginator(solicitudes, 5)  # 10 solicitudes por página
    page = request.GET.get('page', 1)
    solicitudes_paginadas = paginator.get_page(page)

    # Envia las solicitudes paginadas a la plantilla
    context = {'solicitudes': solicitudes_paginadas, 'filtro_actual': filtro}
    return render(request, 'account/adm/news_validation.html', context)


def cambiar_estado(request, solicitud_id, nuevo_estado):
    solicitud = get_object_or_404(Crearsol, pk=solicitud_id)
    solicitud.estado = nuevo_estado
    solicitud.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def recuperar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Crearsol, pk=solicitud_id)
    solicitud.estado = 'nueva'
    solicitud.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# User Functions 
#==============================================================



# User News Functions 
#==============================================================
def solnoticias(request): # usuario solicitud de publicacion de noticia
    return render(request, 'account/users/news_publish.html')   

def crearsolicitud(request): # usuario solicitud de publicacion de noticia
    if request.method == 'POST':
        form = SolPublicacionForm(request.POST)
        if form.is_valid():
            solnoticias = form.save(commit=False)
            usuario = request.user
            solnoticias.usersol = usuario
            solnoticias.save()
            # Limpiar el formulario
            #form = SolPublicacionForm()
            return render(request, 'account/users/news_publish.html')  
    else:
        form = SolPublicacionForm()
    return render(request, 'account/users/news_publish.html', {'form': form})    



