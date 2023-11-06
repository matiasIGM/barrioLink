from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.urls import path

urlpatterns = [
    
     path('login/', views.user_login, name='login'),
     path('', views.home, name='homepage'),
     path('signup/<str:step>/', views.signup, name='signup'),  # Ruta con un parámetro 'step'
     path('adm/users_admin.html', views.users_admin_view, name='users_admin'),
     path('reserva/', views.reservation, name='reserva'),
     path('profile/', views.profileUser, name='profile'),
     path('userProfileConfig/', views.userProfileConfig, name='user_profile_config'),
     path('documents/', views.userDocuments, name='documents'),
     path('userNews/', views.newsPublish, name='users_news'),
     path('userProfile/', views.userProfile, name='user_profile'),
     path('adminProfileConfig/', views.adminProfileConfig, name='user_profile_config'),
     path('userReservation/', views.userReservation, name='user_reservation'),
     path('adminPublish/', views.adminPublish, name='admin_publish'),
     path('adminNewsValidation/', views.adminPublishValidation, name='admin_publish_validation'),
     path('adminNotifications/', views.adminNotifications, name='admin_notifications'),
     path('adminProfile/', views.adminProfile, name='admin_profile'),
     path('adminUserList/', views.adminUserList, name='users_list'),
     path('adminUserValidation/', views.adminUserValidation, name='users_validation'),
     path('adminReservations/', views.adminValidateReservations, name='admin_reservations'),
     path('placesConfig/', views.adminConfigPlaces, name='admin_places'),

      path('password_reset/', auth_view.PasswordResetView.as_view(template_name="users/password_reset.html"),
           name='password_reset'),
      path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
            name='password_reset_done'),
      path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
           name='password_reset_confirm'),
      path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
           name='password_reset_complete'),
      path('adm/users_admin.html', views.users_admin_view, name='users_admin'),
      path('crear-informacion/', views.crear_informacion, name='crear_informacion'),
]
