from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from dataroom import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.index, name='index'),
    path('classification/<int:pk>/', views.classification_detail, name='classification_detail'),
    path('upload/', views.upload_file, name='upload_file'),
    path('file/<int:pk>/', views.file_detail, name='file_detail'),
    path('download/<int:pk>/', views.download_file, name='download_file'),
    path('download/consideration/<int:pk>/', views.download_consideration, name='download_consideration'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
