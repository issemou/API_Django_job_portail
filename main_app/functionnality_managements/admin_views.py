import json
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from main_app.helpers.commonts import getMessage
from main_app.models import CustomUser, JobType, Category, WIBAdmin, Applicant, Employer, Staff, NotificationStaff, \
    NotificationEmployer, NotificationAdmin, Job



@csrf_exempt
def add_type_job(request):
    if request.method == 'POST':
        try:
            admin = WIBAdmin.objects.get(admin_id=request.user.id)

            label = request.POST.get('label')
            type_job = JobType()
            type_job.label = label
            type_job.admin = admin
            type_job.save()
            msg = getMessage("Successfully Added", 201)
            return JsonResponse(msg)
        except Exception as ex:
            msg = getMessage("Can't add type " + str(ex), 500)
            print(ex)
            return JsonResponse(msg)



@csrf_exempt
def edite_type_job(request, type_job_id):
    if request.method == 'POST':
        try:
            admin = WIBAdmin.objects.get(admin_id=request.user.id)
            label = request.POST.get('label')

            type_job = JobType.objects.get(id=type_job_id)
            type_job.label = label
            type_job.admin = admin
            type_job.save()
            msg = getMessage("Successfully Edited", 201)
            return JsonResponse(msg)
        except Exception as ex:
            msg = getMessage("Can't Edite type " + str(ex), 500)
            print(ex)
            return JsonResponse(msg)



@csrf_exempt
def delete_type_job(request, type_job_id):
    if request.method == 'DELETE':
        try:
            type_job = JobType.objects.get(id=type_job_id)
            type_job.delete()
            msg = getMessage("Successfully Deleted", 201)
            return JsonResponse(msg)
        except Exception as ex:
            msg = getMessage("Can't Delete type " + str(ex), 500)
            print(ex)
            return JsonResponse(msg)



@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        try:
            admin = WIBAdmin.objects.get(admin_id=request.user.id)

            title = request.POST.get('title')
            description = request.POST.get('description')
            category = Category()
            category.title = title
            category.description = description
            category.admin = admin
            category.save()
            msg = getMessage("Successfully Added", 201)
            return JsonResponse(msg)
        except Exception as ex:
            msg = getMessage("Can't add  " + str(ex), 500)
            print(ex)
            return JsonResponse(msg)



@csrf_exempt
def edite_category(request, category_id):
    if request.method == 'POST':
        try:
            admin = WIBAdmin.objects.get(admin_id=request.user.id)
            title = request.PUT.get('title')
            description = request.POST.get('description')

            cat = Category.objects.get(id=category_id)
            cat.title = title
            cat.description = description
            cat.admin = admin
            cat.save()
            msg = getMessage("Successfully Edited", 201)
            return JsonResponse(msg)
        except Exception as ex:
            msg = getMessage("Can't Edite type " + str(ex), 500)
            print(ex)
            return JsonResponse(msg)
    else:
        msg = getMessage("Bad request", 500)
        return JsonResponse(msg)

@csrf_exempt
def delete_category(request, category_id):
    if request.method == 'DELETE':
        try:
            cat = Category.objects.get(id=category_id)
            cat.delete()
            msg = getMessage("Successfully Deleted", 201)
            return JsonResponse(msg)
        except Exception as ex:
            msg = getMessage("Can't Delete type " + str(ex), 500)
            print(ex)
            return JsonResponse(msg)
    else:
        msg = getMessage("Bad request", 500)
        return JsonResponse(msg)



def admin_notify_staff(request):
    if request.method == "GET":
        staff = CustomUser.objects.filter(user_type=2)
        context = {
            'message': "Send Notifications To Staff",
            'allStaff': staff
        }
        return JsonResponse(context, safe=False)
    else:
        msg = getMessage("Bad request", 500)
        return JsonResponse(msg)


def admin_notify_employer(request):
    if request.method == 'GET':
        employers = CustomUser.objects.filter(user_type=3)
        context = {
            'message': "Send Notifications To Students",
            'allEmployers': employers
        }
        return JsonResponse(context, safe=False)
    else:
        msg = getMessage("Bad request", 500)
        return JsonResponse(msg)



@csrf_exempt
def send_staff_notification(request):
    if request.method == 'POST':
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
    else:
        msg = getMessage("Bad request", 500)
        return JsonResponse(msg)



