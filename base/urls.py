from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_blogs, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('add/', views.createBlogpost, name = 'create'),
    path('blogpost/<str:pk>', views.singleBlogpost, name = 'blogpost'),
    path('update/<str:pk>', views.updateBlogpost, name = 'update'),
    path('delete/<str:pk>', views.delete, name = 'delete'),
]
