from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    
     path('login/', views.user_login, name='login'),
     path('', views.home, name='homepage'),
     path('signup/', views.signup, name='signup'),  # Ruta con un parámetro 'step'
     path('adm/users_admin.html', views.users_admin_view, name='users_admin'),
     path('reserva/', views.reservation, name='reserva'),
     path('profile/', views.profileUser, name='profile'),
     path('userProfileConfig/', views.userProfileConfig, name='user_profile_config'),
     
     path('Admindocuments/', views.adminDocuments, name='documents'),
     path('documents/', views.userDocuments, name='documents'),
     
     
     path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
     path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
     
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
     path('adminReservations/', views.adminValidateReservations, name='admin_reservations'),
     path('placesConfig/', views.adminConfigPlaces, name='admin_places'),
     path('placesConfig/deletePlace/<id>', views.deletePlace,  name='delete_places'),
     path('placesConfig/register/', views.registerPlace, name='register_place'),
     path('placesConfig/updatePlace/<id>', views.deletePlace,  name='update_places'),
     path('placesConfig/update/<int:id>/', views.updatePlace, name='update_place'),

      path('password_reset/', auth_view.PasswordResetView.as_view(template_name="users/password_reset.html"),
           name='password_reset'),
      path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
            name='password_reset_done'),
      path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
           name='password_reset_confirm'),
      path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
           name='password_reset_complete'),
      
      
     path('adm/users_admin.html', views.users_admin_view, name='users_admin'),
     path('admNewspublish/', views.publicacion, name='news_publish'), # URL para el formulario publicaciones
     path('admValpublish/', views.validationoticias, name='news_validation'), # URL para el formulario validacion publicaciones
     path('solnoticiasuser/', views.solnoticias, name='news_publish'), # solicitud user noticia

]
