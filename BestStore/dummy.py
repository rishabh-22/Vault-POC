from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from socket import gaierror


def test_user():
    try:
        send_mail('Best Store Account Confirmation',
                    "dfg",
                    'admin@thebeststore.com',
                    [1, 2],
                    html_message="fghjkl",
                    fail_silently=False)
    except Exception as e:
        print(e)
        import pdb;pdb.set_trace()
