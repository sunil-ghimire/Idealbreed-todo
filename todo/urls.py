from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<str:id>/', views.delete, name='delete'),
    path('update/<str:pk>/', views.update, name='update'),
]
