import json
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin


def render_login_form(request):
    return render(request, 'Auth/login.html')


def render_register_form(request):
    if request.user.is_anonymous:
        return render(request, "Auth/register.html")
    return redirect('/dashboard/')


def register_user(request):
    """This function will register a user"""
    if request.method == 'POST':
        body = json.loads(request.body)
        user_model_keys = ('username', 'first_name', 'last_name')
        user_dict = {key: body[key] for key in user_model_keys}
        user_dict.update({
            'password': make_password(body['password']), 
            'email': user_dict['username'],
            'is_active': False
        })
        try:
            new_user = User(**user_dict)
            new_user.save()
            token = new_user.password.replace('/', '*')
            url = f"http://127.0.0.1:8000/api/user/verify/{token}/"
            name = f'{new_user.first_name} {new_user.last_name}'
            context = {'action': 'Confirm Email', 'url': url, 'name': name}

            html_message = render_to_string('General/email.html', context)
            plain_message = strip_tags(html_message)
            send_mail('Best Store Account Confirmation',
                      plain_message,
                      'admin@thebeststore.com',
                      [new_user.email],
                      html_message=html_message,
                      fail_silently=False)

            json_res = {'success': True}
            return JsonResponse(json_res)
        except Exception:
            json_res = {'success': False, 'error': 'Email already in use.'}
            return JsonResponse(json_res)


def user_login(request):
    """This is a login function using Django's inbuilt login functionality"""
    body = json.loads(request.body)
    username, password = body['email'], body['password']
    cart = request.session.get('cart', False)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        name = user.first_name
        login(request, user)
        request.session['cart'] = cart

        json_res = {'success': True}
        return JsonResponse(json_res)
    elif len(User.objects.filter(username=username)):
        return JsonResponse({'success': False, 'exists': True})

    return JsonResponse({'success': False, 'exists': False})


def verify_user_email(request, token):
    """Confirming the user email"""
    user = User.objects.get(password=token.replace("*", "/"))
    if user is not None:
        user.is_active = True
        user.save()
        return redirect('/login/')
    else:
        raise Http404

        
def logout_view(request):
    """Logging off the user"""
    logout(request)
    return redirect("homepage")
