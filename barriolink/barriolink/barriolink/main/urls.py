from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.urls import path
from .views import TelegramWebhook


urlpatterns = [
      path('', views.home, name='home'),
      path('home', views.home, name='home'),
      path('sign-up', views.sign_up, name='sign_up'),
      path('registro_segundo_paso/', views.sign_up_2, name='registro_segundo_paso'),
      path('create-post', views.create_post, name='create_post'),
      path('password_reset/', auth_view.PasswordResetView.as_view(template_name="users/password_reset.html"),
           name='password_reset'),
      path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
            name='password_reset_done'),
      path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
           name='password_reset_confirm'),
      path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
           name='password_reset_complete'),
     path('telegram_webhook/', TelegramWebhook.as_view(), name='telegram_webhook'),
]
