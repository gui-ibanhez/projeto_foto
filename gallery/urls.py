from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.store_list, name='store_list'),
    path('loja/<uuid:pk>/', views.store_detail, name='store_detail'),
]


