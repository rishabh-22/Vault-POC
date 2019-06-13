from django.urls import path
from .views import user_dashboard, UpdateUserProfile, DeleteUserProfile, contact_us, change_password, privacy, tnc, \
    settings, add_address, view_address, delete_address

urlpatterns = [
    path('dashboard/', user_dashboard, name='dashboard'),
    path('profile/delete/<int:pk>/', DeleteUserProfile.as_view(), name='delete_profile'),
    path('profile/update/<int:pk>/', UpdateUserProfile.as_view(success_url='/dashboard/'),
         name='update_profile'),
    path('contact/', contact_us, name='contact'),
    path('change_password/', change_password, name='change_password'),
    path('privacy-policy/', privacy, name='privacy_policy'),
    path('terms-conditions/', tnc, name='terms_conditions'),
    path('settings/ ', settings, name='settings'),
    path('add-address/', add_address, name='add_address'),
    path('user-address', view_address, name='user_addresses'),
    path('user-address-delete/<int:pk>/', delete_address, name='delete_address'),
]
