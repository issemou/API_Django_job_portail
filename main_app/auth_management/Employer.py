from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from main_app.helpers.commonts import getMessage, check_email_exist
from main_app.models import CustomUser, Employer


@csrf_exempt
def employer_registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        compagny_name = request.POST.get('compagny_name')
        compagny_description = request.POST.get('compagny_description')
        website = request.POST.get('website')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile = request.FILES.get('profile_pic')

        if check_email_exist(email):
            fp = getMessage("Email Already Exists", 500)
            return JsonResponse(fp)
        else:
            try:
                cust = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    user_type=3,
                    first_name=first_name,
                    last_name=last_name,
                    profile_pic=profile
                )
                cust.address = address
                cust.employer.compagny_name = compagny_name
                cust.employer.compagny_description = compagny_description
                cust.employer.website = website
                cust.save()
                send_mail(
                    'VALIDATION CREATION DE COMPTE',
                    f"Salut a vous Monsieur {cust.first_name} {cust.last_name} "
                    f" veillez vous connecter et rejoindre l'aventure avec nous http://localhost:8000/",
                    settings.EMAIL_HOST_USER,
                    [cust.email],
                    fail_silently=False
                )
                fp = getMessage("Success Created", 200)
                return JsonResponse(fp)

            except Exception as e:
                fp = getMessage("Could Not Add " + str(e), 500)
                return JsonResponse(fp)
    else:
        fp = getMessage("Bad Request", 500)
        return JsonResponse(fp)


@login_required
@csrf_exempt
def employer_view_profile(request):
    if request.method == 'GET':
        admin = CustomUser.objects.get(id=request.user.id)
        fs = FileSystemStorage()
        profile_url = fs.url(admin.profile_pic)
        data = {
            "id": admin.id,
            "user_type": admin.user_type,
            "first_name": admin.first_name,
            "last_name": admin.last_name,
            "address": admin.address,
            "email": admin.email,
            "compagny_name": admin.employer.compagny_name,
            "compagny_description": admin.employer.compagny_description,
            "website": admin.employer.website,
            "profile_picture": profile_url
        }

        fp = getMessage("Sucessfully", 200, data=data)
        return JsonResponse(fp)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)


@login_required
@csrf_exempt
def employer_edite_profile(request):
    if request.method == 'POST':
        employer = get_object_or_404(Employer, admin_id=request.user.id)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')
        compagny_name = request.POST.get('compagny_name')
        compagny_description = request.POST.get('compagny_description')
        website = request.PUT.get('website')
        profile = request.FILES.get('profile_pic')

        try:
            cust = CustomUser.objects.get(id=employer.admin.id)

            if cust.email == email:
                cust.email = str(email).lower()

            if cust.email != email:
                if check_email_exist(email) == True:
                    fp = getMessage("Email Already Exists", 500)
                    return JsonResponse(fp)
                else:
                    cust.email = str(email).lower()

            if profile != None:
                cust.profile_pic = profile

            cust.first_name = str(first_name).lower()
            cust.last_name = str(last_name).lower()
            cust.address = str(address).lower()
            if password is not None:
                cust.set_password(str(password).lower())

            cust.save()
            employer.website = str(website).lower()
            employer.compagny_description = str(compagny_description).lower()
            employer.compagny_name = str(compagny_name).lower()
            employer.save()
            message = f"Salut a vous Monsieur {cust.first_name} {cust.last_name}  veillez vous connecter et rejoindre l'aventure avec nous ! " \
                      f"vos nouveau identifiants sont : Email {cust.email} " \
                      f" Password:{password}" \
                      f"Gadez les secret : login http://localhost:8000/"

            send_mail(
                'MISE A JOUR DU COMPTE UTILISATEUR',
                message,
                settings.EMAIL_HOST_USER,
                [cust.email],
                fail_silently=False
            )
            fp = getMessage("Success Updated", 200)
            return JsonResponse(fp)

        except Exception as e:
            fp = getMessage("Could Not Update " + str(e), 500)
            return JsonResponse(fp)

    else:
        fp = getMessage("Bad Request", 500)
        return JsonResponse(fp)

