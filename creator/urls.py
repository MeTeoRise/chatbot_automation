from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='creator-home'),
    path('about/', views.about, name='creator-about'),
]