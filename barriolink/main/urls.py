from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    
     path('login/', views.user_login, name='login'),
     path('', views.home, name='homepage'),
     path('signup/<str:step>/', views.signup, name='signup'),  # Ruta con un parámetro 'step'
     path('adm/users_admin.html', views.users_admin_view, name='users_admin'),
     path('reserva/', views.reservation, name='reserva'),
     path('profile/', views.profileUser, name='profile'),


     

      path('password_reset/', auth_view.PasswordResetView.as_view(template_name="users/password_reset.html"),
           name='password_reset'),
      path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
            name='password_reset_done'),
      path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
           name='password_reset_confirm'),
      path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
           name='password_reset_complete'),

]
