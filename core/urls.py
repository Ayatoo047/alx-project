from django.urls import path, include
from django.contrib import admin
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("core_login/", views.core_login, name='core_login'),
    path("core_logout/", views.logoutUser, name='core_logout'),
    path('', views.index, name='index'),
    path('create_instance', views.createInstance, name='createinstance'),
    path('admin-dashboard', views.adminDash, name='admindash'),
]