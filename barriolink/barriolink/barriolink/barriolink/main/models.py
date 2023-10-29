from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):# Define una clase CustomUser que extiende AbstractUser
    rut = models.CharField(max_length=20)  # Agregar campo Rut como string
    birth_date = models.DateField(blank=True, null=True)  # Agregar campo de fecha de nacimiento
    celular = models.CharField(max_length=10)  # Agregar campo de celular
    nombres = models.CharField(max_length=255)  # Agregar campo de nombres
    apellidos = models.CharField(max_length=255)  # Agregar campo de apellidos

    # Reemplaza el campo de inicio de sesión "username" por "email"
    email = models.EmailField(unique=True) # Agrega un campo de correo electrónico único para iniciar sesión
    username = models.CharField(max_length=30, unique=False)   # Cambia el campo de "username" para que no sea requerido ni único

    # Agrega related_name para resolver la colisión
    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')

    def __str__(self):
        return self.username

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "\n" + self.description