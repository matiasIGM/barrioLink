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
