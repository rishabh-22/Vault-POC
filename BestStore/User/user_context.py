from django.contrib.auth.models import User


def add_user_firstname(request):
    """Adds the value of the user firstname"""
    firstname = ''
    if not request.user.is_anonymous:
        firstname = request.user.first_name

    return {'firstname': firstname}
