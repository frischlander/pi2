from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='caaordserv'),
    path('add-ordem/', views.add_ordem, name='add_ordem'),
]