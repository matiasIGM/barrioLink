from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid
import hashlib

class CustomUser(AbstractUser):# Define una clase CustomUser que extiende AbstractUser
    rut = models.CharField(max_length=20)  # Agregar campo Rut como string
    birth_date = models.DateField(blank=True, null=True)  # Agregar campo de fecha de nacimiento
    celular = models.CharField(max_length=10)  # Agregar campo de celular
    nombres = models.CharField(max_length=255)  # Agregar campo de nombres
    apellidos = models.CharField(max_length=255)  # Agregar campo de apellidos

    #campos para la segunda parte del registro
    numero_documento = models.CharField(max_length=20, blank=True)
    region = models.CharField(max_length=100, blank=True)
    comuna = models.CharField(max_length=100, blank=True)
    calle = models.CharField(max_length=255, blank=True)
    numero_domicilio = models.CharField(max_length=20, blank=True)
    is_admin_general = models.BooleanField(default=False)
    is_hoa_admin = models.BooleanField(default=False)  # Nuevo campo para los administradores de juntas de vecinos

    # Reemplaza el campo de inicio de sesión "username" por "email"
    email = models.EmailField(unique=True) # Agrega un campo de correo electrónico único para iniciar sesión
    username = models.CharField(max_length=30, unique=False)   # Cambia el campo de "username" para que no sea requerido ni único
    is_active = models.BooleanField(default=False)  # Agrega el campo is_active con valor predeterminado False
    # Agrega related_name para resolver la colisión
    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')

    def __str__(self):
        return self.username
    

    def save(self, *args, **kwargs):
        # Establece is_active en False al crear un nuevo usuario
        
        if not self.id:  # Si es una instancia nueva (no tiene ID asignado)
            self.is_active = False
        super().save(*args, **kwargs)



class JuntaDeVecinos(models.Model):
    
    hoa_id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12, blank=True)
    hoa_name = models.CharField(max_length=70, blank=True)
    legal_address = models.CharField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    foundation_date = models.DateField(blank=True, null=True)
    legal_representative_name = models.CharField(max_length=255, blank=True)
    legal_representative_rut = models.CharField(max_length=12, blank=True)
    logo_symbol = models.ImageField(upload_to='uploads/logos/', blank=True)
    signature_img = models.ImageField(upload_to='uploads/signatures/', blank=True)

    
    def __str__(self):
        return self.hoa_name
    


#Modelo para guardar datos de generacion del certificado de residencia.
class ResidenceCertificate(models.Model):
    certificate_id = models.AutoField(primary_key=True)
    resident = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='residence_certificates_received')
    certificate_date = models.DateField()
    certificate_filename = models.CharField(max_length=255)
    certificate_status = models.CharField(max_length=50)
    hoa = models.ForeignKey(JuntaDeVecinos, on_delete=models.CASCADE)
    generated_by_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='residence_certificates_generated')
    verification_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    @staticmethod
    def uuid_to_short_id(uuid_str, num_digits=4):
        # Utiliza SHA-256 para generar un hash
        sha256_hash = hashlib.sha256(uuid_str.encode()).hexdigest()

        # Toma solo los primeros 'num_digits' dígitos del hash
        short_id = int(sha256_hash[:num_digits], 16)

        return short_id


    
    def save(self, *args, **kwargs):
        # generar un nuevo UUID cada vez que se guarda el objeto, incluso si no es nuevo
        if not self.verification_code:
            self.verification_code = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.verification_code)

class Resident(models.Model):
    resident_id = models.AutoField(primary_key=True)
    hoa = models.ForeignKey(JuntaDeVecinos, on_delete=models.CASCADE, default=4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, default=" ")


class CommunitySpace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    max_capacity = models.PositiveIntegerField(blank=True, null=True)

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    community_space = models.ForeignKey(CommunitySpace, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    reservation_status = models.CharField(max_length=20)

class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateField()
    publisher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message_content = models.TextField()
    send_date_time = models.DateTimeField()

    

#Modelo de Región
class Region(models.Model):
    nombre = models.CharField(max_length=255)
    region_iso_3166_2 = models.CharField(max_length=10)
    capital_regional = models.CharField(max_length=255)
    capital_regional2 = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

#Modelo de Provincia
class Provincia(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=10)
    capital_provincial = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

#Modelo de Comuna
class Comuna(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=10)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
# Este modelo representa una publicación de noticias con un título, contenido y fecha de publicación.
class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
    

class Crearsol(models.Model):
    ESTADO_CHOICES = [
        ('nueva', 'Nueva'),
        ('eliminada', 'Eliminada'),
    ]
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='nueva')
    fecha_publicacion = models.DateTimeField(auto_now_add=True) 
    contenido = models.TextField()
    usersol = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def formatted_fecha_publicacion(self):
        return self.fecha_publicacion.strftime("%d-%m-%Y %H:%M:%S")



class Noticia(models.Model):
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)