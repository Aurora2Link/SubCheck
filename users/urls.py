from django.urls import path
from .views import check_subscription

urlpatterns = [
    path('api/check_subscription/', check_subscription, name='check_subscription'),
]
