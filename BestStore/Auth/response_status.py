from django.http import JsonResponse


def register_json_response(success, message):
    """
    Tells if user was registered or not
    :param success: Boolean
    :param message: String Message
    :return:
    """
    obj = {'success': success, 'message': message}
    return JsonResponse(obj)


def login_json_response(success, login_status):
    """
    Tells if a user is logged in or not
    :param success: Boolean
    :param login_status:  status
    :return: Json response
    """
    messages = {'Logged In': None, 0: False, 1: True}
    exists = messages[login_status]
    return JsonResponse({'success': success, 'exists': exists})