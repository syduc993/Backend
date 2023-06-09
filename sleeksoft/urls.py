"""th URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# from Data_Interaction.admin import admin_site
from django.urls import path

from social import views
from rest_framework.routers import DefaultRouter,SimpleRouter
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from django.urls import re_path as url 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-my-zip-file',views.get_my_zip_file),
    path('get-my-zip-file-product',views.get_my_zip_file_product),
    path('get_file_calendar',views.get_file_calendar),
    path('get-file-sortqc',views.get_file_sortqc),
    path('delete-my-zip-file',views.delete_my_zip_file),
    path('delete-my-zip-file-product',views.delete_my_zip_file_product),
    path('delete-file-calendar',views.delete_file_calendar),
    path('delete-file-sortqc',views.delete_file_sortqc),
    
    # path('add-data-file',views.add_data_file),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
