from django.apps import AppConfig
from django.conf import settings



class MainConfig(AppConfig):
    # Configura el campo de autonumeración predeterminado para modelos
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        # Importa el modelo de Group y las señales de Django
        from django.contrib.auth.models import Group
        from django.db.models.signals import post_save
        from .models import CustomUser  # Importa  modelo CustomUser

        # Función para agregar usuarios al grupo "default" cuando se crea un usuario
        def add_to_default_group(sender, instance, created, **kwargs):
            if created:
                group, ok = Group.objects.get_or_create(name="default")
                ##(aqui pendiente asginacion de grupo a el usuario)
        # Conecta la función anterior al evento post_save del modelo AUTH_USER_MODEL
        post_save.connect(add_to_default_group, sender=CustomUser)