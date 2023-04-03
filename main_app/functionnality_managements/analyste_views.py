from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from main_app.helpers.commonts import getMessage
from main_app.models import Job, CahierCharge, Analyste



@csrf_exempt
def validate_book_job(request, job_id):
    if request.method == 'POST':
        try:
            upload = request.FILES.get('upload')
            max_task = request.POST.get('max_task')
            min_task = request.POST.get('min_task')
            isvalidated = request.POST.get('isvalidated')

            job = get_object_or_404(Job, id=job_id)
            cahier = CahierCharge.objects.get(job=job)
            analyste = Analyste.objects.get(admin_id=request.user.id)

            if upload is not None:
                cahier.upload = upload

            if isvalidated == "True":
                cahier.isValidated = isvalidated
                cahier.max_task = max_task
                cahier.min_task = min_task
                cahier.save()
                fs = FileSystemStorage()
                cahier_url = fs.url(cahier.upload)
                send_mail(
                    'Validation Fonctionnality Book',
                    f"votre job a bien ete approuver et mis en ligne http://localhost:8000{cahier_url}",
                    ['ridovicisseou@gmail.com', 'sandseller10@gmail.com'],
                    fail_silently=False
                )
                msg = getMessage("Successfully Verify Job", 201)
                return JsonResponse(msg)
            else:
                send_mail(
                    'Validation Fonctionnality Book',
                    "votre job n'a pas pu etre poster suite a la non-validation de votre cahier",
                    ['ridovicisseou@gmail.com', 'sandseller10@gmail.com'],
                    fail_silently=False
                )
                return HttpResponse(False)

            cahier.save()
            return HttpResponse(False)

        except Exception as ex:
            msg = getMessage("Can't Verify" + " " + str(ex), 500)
            print(ex)
            return JsonResponse(msg)
    else:
        msg = getMessage("Bad Request", 500)
        return JsonResponse(msg)
