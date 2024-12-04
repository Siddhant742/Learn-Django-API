from django.urls import path
from .views import login_view, userlogout, index, verify_user_id_images, verify_prescriptions, view_orders

app_name = 'backend'

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login_view'),
    path('logout/', userlogout, name='userlogout'),
    path('verify-user-id-images/', verify_user_id_images, name='verify_user_id_images'),
    path('verify-prescriptions/', verify_prescriptions, name='verify_prescriptions'),
    path('view-orders/', view_orders, name='view_orders'),
]