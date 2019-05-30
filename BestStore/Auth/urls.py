from django.urls import path
from .views import user_login, logout_view, register_user, verify_user_email, render_login_form, render_register_form

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('api/user/login/', user_login, name='user_login'),
    path('login/', render_login_form, name="loginform"),
    path('api/user/register/', register_user, name='register_post'),
    path('register/', render_register_form, name='registerform'),
    path('api/user/verify/<str:token>/', verify_user_email, name='user_verify'),
]
