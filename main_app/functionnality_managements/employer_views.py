import json

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from main_app.helpers.commonts import getMessage
from main_app.models import CustomUser, Staff, NotificationStaff, WIBAdmin, NotificationEmployer, NotificationAdmin, \
    CahierCharge

from main_app.models import JobType, Category, Job, Employer



@csrf_exempt
def add_job(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            location = request.POST.get('location')
            type_job_id = request.POST.get('type_job_id')
            category_id = request.POST.get('category_id')
            livrable_date = request.POST.get('livrable_date')
            upload = request.FILES.get('cahier_upload')

            emp = Employer.objects.get(admin_id=request.user.id)
            type_job = JobType.objects.get(id=type_job_id)
            category = Category.objects.get(id=category_id)

            job = Job()
            job.employer = emp
            job.type_job = type_job
            job.category = category
            job.title = title
            job.description = description
            job.location = location
            job.livrable_date = livrable_date
            job.save()

            cahier = CahierCharge()
            cahier.upload = upload
            cahier.job = job
            cahier.save()

            msg = getMessage("Successfully Added", 201)
            return JsonResponse(msg)
        except Exception as ex:
            msg = getMessage("Can't add type " + str(ex), 500)
            print(ex)
            return JsonResponse(msg)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)


@csrf_exempt
def edite_job(request, job_id):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            location = request.POST.get('location')
            type_job_id = request.POST.get('type_job_id')
            category_id = request.POST.get('category_id')
            livrable_date = request.POST.get('livrable_date')
            upload = request.FILES.get('cahier_upload')

            emp = Employer.objects.get(admin_id=request.user.id)
            type_job = JobType.objects.get(id=type_job_id)
            category = Category.objects.get(id=category_id)

            job = get_object_or_404(Job, id=job_id)
            job.type_job = type_job
            job.category = category
            job.title = title
            job.description = description
            job.location = location
            job.livrable_date = livrable_date
            job.employer = emp
            job.save()

            cahier = CahierCharge.objects.get(job=job)

            if upload is not None:
                cahier.upload = upload

            cahier.job = job
            cahier.save()
            msg = getMessage("Successfully Edited", 201)
            return JsonResponse(msg)
        except Exception as ex:
            msg = getMessage("Can't Edite type " + str(ex), 500)
            print(ex)
            return JsonResponse(msg)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)



@csrf_exempt
def delete_job(request, job_id):
    if request.method == 'DELETE':
        job = Job.objects.get(id=job_id)
        job.delete()
        msg = getMessage("Successfully Deleted", 201)
        return JsonResponse(msg)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)



def employer_notify_staff(request):
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'message': "Send Notifications To Staff",
        'allStaff': staff
    }
    return JsonResponse(context, safe=False)



def employer_notify_admin(request):
    admins = CustomUser.objects.filter(user_type=1)
    context = {
        'message': "Send Notifications To Students",
        'allEmployers': admins
    }
    return JsonResponse(context, safe=False)



@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    staff = get_object_or_404(Staff, admin_id=id)
    try:
        notification = NotificationStaff(staff=staff, message=message)
        notification.save()
        msg = getMessage("Sucessfully Send", 200)
        return JsonResponse(msg)
    except Exception as e:
        msg = getMessage(f"On Error Occured {str(e)}", 200)
        return JsonResponse(msg)



@csrf_exempt
def send_admin_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    admin = get_object_or_404(WIBAdmin, admin_id=id)
    try:
        notification = NotificationAdmin(admin=admin, message=message)
        notification.save()
        msg = getMessage("Sucessfully Send", 200)
        return JsonResponse(msg)
    except Exception as e:
        msg = getMessage(f"On Error Occured {str(e)}", 200)
        return JsonResponse(msg)


@csrf_exempt
def employer_fcmtoken(request):
    token = request.POST.get('token')
    try:
        employer_user = get_object_or_404(CustomUser, id=request.user.id)
        employer_user.fcm_token = token
        employer_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")



def employer_view_notification(request):
    employer = get_object_or_404(Employer, admin=request.user)
    notifications = NotificationEmployer.objects.filter(employer=employer)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return JsonResponse(context, safe=False)


@csrf_exempt
def get_all_jobs(request):
    emp = Employer.objects.get(admin_id=request.user.id)
    job_list = Job.objects.filter(employer=emp)
    total_job = job_list.count()
    total_job_finished = job_list.filter(filled=True).count()
    total_job_not_finished = job_list.filter(filled=False).count()

    statistics = {
        "Total_jobs": str(total_job),
        "Total_jobs_finished": str(total_job_finished),
        "Total_jobs_not_finished": str(total_job_not_finished)
    }
    json_data = [
        {
            "stat": statistics
        }
    ]
    for job in job_list:
        type_job = JobType.objects.get(id=job.type_job.id)
        categorie = Category.objects.get(id=job.category.id)
        cahier_charge = CahierCharge.objects.get(job=job)
        fs = FileSystemStorage()
        cahier_url = fs.url(cahier_charge.upload)
        data = {
            "id": str(job.id),
            "title": str(job.title),
            "description ": str(job.description),
            "location": str(job.location),
            "livrable_date": str(job.livrable_date),
            "type_job": {
                "label": str(type_job.label)
            },
            "category": {
                "title": str(categorie.title),
                "description": str(categorie.description)
            },
            "filled": str(job.filled),
            "cahier_charge": {
                'url': str(cahier_url),
                'isValidated': str(cahier_charge.isValidated)
            }
        }
        json_data.append(data)
    return JsonResponse(json_data, safe=False)
