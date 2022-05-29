"""face_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from face import views
from django.conf import settings 
from django.conf.urls.static import static
from face.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from face_django_project.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base, name='base'),
    path('create_record/', views.create_record, name='create_record'),
    path('view/', views.view, name='view'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('<int:id>', views.edit, name='edit'),
    path('search/', views.search,name='search'),
    path('face_rec/', views.face_rec, name='face_rec'),
    path('face_recognition_cam/', views.face_recognition_cam, name='face_recognition_cam'),
    path('face_recognition_img/', views.face_recognition_img, name='face_recognition_img'),
    path('face_recognition_video/', views.face_recognition_video, name='face_recognition_video'),
    path('view_search_criminal/', views.view_of_search, name='view_of_search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()