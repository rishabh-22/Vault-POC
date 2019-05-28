import json
from socket import gaierror
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from BestStore.settings import USER_REGISTER_KEYS, VERIFY_EMAIL_URL, DUMMY_EMAIL, EMAIL_SUBJECT
from django.db.utils import IntegrityError
from .response_status import register_json_response, login_json_response


def render_login_form(request):
    """
    Renders the login block to be included in the base template
    :param request: Django's HTTP Request object
    :return: Rendered login block to base template
    """
    return render(request, 'Auth/login.html')


def render_register_form(request):
    """
    If user not logged in render register block else redirect to the dashboard url
    :param request: Django's HTTP Request object
    :return: Rendered register block to base template or django redirect object to dashboard
    """
    if request.user.is_anonymous:
        return render(request, "Auth/register.html")
    return redirect('/dashboard/')


def register_user(request):
    """
        This function will register a user
       :param request: Django's HTTP Request object
       :return: A success or failure message
    """
    if request.method == 'POST':
        # Initialize variables to use in determining what json response to send
        success, message = False, ''
        body = json.loads(request.body)
        # Extract relevant user registration info for django user model instance creation
        user_dict = {key: body[key] for key in USER_REGISTER_KEYS}
        """
        Hash password for user equate email with username (for django's inbuilt forgot password) 
        and deactivate account until email is confirmed by user
        """
        user_dict.update({
            'password': make_password(body['password']), 
            'email': user_dict['username'],
            'is_active': False
        })
        try:
            # Create a new user object and save, except an Integrity error if already in use
            new_user = User(**user_dict)
            new_user.save()
            # Create a token and append to verify email link to send to new user for confirmation
            token = new_user.password.replace('/', '*')
            url = f"{VERIFY_EMAIL_URL}/{token}/"
            # Set context for email template to be sent
            name = f'{new_user.first_name} {new_user.last_name}'
            context = {'action': 'Confirm Email', 'url': url, 'name': name}
            # Prepare HTML template to be sent in the Email
            html_message = render_to_string('General/email.html', context)
            # Plain message is shown in email in case HTML template does't render for user email host
            plain_message = strip_tags(html_message)
            send_mail(EMAIL_SUBJECT,
                      plain_message,
                      DUMMY_EMAIL,
                      [new_user.email],
                      html_message=html_message,
                      fail_silently=False)
            # parameter to determine json response is set
            success = True
        except IntegrityError:
            # Catches case where username is already in use
            message = "Email already in use!"
        except gaierror:
            #  Catches case where internet connection is down
            message = "Check your internet connection!"
        # return a json response with appropriate parameters
        return register_json_response(success, message)


def user_login(request):
    """
      This is a login function using Django's inbuilt login functionality
      :param request: Django's HTTP Request object
      :return: Success message or failure message in JSON format
    """
    # Initialize variables to use in determining what json response to send
    success = False
    # Grab username and password fields from JSON request body
    body = json.loads(request.body)
    username, password = body['email'], body['password']
    # Session is reset after login so we assign the cart variable in session so it persists
    cart = request.session.get('cart', dict())
    # Authenticate user by using the inbuilt Django's functionality
    user = authenticate(request, username=username, password=password)
    # For checking if user exists but has not confirmed their email
    status = len(User.objects.filter(username=username))
    # If user exist it will log them in
    if user is not None:
        login(request, user)
        # Reassign the session variable after login
        request.session['cart'] = cart
        # Set success to true and exists param to indicate user logged in to send in the json response
        success = True
        status = 'Logged In'
    # Return json response appropriate to the result of the login attempt
    return login_json_response(success, status)


def verify_user_email(request, token):
    """
        Confirming the user email
        :param request, token: Django's HTTP Request object, Token to verify user
        :return: Redirect to Login or Raise 404
    """
    # Parse user hashed password from URL to query against user model
    user = User.objects.get(password=token.replace("*", "/"))
    # If a user is found then this will activate the account and redirect to login page
    if user is not None:
        user.is_active = True
        user.save()
        return redirect('/login/')
    # If a user is not found then token from url is invalid and the link points to nothing
    else:
        return Http404()

        
def logout_view(request):
    """Logging off the user
       :param request: Django's HTTP Request object
       :return: Redirect to homepage
    """
    logout(request)
    return redirect("homepage")
