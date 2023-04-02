import json

from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from main_app.helpers.commonts import getMessage, check_email_exist
from main_app.models import CustomUser, Staff, Job, Applicant, JobType, Category, Employer, NotificationEmployer, \
    WIBAdmin, NotificationAdmin, NotificationStaff, CahierCharge


@login_required
@csrf_exempt
def Staff_apply_job(request, job_id):
    if request.method == 'POST':
        staff = Staff.objects.get(admin_id=request.user.id)
        job = Job.objects.get(id=job_id)
        applicant = Applicant()
        applicant.staff = staff
        applicant.job = job
        applicant.save()
        fp = getMessage("Success Apply For This Job", 200)
        return JsonResponse(fp)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)


@login_required
@csrf_exempt
def get_all_Applyjob(request):
    if request.method == 'GET':
        staff = Staff.objects.get(admin_id=request.user.id)
        apply_list = Applicant.objects.filter(staff=staff)
        total_apply = apply_list.count()
        total_job_finish = 0
        total_job_not_finish = 0
        json_data = []

        for apply in apply_list:
            job = Job.objects.get(id=apply.job.id)
            type_job = JobType.objects.get(id=job.type_job.id)
            categorie = Category.objects.get(id=job.category.id)
            cahier_charge = CahierCharge.objects.get(job=job)
            fs = FileSystemStorage()
            cahier_url = fs.url(cahier_charge.upload)

            if job.filled:
                total_job_finish += 1
            else:
                total_job_not_finish += 1
            data = {
                "statistics": {
                    "Total_applies": str(total_apply),
                    "Total_job_finish": str(total_job_finish),
                    "Total_job_not_finish": str(total_job_not_finish)
                },
                "id_applicant": str(apply.id),
                "Job": {
                    "id_job": str(job.id),
                    "title": str(job.title),
                    "description ": str(job.description),
                    "location": str(job.location),
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
                },
            }
            json_data.append(data)

        return JsonResponse(json_data, safe=False)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)


@login_required
def staff_notify_employer(request):
    employer = CustomUser.objects.filter(user_type=3)
    context = {
        'message': "Send Notifications To Employer",
        'allStaff': employer
    }
    return JsonResponse(context, safe=False)


@login_required
def staff_notify_admin(request):
    admins = CustomUser.objects.filter(user_type=1)
    context = {
        'message': "Send Notifications To Admin",
        'allEmployers': admins
    }
    return JsonResponse(context, safe=False)


@login_required
@csrf_exempt
def send_employer_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    employer = get_object_or_404(Employer, admin_id=id)
    try:
        notification = NotificationEmployer(employer=employer, message=message)
        notification.save()
        msg = getMessage("Sucessfully Send", 200)
        return JsonResponse(msg)
    except Exception as e:
        msg = getMessage(f"On Error Occured {str(e)}", 200)
        return JsonResponse(msg)


@login_required
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
def staff_fcmtoken(request):
    token = request.POST.get('token')
    try:
        staff_user = get_object_or_404(CustomUser, id=request.user.id)
        staff_user.fcm_token = token
        staff_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@login_required
def staff_view_notification(request):
    staff = get_object_or_404(Staff, admin=request.user)
    notifications = NotificationStaff.objects.filter(staff=staff)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return JsonResponse(context, safe=False)
