from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)


admin.site.register(CustomUser, UserModel)
admin.site.register(Staff)
admin.site.register(Employer)
admin.site.register(Analyste)
admin.site.register(JobType)
admin.site.register(Job)
admin.site.register(Applicant)
admin.site.register(Category)
admin.site.register(TaskJob)
admin.site.register(CahierCharge)
admin.site.register(FeedbackEmployer)
admin.site.register(FeedbackStaff)
admin.site.register(NotificationEmployer)
admin.site.register(NotificationStaff)
