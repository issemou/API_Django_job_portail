from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from main_app import views
from main_app.auth_management import Admin, Employer, Staff, Analyste
from main_app.functionnality_managements import admin_views, employer_views, staff_views, analyste_views

urlpatterns = [

    # AUTH_FUNC
    path("admin/register", Admin.wib_registration, name="wib_admin_registration"),
    path("admin/update/profile", Admin.admin_edite_profile, name="admin_update_profile"),
    path("admin/profile", Admin.admin_view_profile, name="admin_profile"),

    path("analyste/register", Analyste.analyste_registration, name="analyste_registration"),
    path("analyste/update/profile", Analyste.analyste_edite_profile, name="analyste_update_profile"),
    path("analyste/profile", Analyste.analyste_view_profile, name="analyste_profile"),

    path("employer/register", Employer.employer_registration, name="employer_registration"),
    path("employer/update/profile", Employer.employer_edite_profile,
         name="employer_update_profile"),
    path("employer/profile", Employer.employer_view_profile, name="employer_profile"),

    path("staff/register", Staff.Satff_registration, name="staff_registration"),
    path("staff/update/profile", Staff.staff_edite_profile, name="staff_update_profile"),
    path("staff/profile", Staff.staff_view_profile, name="staff_profile"),
    path("logout", views.logout_user, name="logout"),
    path("login", views.doLogin, name="login"),


    # ADMIN VIEWS

    path("add/type-job", admin_views.add_type_job, name="wib_admin_add_type_job"),
    path("edite/type-job/<int:type_job_id>", admin_views.edite_type_job, name="wib_admin_edite_type_job"),
    path("delete/type-job/<int:type_job_id>", admin_views.delete_type_job,
         name="wib_admin_delete_type_job"),
    path("add/category", admin_views.add_category, name="wib_admin_add_category"),
    path("edite/category/<int:category_id>", admin_views.edite_category, name="wib_admin_edite_category"),
    path("delete/category/<int:category_id>", admin_views.delete_category,
         name="wib_admin_delete_category"),
    path("admin/applicants", admin_views.all_applicants, name="admin_view_applicants"),
    path("admin/applicant/<int:applicant_id>", admin_views.get_applicant_by_id,
         name="admin_get_by_id_applicants"),
    path("send_staff_notification/", admin_views.send_staff_notification,
         name='send_staff_notification'),
    path("send_employer_notification/", admin_views.send_employer_notification,
         name='send_employer_notification'),
    path("admin_notify_staff", admin_views.admin_notify_staff,
         name='admin_notify_staff'),
    path("admin_notify_employer", admin_views.admin_notify_employer,
         name='admin_notify_employer'),
    path("admin/fcmtoken/", admin_views.admin_fcmtoken, name='admin_fcmtoken'),
    path("admin/view/notification/", admin_views.admin_view_notification,
         name="admin_view_notification"),

    #ANALYSTE
    path("analyste/verify_job/<int:job_id>", analyste_views.validate_book_job, name="analyste_verify_job"),
    # EMPLOYER VIEWS

    path("add/job", employer_views.add_job, name="employer_add_job"),
    path("edite/job/<int:job_id>", employer_views.edite_job, name="employer_edite_job"),
    path("jobs/", employer_views.get_all_jobs, name="employer_get_jobs"),
    path("delete/job/<int:job_id>", employer_views.delete_job, name="employer_delete_job"),
    path("employer/send_staff_notification/", employer_views.send_staff_notification,
         name='employer_send_staff_notification'),
    path("employer/send_admin_notification/", employer_views.send_admin_notification,
         name='employer/send_admin_notification'),
    path("employer_notify_staff", employer_views.employer_notify_staff,
         name='employer_notify_staff'),
    path("employer_notify_admin", employer_views.employer_notify_admin,
         name='employer_notify_admin'),
    path("employer/fcmtoken/", employer_views.employer_fcmtoken, name='employer_fcmtoken'),
    path("employer/view/notification/", employer_views.employer_view_notification,
         name="employer_view_notification"),

    # STAFF


    path("staff/apply/<int:job_id>", staff_views.Staff_apply_job, name="staff_apply_job"),
    path("staff/applies/", staff_views.get_all_Applyjob, name="staff_applies_job"),
    path("staff/send_employer_notification/", staff_views.send_employer_notification,
         name='staff_send_employer_notification'),
    path("staff/send_admin_notification/", staff_views.send_admin_notification,
         name='staff/send_admin_notification'),
    path("staff_notify_employer", staff_views.staff_notify_employer,
         name='staff_notify_employer'),
    path("staff_notify_admin", staff_views.staff_notify_admin,
         name='staff_notify_admin'),
    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),
    path("staff/view/notification/", staff_views.staff_view_notification,
         name="staff_view_notification"),
    # APP VIEWS


    path("category/all", views.get_all_category, name="category_all"),
    path("category/<int:category_id>", views.get_category_by_id, name="category"),
    path("type_job/all", views.get_all_type_job, name="type_job_all"),
    path("type_job/<int:type_job_id>", views.get_type_job_by_id, name="type_job"),
]
