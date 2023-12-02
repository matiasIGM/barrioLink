from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
     path('login/', views.user_login, name='login'),
     path('logout/', views.logout_view, name='logout'),
     path('', views.home, name='homepage'),
     path('signup/', views.signup, name='signup'),  # Ruta con un parámetro 'step'
     path('adm/users_admin.html', views.users_admin_view, name='users_admin'),
     path('reserva/', views.reservation, name='reserva'),
     path('profile/', views.profileUser, name='profile'),
     
     path('userProfileConfig/', views.userProfileConfig, name='user_profile_config'),
     path('userUpdateProfile/<int:user_id>/', views.editUserConfig, name='user_profile_update'),
     path('userUpdateProfile/', views.userProfileUpdate, name='user_update_profile'),
     
     path('adminProfileConfig/', views.adminProfileConfig, name='admin_profile_config'),
     path('adminUpdateProfile/<int:user_id>/', views.editAdmConfig, name='admprofile_update'),
     path('adminEditProfile/<int:user_id>/', views.adminProfileUpdate, name='admconfig_edit'),

     
     path('userNews/', views.newsPublish, name='users_news'),
     path('userProfile/', views.userProfile, name='user_profile'),
     path('adminProfileConfig/', views.adminProfileConfig, name='user_profile_config'),
     path('userReservation/', views.userReservation, name='user_reservation'),
     path('adminPublish/', views.adminPublish, name='admin_publish'),
     path('adminNewsValidation/', views.adminPublishValidation, name='admin_publish_validation'),
     path('adminNotifications/', views.adminNotifications, name='admin_notifications'),
     path('adminProfile/', views.adminProfile, name='admin_profile'),
     path('adminUserList/', views.adminUserList, name='users_list'),
     
     path('adminUserValidation/', views.def_validation_view, name='users_validation'),
     path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
     path('denegar_usuario/', views.denegar_usuario, name='denegar_usuario'),
     
     path('adminReservations/', views.adminValidateReservations, name='admin_reservations'),
     path('placesConfig/', views.adminConfigPlaces, name='admin_places'),
     path('placesConfig/deletePlace/<id>', views.deletePlace,  name='delete_places'),
      path('create_space/', views.create_community_space, name='create_community_space'),
     path('placesConfig/updatePlace/<id>', views.deletePlace,  name='update_places'),

     #Mantenedores configuración junta de vecinos
     path('hoaConfig/', views.hoaConfig, name='admin_hoa'),
     path('edit-hoa-config/<int:hoa_id>/', views.editHoaConfig, name='edit_hoa_data'),
     path('update-hoa-config/<int:hoa_id>/', views.updateHoaConfig, name='update_hoa_data'),

     path('password_reset/', auth_view.PasswordResetView.as_view(template_name="account/users/password_reset.html"),
           name='password_reset'),
     path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name="account/users/password_reset_done.html"),
            name='password_reset_done'),
     path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="account/users/password_reset_confirm.html"),
           name='password_reset_confirm'),
     path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name="account/users/password_reset_complete.html"),
           name='password_reset_complete'),
      
      
     path('admValpublish/', views.validationoticias, name='news_validation'), # URL para el formulario validacion publicaciones
     path('solnoticiasuser/', views.solnoticias, name='news_publish'), # solicitud user noticia
     path('crearsolicitud/', views.crearsolicitud, name='news_publish'),
     path('cambiar_estado/<int:solicitud_id>/<str:nuevo_estado>/', views.cambiar_estado, name='cambiar_estado'),
     path('recuperar_solicitud/<int:solicitud_id>/', views.recuperar_solicitud, name='recuperar_solicitud'),
     path('public_val/<int:solicitud_id>', views.public_val, name='public_val'),
     path('detalle/<int:pk>/', views.detalle_publicacion, name='detalle_publicacion'),

    path('cargar-regiones/', views.cargar_regiones, name='cargar_regiones'),
    path('cargar-comunas/<int:region_id>/', views.cargar_comunas, name='cargar_comunas'),
 
    path('edit-space/<int:space_id>/', views.editCommunitySpace, name='edit_space'),
    path('update-space/<int:space_id>/', views.updateCommunitySpace, name='update_space'),
    
    path('email/', views.view_email, name='email'),
    path('enviar_correo/', views.enviar_correo, name='enviar_correo'),
    
#     path('cargar-datos/', views.cargar_datos, name='cargar_datos'),
    

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
