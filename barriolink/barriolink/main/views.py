from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import Post, CustomUser  # Importar el modelo de usuario personalizado
from django.urls import reverse

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
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo usuario en la base de datos
            user = form.save()

             # Obtén o crea el grupo "default"
            group, created = Group.objects.get_or_create(name='default')

            # Agrega el usuario al grupo(pendiente)
            login(request, user)
            return redirect(reverse('login'))  # Redirigir al usuario a la página de inicio de sesión
    else:
        form = RegisterForm()
     # Renderizar la página de registro con el formulario (ya sea el formulario vacío o con errores)
    return render(request, 'registration/sign_up.html', {"form": form})