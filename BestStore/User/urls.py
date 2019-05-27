from django.urls import path
from .views import user_dashboard, UpdateUserProfile, DeleteUserProfile

urlpatterns = [
    path('dashboard/', user_dashboard, name='dashboard'),
    path('profile_delete/<int:pk>/', DeleteUserProfile.as_view(), name='delete_profile'),
    path('profile_update/<int:pk>/', UpdateUserProfile.as_view(success_url='/dashboard/'),
         name='update_profile'),
]
