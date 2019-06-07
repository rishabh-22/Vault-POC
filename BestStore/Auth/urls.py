from django.urls import path
from .views import user_login, logout_view, register_user, verify_user_email, render_login_form, render_register_form, social_login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('api/user/login/', user_login, name='user_login'),
    path('login/', render_login_form, name="loginform"),
    path('api/user/register/', register_user, name='register_post'),
    path('register/', render_register_form, name='registerform'),
    path('api/user/verify/<str:token>/', verify_user_email, name='user_verify'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='Auth/password_reset.html',
        html_email_template_name="Auth/email_reset_template.html",
        subject_template_name="Auth/password_reset_subject.txt"),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='Auth/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='Auth/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='Auth/password_reset_complete.html'),
         name='password_reset_complete'),
    path('social_login/', social_login, name='social_login'),
]
