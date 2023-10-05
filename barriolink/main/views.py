from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import Post, CustomUser  # Importar el modelo de usuario personalizado
from django.urls import reverse


@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()

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

    return render(request, 'profile/profile.html', {"posts": posts})


@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/profile/profile")
    else:
        form = PostForm()

    return render(request, 'profile/profile.html', {"form": form})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

             # Obtén o crea el grupo "default"
            group, created = Group.objects.get_or_create(name='default')

            # Agrega el usuario al grupo(pendiente)
            

            login(request, user)
            return redirect(reverse('login'))  # Redirigir al usuario a la página de inicio de sesión
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})