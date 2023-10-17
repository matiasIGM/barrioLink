from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm, RegisterForm2, CustomUserAdminRegistrationForm, Post, JuntaDeVecinosForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import  CustomUser  # Importar el modelo de usuario personalizado
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding  import force_bytes
from django.utils.http import urlsafe_base64_encode

# Vista protegida por @login_required, que redirige a la página de inicio de sesión si el usuario no está autenticado.
@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()
    # Obtiene todos los objetos Post de la base de datos.
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            # Verificar si el usuario es el autor del post o tiene permiso para eliminar
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        elif user_id:
            user = CustomUser.objects.filter(id=user_id).first()
            # Verificar si el usuario actual es un administrador para eliminar usuarios
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass
    # Renderiza la página 'profile.html' y pasa los objetos 'posts' a la plantilla.                
    return render(request, 'profile/profile.html', {"posts": posts})



# Vista protegida por @login_required y @permission_required, que redirige a la página de inicio de sesión
# si el usuario no está autenticado o no tiene el permiso necesario.
@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    # Si la solicitud es una POST (envío del formulario), crea una instancia del formulario PostForm con los datos proporcionados.
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, guarda el objeto Post en la base de datos.
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # Redirige al usuario a la página de perfil después de crear el post.
            return redirect("/profile/profile")
    else:
        form = PostForm()
    # Renderiza la página 'profile.html' y pasa el formulario 'form' a la plantilla.
    return render(request, 'profile/profile.html', {"form": form})



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
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            request.session['registro_primer_paso'] = form.cleaned_data
            return redirect('registro_segundo_paso')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form})


def sign_up_2(request):
    if request.method == 'POST':
        form = RegisterForm2(request.POST)
        if form.is_valid():
            datos_primer_paso = request.session.get('registro_primer_paso', {})
            datos_segundo_paso = form.cleaned_data
            datos_primer_paso.update(datos_segundo_paso)
            user = CustomUser(**datos_primer_paso)
            user.save()
            del request.session['registro_primer_paso']
            return redirect('login')
    else:
        form = RegisterForm2()
    return render(request, 'registration/sign_up_step_2.html', {'form': form})

#Función para resetear contraseña de usuario
def password_reset_request(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = CustomUser.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = 'Restablecer tu contraseña'
                    email_template_name = 'users/password_message.txt' 
                    parameters = {
                        'email': user.email,
                        'domain': 'localhost:8000',
                        'site_name': 'BarrioLink',
                        'udi': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, parameters)
                    try:
                        send_mail(subject, email, '', [user.email], fail_silently=False)
                    except:
                        return HttpResponse('Invalid Header')
                return redirect('Password_reset_done')
    else:
        password_form = PasswordResetForm()

    context = {
        'password_form': password_form
    }
    return render(request, 'users/password_reset.html', context)




def register_hoa_admin(request):
    if request.method == 'POST':
        form = CustomUserAdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data["password"])
            user.is_hoa_admin = True  # Establece como administrador de juntas de vecinos
            user.save()
            return redirect("admin_dashboard")  # Redirige a la página de administración
    else:
        form = CustomUserAdminRegistrationForm()
    return render(request, 'registration/register_hoa_admin.html', {'form': form})

def register_junta_de_vecinos(request):
    if request.method == 'POST':
        form = JuntaDeVecinosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")  # Redirige a la página de administración
    else:
        form = JuntaDeVecinosForm()
    return render(request, 'registration/register_junta_de_vecinos.html', {'form': form})