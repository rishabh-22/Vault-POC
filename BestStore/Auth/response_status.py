from django.http import JsonResponse


def register_json_response(success, message):
    obj = {'success': success, 'message': message}
    return JsonResponse(obj)


def login_json_response(success, login_status):
    messages = {'Logged In': None, 0: False, 1: True}
    exists = messages[login_status]
    return JsonResponse({'success': success, 'exists': exists})