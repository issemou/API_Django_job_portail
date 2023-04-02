from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from main_app.helpers.CheckEmail import EmailBackend
from main_app.helpers.commonts import getUserLoged, getMessage
from main_app.models import Category, JobType


def logout_user(request):
    if request.user is not None:
        logout(request)
        result = {"code": 200, "message": "success"}
    return JsonResponse(result)


@csrf_exempt
def doLogin(request, **kwargs):
    if request.method != 'GET':
        fp = getMessage(f"Denied", 404)
        return JsonResponse(fp)
    else:

        email = request.GET.get('email')
        password = request.GET.get('password')
        # Authenticate
        user = EmailBackend.authenticate(request, username=email,
                                         password=password)
        if user is not None:
            login(request, user)
            if user.user_type == '1':
                fp = getUserLoged(user)
                return JsonResponse(fp)
            elif user.user_type == '2':
                fp = getUserLoged(user)
                return JsonResponse(fp)
            else:
                fp = getUserLoged(user)
                return JsonResponse(fp)
        else:
            fp = getMessage(f"Invalid details Or Not User found", 500)
            return JsonResponse(fp)


@login_required
@csrf_exempt
def get_category_by_id(request, category_id):
    if request.method == 'GET':
        try:
            cat = Category.objects.get(id=category_id)
            data = {
                "title": cat.title,
                "description": cat.description
            }
            msg = getMessage("Successfully Gets category", 200, data=data)
            return JsonResponse(msg)
        except Exception as ex:
            msg = getMessage("Can't Edite type " + str(ex), 500)
            print(ex)
            return JsonResponse(msg)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)


@login_required
@csrf_exempt
def get_all_category(request):
    if request.method == 'GET':
        try:
            cat_list = Category.objects.all()
            json_data = []
            for cat in cat_list:
                data = {
                    "id": cat.id,
                    "title": cat.title,
                    "description": cat.description
                }
                json_data.append(data)
            return JsonResponse(json_data, safe=False)

        except Exception as ex:
            msg = getMessage("Can't Edite type " + str(ex), 500)
            print(ex)
            return JsonResponse(msg)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)


@login_required
@csrf_exempt
def get_type_job_by_id(request, type_job_id):
    if request.method == 'GET':
        try:
            type_job = JobType.objects.get(id=type_job_id)
            data = {
                "label": type_job.title,
            }
            msg = getMessage("Successfully Gets category", 200, data=data)
            return JsonResponse(msg)
        except Exception as ex:
            msg = getMessage("Can't Edite type " + str(ex), 500)
            print(ex)
            return JsonResponse(msg)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)


@login_required
@csrf_exempt
def get_all_type_job(request):
    if request.method == 'GET':
        try:
            type_jobs = JobType.objects.all()
            json_data = []
            for type_j in type_jobs:
                data = {
                    "id": type_j.id,
                    "label": type_j.label,
                }
                json_data.append(data)
            return JsonResponse(json_data, safe=False)
        except Exception as ex:
            msg = getMessage("Can't Edite type " + str(ex), 500)
            print(ex)
            return JsonResponse(msg)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)
