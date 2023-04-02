from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE = ((1, "WIB"), (2, "Staff"), (3, "Employer"), (4, "Analyste"))
    GENDER = [("M", "Male"), ("F", "Female")]

    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField(upload_to='media_profiles')
    address = models.TextField()
    fcm_token = models.TextField(default="")  # For firebase notifications
    forgot_password_token = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.last_name + ", " + self.first_name


class WIBAdmin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name


class Analyste(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name


class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name


class Employer(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    compagny_name = models.CharField(max_length=255)
    compagny_description = models.TextField(default="")
    website = models.CharField(max_length=255)

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name


class JobType(models.Model):
    admin = models.ForeignKey(WIBAdmin, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    admin = models.ForeignKey(WIBAdmin, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(default=" ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    filled = models.BooleanField(default=False)
    location = models.CharField(max_length=255)
    type_job = models.ForeignKey(JobType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    livrable_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CahierCharge(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    isValidated = models.BooleanField(default=False)
    min_task = models.IntegerField(default=1)
    max_task = models.IntegerField(default=1)
    upload = models.FileField(upload_to='media_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Applicant(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStaff(models.Model):
    student = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    upload = models.FileField(upload_to='media_feedback')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackEmployer(models.Model):
    staff = models.ForeignKey(Employer, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    upload = models.FileField(upload_to='media_feedback')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    upload = models.FileField(upload_to='media_notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationEmployer(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    message = models.TextField()
    upload = models.FileField(upload_to='media_notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationAdmin(models.Model):
    admin = models.ForeignKey(WIBAdmin, on_delete=models.CASCADE)
    message = models.TextField()
    upload = models.FileField(upload_to='media_notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            WIBAdmin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Employer.objects.create(admin=instance)
        if instance.user_type == 4:
            Analyste.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.wibadmin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.employer.save()
    if instance.user_type == 4:
        instance.analyste.save()
