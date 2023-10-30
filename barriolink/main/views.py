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

# Vista protegida por @login_required, que redirige a la página de inicio de sesión si el usuario no está autenticado.
# @login_required(login_url="/login")
# def home(request):
#     posts = Post.objects.all()
#     # Obtiene todos los objetos Post de la base de datos.
#     if request.method == "POST":
#         post_id = request.POST.get("post-id")
#         user_id = request.POST.get("user-id")

#         if post_id:
#             post = Post.objects.filter(id=post_id).first()
#             # Verificar si el usuario es el autor del post o tiene permiso para eliminar
#             if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
#                 post.delete()
#         elif user_id:
#             user = CustomUser.objects.filter(id=user_id).first()
#             # Verificar si el usuario actual es un administrador para eliminar usuarios
#             if user and request.user.is_staff:
#                 try:
#                     group = Group.objects.get(name='default')
#                     group.user_set.remove(user)
#                 except:
#                     pass

#                 try:
#                     group = Group.objects.get(name='mod')
#                     group.user_set.remove(user)
#                 except:
#                     pass
#     # Renderiza la página 'profile.html' y pasa los objetos 'posts' a la plantilla.                
#     return render(request, 'profile/profile.html', {"posts": posts})



# Vista protegida por @login_required y @permission_required, que redirige a la página de inicio de sesión
# si el usuario no está autenticado o no tiene el permiso necesario.
# @login_required(login_url="/login")
# @permission_required("main.add_post", login_url="/login", raise_exception=True)
# def create_post(request):
#     # Si la solicitud es una POST (envío del formulario), crea una instancia del formulario PostForm con los datos proporcionados.
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             # Si el formulario es válido, guarda el objeto Post en la base de datos.
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             # Redirige al usuario a la página de perfil después de crear el post.
#             return redirect("/profile/profile")
#     else:
#         form = PostForm()
#     # Renderiza la página 'profile.html' y pasa el formulario 'form' a la plantilla.
#     return render(request, 'profile/profile.html', {"form": form})

@login_required(login_url="/login")
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
            error_message = "Credenciales inválidas. Por favor, inténtalo de nuevo."
            return render(request, 'registration/login.html', {'error_message': error_message})
    return render(request, 'registration/login.html')




def users_admin_view(request):
    # Lógica de tu vista
    return render(request, 'adm/users_admin.html')



#Función Registro de usuario
# def sign_up(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             # Guardar el nuevo usuario en la base de datos
#             user = form.save()

#              # Obtén o crea el grupo "default"
#             group, created = Group.objects.get_or_create(name='default')

#             # Agrega el usuario al grupo(pendiente)
#             login(request, user)
#             return redirect(reverse('login'))  # Redirigir al usuario a la página de inicio de sesión
#     else:
#         form = RegisterForm()
#      # Renderizar la página de registro con el formulario (ya sea el formulario vacío o con errores)
#     return render(request, 'registration/sign_up.html', {"form": form})

# def sign_up(request):
#     if request.method == 'POST':
#         form = RegisterFormStep1(request.POST)
#         if form.is_valid():
#             request.session['registro_primer_paso'] = form.cleaned_data
#             return redirect('registro_segundo_paso')
#     else:
#         form = RegisterFormStep1()
#     return render(request, 'registration/sign_up.html', {'form': form})
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

# def sign_up_2(request):
#     datos_primer_paso = request.session.get('registro_primer_paso', {})
#     form = RegisterForm2(request.POST)

#     if request.method == 'POST':
#         form = RegisterForm2(request.POST)
#         if form.is_valid():
#             datos_segundo_paso = form.cleaned_data
#             datos_primer_paso.update(datos_segundo_paso)
#             email = form.cleaned_data['email']

#             # Registrar un mensaje en la consola para verificar los datos antes de guardarlos
#             logger.info(f"Datos a registrar: {datos_primer_paso}")
        
#             user, created = CustomUser.objects.get_or_create(email=email, defaults=datos_primer_paso)

#             if created:
#                 user.save()  # Guardar el nuevo usuario solo si se crea
#                 del request.session['registration/sign_up.html']
#                 return redirect('login')
#             else:
#                 # Mostrar un mensaje de error al usuario indicando que el correo electrónico ya está en uso
#                 form.add_error('email', 'Este correo electrónico ya está registrado.')
#         else:
#             # Registrar un mensaje en la consola para verificar los datos si hay errores en el formulario
#             logger.warning(f"Datos inválidos: {form.errors}")

#     else:
#         form = RegisterForm2()

#     return render(request, 'registration/sign_up_step_2.html', {
#         'form': form,
#         'nombre_completo': f"{datos_primer_paso.get('nombres', '')} {datos_primer_paso.get('apellidos', '')}",
#         'rut': datos_primer_paso.get('rut', '')
#     })
    
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



def filter_user_adm(request):
    usuarios = CustomUser.objects.all(is_hoa_admin=False)
    
    for usuario in usuarios:
        print(f"Usuario: {usuario.username}, Nombres: {usuario.nombres}, Apellidos: {usuario.apellidos}, Email: {usuario.email}")
    
    context = {'usuarios': usuarios}
    return render(request, 'adm/users_admin.html', context)



def certificado(request):
    return('ruta certificado/certificado.html')