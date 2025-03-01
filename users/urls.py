from django.urls import path
from . import views

urlpatterns = [
    path('check_subscription/', views.check_subscription, name='check_subscription'),
]
