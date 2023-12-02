from django.shortcuts import render
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
from django.core.mail import send_mail , EmailMessage
#render correos


def activation_email_rendered(user):
    # Renderiza el correo de activación exitosa con el nombre y apellidos del usuario
    email_subject = 'Activación de Cuenta en BarrioLink'
    
    # Pasa nombres y apellidos al contexto del template
    context = {'user': user, 'nombres': user.nombres, 'apellidos': user.apellidos}
    
    # Renderiza el cuerpo del correo a partir del template HTML
    email_body = render_to_string('account/email/activation_account_email.html', context)
    
    # Configura el correo electrónico como HTML
    email = EmailMessage(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.content_subtype = 'html'  # Indica que el contenido es HTML

    try:
        # Envía el correo
        email.send()
    except Exception as e:
        #  excepción que pueda ocurrir al enviar el correo
        print(f"Error al enviar el correo: {e}")
    

def reject_email_rendered(user, motivo):
    # Renderiza el correo de rechazo con el nombre y apellidos del usuario y el motivo
    email_subject = 'Problema de Cuenta en BarrioLink'
    
    # Pasa nombres, apellidos y motivo al contexto del template
    context = {'user': user, 'nombres': user.nombres, 'apellidos': user.apellidos, 'motivo': motivo}
    
    # Renderiza el cuerpo del correo a partir del template HTML
    email_body = render_to_string('account/email/rejection_account_email.html', context)
    
    # Configura el correo electrónico como HTML
    email = EmailMessage(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.content_subtype = 'html'  # Indica que el contenido es HTML

    try:
        # Envía el correo
        email.send()
    except Exception as e:
        # Maneja cualquier excepción que pueda ocurrir al enviar el correo
        print(f"Error al enviar el correo: {e}")
        
        
        
def send_validation_account_email(user):
    # Asunto del correo electrónico
    email_subject = 'Activación de Cuenta en BarrioLink'

    # Variables para pasar al contexto del template
    context = {'user': user, 'nombres': user.nombres, 'apellidos': user.apellidos}

    # Renderiza el cuerpo del correo desde el template HTML
    email_body = render_to_string('account/email/email_account_Activation.html', context)

    # Configura el correo electrónico como HTML
    email = EmailMessage(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.content_subtype = 'html'  # Indica que el contenido es HTML

    try:
        # Envía el correo
        email.send()
        return True  # Éxito al enviar el correo
    except Exception as e:
        # Manejo de excepciones en caso de error al enviar el correo
        print(f"Error al enviar el correo: {e}")
        return False  # Fracaso al enviar el correo