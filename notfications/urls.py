#create urls.py in the notifications app
from django.urls import path
from views import NotificationViewSet



urlpatterns = [
    path('notifications/', NotificationViewSet.as_view(), name='notification_list'),
]