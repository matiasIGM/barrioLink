from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from main.models import  CustomUser, ResidenceCertificate, Comuna, Region, CommunitySpace, Resident, Publicacion  # Importar el modelo de usuario personalizado
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
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from django.conf import settings


#  User Functions 
#==============================================================
def userDocuments(request):
    return render(request, 'account/users/documents.html')

def adminDocuments(request):
    return render(request, 'account/adm/documents.html')

#Generación de certificado de residencia
#==============================================================
#Ruta de template html base para renderizar el PDF
#==============================================================
def validator(request):
    pass

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
            result["signature"] = junta_data.signature_img
            result["logo"] = junta_data.logo_symbol
             
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
            box_size=3,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_image = BytesIO()
        img.save(qr_image, format='PNG')
        result["qr_code"] = base64.b64encode(qr_image.getvalue()).decode('utf-8')  # Convierte a base64

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
    
        

class DownloadPDF(View):
    def generate_pdf_and_qr(self, resident, hoa_data, user_data):
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

        result = {}  # diccionario vacío para almacenar datos

        # Agregar datos al diccionario de resultado
        if hoa_data:
            result["hoa_name"] = hoa_data.hoa_name
            result["hoa_city"] = hoa_data.legal_address
            result["junta_rut"] = hoa_data.rut
            result["junta_contact_phone"] = hoa_data.contact_phone
            result["junta_email"] = hoa_data.contact_email
            result["rep_name"] = hoa_data.legal_representative_name
            result["rep_rut"] = hoa_data.legal_representative_rut
            result["signature"] = hoa_data.signature_img
            result["logo"] = hoa_data.logo_symbol
        else:
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
        result["current_date"] = current_date

        # Generar un UUID4
        result["uuid"] = str(uuid.uuid4())

        # Generar un código QR para la URL 'barriolink.online/certifica/:uuid'
        qr_data = f'barriolink.online/certifica/{result["uuid"]}'
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_image = BytesIO()
        img.save(qr_image, format='PNG')
        result["qr_code"] = base64.b64encode(qr_image.getvalue()).decode('utf-8')  # Convierte a base64

        # Generar el certificado PDF
        template = get_template(os.path.join('account', 'pdf', 'pdf_template.html'))
        context = {'result': result}  # Corregir la clave a 'result'
        html = template.render(context)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)

        return pdf, result

    def send_email(self, to_email, subject, body, pdf_data, filename):
        # Configura el servidor SMTP y las credenciales desde settings.py
        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        smtp_username = settings.EMAIL_HOST_USER
        smtp_password = settings.EMAIL_HOST_PASSWORD

        # Configura el correo electrónico
        from_email = settings.DEFAULT_FROM_EMAIL
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Adjunta el PDF al correo electrónico
        pdf_attachment = MIMEApplication(pdf_data, _subtype="pdf")
        pdf_attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(pdf_attachment)

        # Agrega el cuerpo del correo electrónico (puedes personalizarlo según tus necesidades)
        msg.attach(MIMEText(body, 'html'))

        # Inicia la conexión con el servidor SMTP y envía el correo electrónico
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())

    def get(self, request, *args, **kwargs):
        resident = None
        hoa_data = None
        user_data = None

        try:
            # Obtener el residente asociado al usuario actual
            resident = Resident.objects.get(user=request.user.id)
            # Obtener los datos de la Junta de Vecinos relacionados con el usuario
            hoa_data = resident.hoa
        except Resident.DoesNotExist:
            # Manejar el caso en que el usuario no tiene un residente asociado
            hoa_data = None

        # Obtener los datos del usuario actual (logeado)
        user_data = request.user

        pdf, result = self.generate_pdf_and_qr(resident, hoa_data, user_data)

        response = HttpResponse(content_type='application/pdf')  # Inicializa la variable response

        if not pdf.err:
            pdf_data = response.getvalue()
            response.close()
            response = HttpResponse(pdf_data, content_type='application/pdf')
            filename = f"Certificado_residencia_{result['uuid']}.pdf"
            content = f"attachment; filename='{filename}'"
            response['Content-Disposition'] = content

            # Envía el correo electrónico con el PDF adjunto
            to_email = 'ma.garcesm@duocuc.cl'  # Cambia al destinatario deseado
            subject = 'Certificado de Residencia BarrioLink'
            body = '<p>Cuerpo del correo electrónico con HTML.</p>'  # Personaliza según tus necesidades
            self.send_email(to_email, subject, body, pdf_data, filename)

            # Puedes realizar acciones adicionales aquí antes de devolver la respuesta

            return response

        return None
   