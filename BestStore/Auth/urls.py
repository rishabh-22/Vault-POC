from django.urls import path
from .views import user_login
from .views import logout_view
from .views import register_user
from .views import verify_user_email
from .views import render_login_form
from .views import render_register_form

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('api/user/login/', user_login, name='user_login'),
    path('login/', render_login_form, name="loginform"),
    path('api/user/register/', register_user, name='register_post'),
    path('register/', render_register_form, name='registerform'),
    path('api/user/verify/<str:token>/', verify_user_email, name='user_verify'),
]
