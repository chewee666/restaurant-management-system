from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('confirm/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
]
