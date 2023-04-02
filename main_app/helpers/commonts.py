import json

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import JsonResponse

from main_app.models import CustomUser


def getMessage(message, statut, data=None):
    if statut == 200:
        data = {
            "message": message,
            "code": 200,
            "data": data
        }
        return data

    if statut == 201:
        data = {
            "message": message,
            "code": 201,
            "data": data
        }
        return data

    if statut == 500:
        data = {
            "message": message,
            "code": 500,
            "data": data
        }
        return data

    if statut == 404:
        data = {
            "message": message,
            "code": 404,
            "data": data
        }
        return data


def getUserLoged(user):
    if user is not None:
        fs = FileSystemStorage()
        profile_url = fs.url(user.profile_pic)
        data = {
            "message": "Success Request",
            "code": 200,
            "data": [
                {
                    "id": user.id,
                    "type": user.user_type,
                    "email": user.email,
                    "profile_picture": profile_url
                }
            ]
        }
        return data
    else:
        data = {
            "message": "Error none",
            "code": 500,
            "data": None
        }
        return data


def decobeBodyRequest(request):
    data = json.loads(request.body.decode('utf-8'))
    return data


def check_email_exist(email):
    user_obj = CustomUser.objects.filter(email=email)
    if user_obj:
        return True
    else:
        return False
