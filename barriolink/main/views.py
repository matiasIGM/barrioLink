from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterFormStep1, RegisterFormStep2, CustomUserAdminRegistrationForm, PublicacionForm, JuntaDeVecinosForm, CommunitySpaceForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import  CustomUser, ResidenceCertificate, Comuna, Region, CommunitySpace, Resident, Publicacion  # Importar el modelo de usuario personalizado
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
from reportlab.pdfgen import canvas
from django.utils import timezone
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from io import BytesIO
import os
from datetime import date
import uuid
import qrcode

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
#Ruta de template html base para renderizar el PDF
template = get_template(os.path.join('account', 'pdf', 'pdf_template.html'))

def render_to_pdf(template_src, context_dict={}):
    template_path = os.path.join('account', 'pdf', template_src)
    template = get_template(template_path)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class ViewPDF(View):
    
    def save_certificate_to_db(self, resident, hoa_data, user_data):
        # Obtener la fecha actual
        current_date = date.today()

        # Crear un nuevo objeto de certificado de residencia
        certificate = ResidenceCertificate.objects.create(
            resident=user_data,
            certificate_date=current_date,
            certificate_filename='nombre_archivo.pdf',  # Reemplaza con el nombre real del archivo PDF
            certificate_status='Generado',
            hoa=hoa_data,
            generated_by_user=user_data
        )

        # Guardar el objeto en la base de datos
        certificate.save()
        
    def get(self, request, *args, **kwargs):
        result = {}  #  diccionario vacío para guardar datos

        try:
            # Obtener el residente asociado al usuario actual
            resident = Resident.objects.get(user=request.user.id)
            # Obtener los datos de la Junta de Vecinos relacionados con el usuario
            hoa_data = resident.hoa
        except Resident.DoesNotExist:
            # Manejar el caso en que el usuario no tiene un residente asociado
            hoa_data = None

        # Obtener los datos del usuario actual(logeado)
        user_data = request.user
        if hoa_data:
            # Obtener los datos de la Junta de Vecinos asociada al usuario
            junta_data = hoa_data
        else:
            # En caso de que no haya una asociación de usuario
            junta_data = None

        # Agregar datos al diccionario de resultado
        if junta_data:
            result["hoa_name"] = junta_data.hoa_name
            result["hoa_city"] = junta_data.legal_address
            result["junta_rut"] = junta_data.rut
            result["junta_contact_phone"] = junta_data.contact_phone
            result["junta_email"] = junta_data.contact_email
            result["rep_name"] = junta_data.legal_representative_name
            result["rep_rut"] = junta_data.legal_representative_rut
             
        else:
            # Set como no disponible si los datos no existen o faltan
            result["hoa_name"] = "No disponible"
            result["hoa_city"] = "No disponible"
            result["junta_rut"] = "No disponible"
            result["junta_contact_phone"] = "No disponible"

        result["user_name"] = user_data.nombres
        result["user_lastname"] = user_data.apellidos
        result["user_rut"] = user_data.rut
        result["user_comuna"] = user_data.comuna
        result["user_calle"] = user_data.calle
        result["user_numero_domicilio"] = user_data.numero_domicilio
        result["user_celular"] = user_data.celular
        result["current_date"] = date.today()

        # Generar un UUID4
        result["uuid"] = str(uuid.uuid4())

        # Generar un código QR para la URL 'barriolink.online/certifica/:uuid'
        qr_data = f'barriolink.online/certifica/{result["uuid"]}'
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_image = BytesIO()
        img.save(qr_image, format='PNG')
        result["qr_code"] = qr_image.getvalue()

         # Generar el certificado PDF
        template = get_template(os.path.join('account', 'pdf', 'pdf_template.html'))
        context = {'result': result}  # Corregir la clave a 'result'
        html = template.render(context)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), response)

        if not pdf.err:
            # Enviar el certificado PDF como respuesta HTTP
            certificate_data = response.getvalue()
            response.close()
            response = HttpResponse(certificate_data, content_type='application/pdf')

            # Guardar los datos en la base de datos
            self.save_certificate_to_db(resident, hoa_data, user_data)

            return response

        return None
    
        

class ViewPDF1(View):
    def get(self, request, *args, **kwargs):
        data = hoaConfig(request)
        template = get_template(os.path.join('account', 'pdf', 'pdf_template.html'))
        context = {'data': data}  # Crear un diccionario con la clave 'data'
        print(context)
        html = template.render(context)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), response)

        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')

        return None
# class ViewPDF(View):
#     def get(self, request, *args, **kwargs):
#         pdf = render_to_pdf('pdf_template.html', data)
#         return HttpResponse(pdf, content_type='application/pdf')

class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('pdf_template.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response

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