@csrf_exempt
def send_employer_notification(request):
    if request.method == "POST":
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
    else:
        msg = getMessage("Bad request", 500)
        return JsonResponse(msg)



def admin_fcmtoken(request):
    if request.method == "POST":
        token = request.POST.get('token')
        try:
            admin_user = get_object_or_404(CustomUser, id=request.user.id)
            admin_user.fcm_token = token
            admin_user.save()
            return HttpResponse("True")
        except Exception as e:
            return HttpResponse("False")
    else:
        msg = getMessage("Bad request", 500)
        return JsonResponse(msg)



def admin_view_notification(request):
    if request.method == "GET":
        admin = get_object_or_404(WIBAdmin, admin=request.user)
        notifications = NotificationAdmin.objects.filter(admin=admin)
        context = {
            'notifications': notifications,
            'page_title': "View Notifications"
        }
        return JsonResponse(context, safe=False)
    else:
        msg = getMessage("Bad request", 500)
        return JsonResponse(msg)



def all_applicants(request):
    if request.method == 'GET':
        applicant_list = Applicant.objects.all()
        total_applicants = applicant_list.count()
        employers_list = Employer.objects.all()
        total_employers = employers_list.count()

        statistics = {
            "Total_applicants": str(total_applicants),
            "Total_employers": str(total_employers),
        }

        json_apply = []
        for applict in applicant_list:
            staffs = Staff.objects.filter(admin_id=applict.staff.admin)
            json_staff = []
            for st in staffs:
                staff_data = {
                                 "id": str(st.admin.id),
                                 "first_name": str(st.admin.first_name),
                                 "last_name": str(st.admin.last_name),
                                 "email": str(st.admin.email),
                                 "address": str(st.admin.address)
                             },
                json_staff.append(staff_data)

            data = {
                "id_applicant": str(applict.id),
                "Job": {
                    "id_job": str(applict.job.id),
                    "title": str(applict.job.title),
                    "description ": str(applict.job.description),
                    "location": str(applict.job.location),
                    "type_job": {
                        "label": str(applict.job.type_job.label)
                    },
                    "category": {
                        "title": str(applict.job.category.title),
                        "description": str(applict.job.category.description)
                    },

                    "staff": json_staff,

                    "filled": str(applict.job.filled),
                }
            }
            json_apply.append(data)

        json_data = {"stats": statistics, "applies": json_apply}
        return JsonResponse(json_data, safe=False)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)



def get_applicant_by_id(request, applicant_id):
    if request.method == 'GET':
        applicant = Applicant.objects.get(id=applicant_id)
        staffs = Staff.objects.filter(admin_id=applicant.staff.admin)

        json_staff = []
        json_job = []
        json_employer = []

        for st in staffs:
            fs = FileSystemStorage()
            profile_url = fs.url(st.admin.profile_pic)
            staff_data = {
                             "id": str(st.admin.id),
                             "first_name": str(st.admin.first_name),
                             "last_name": str(st.admin.last_name),
                             "email": str(st.admin.email),
                             "address": str(st.admin.address),
                             "profile_pic": profile_url
                         },
            json_staff.append(staff_data)
        data = {
            "id_applicant": str(applicant.id),
            "created_at": str(applicant.created_at),
            "Job": {
                "id_job": str(applicant.job.id),
                "title": str(applicant.job.title),
                "description ": str(applicant.job.description),
                "location": str(applicant.job.location),
                "type_job": {
                    "label": str(applicant.job.type_job.label)
                },
                "category": {
                    "title": str(applicant.job.category.title),
                    "description": str(applicant.job.category.description)
                },
                "filled": str(applicant.job.filled),
                "created_at": str(applicant.job.created_at),
                "livrable_date": str(applicant.job.livrable_date)
            }
        }
        json_job.append(data)

        json_data = {"applicant": json_job, "staffs": json_staff}
        return JsonResponse(json_data, safe=False)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)



def get_all_employer(request, applicant_id):
    if request.method == 'GET':
        employers = Employer.objects.all()
        total_employers = employers.count()
        total_job_finish = 0
        total_job_not_end = 0

        for emp in employers:
            jobs = Job.objects.filter(employer=emp)
            for job in jobs:

                if job.filled == True:
                    total_job_finish += 1
                else:
                    total_job_not_end += 1

        # json_data = {"applicant": json_job, "staffs": json_staff}
        # return JsonResponse(json_data, safe=False)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)
