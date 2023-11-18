from django.contrib import admin
from django.urls import path, include
from certificates import views
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('django.contrib.auth.urls')),
    path('Admindocuments/', views.adminDocuments, name='documents'),
    path('documents/', views.userDocuments, name='documents'),
    
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
     
    path('Admindocuments/', views.adminDocuments, name='documents'),
    path('documents/', views.userDocuments, name='documents'),
    path('validador/', views.validator, name='document_valitador'),
     

]
