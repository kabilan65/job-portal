from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_settings/', views.profile_settings, name="profile_settings"),
    path('profile/<str:username>/', views.views_profile, name="profile"),
    path('save_post/<int:postid>/', views.save_post, name="save_post"),
    path('job_alerts/', views.job_alerts, name="job_alerts"),
    path('delete_alert/<int:alert_id>/', views.delete_alert, name="delete_alert"),
    path('saved_jobs/', views.saved_jobs, name="saved_jobs"),
    path('search/', views.search, name="search"),
    path('apply_for_job/<int:post_id>/', views.apply_for_job, name="apply_for_job"),
    path('follow/<str:username>/', views.follow, name="follow"),
    path('post_detail/<int:post_id>/', views.post_detail, name="post_detail"),
    path('post_delete/<int:post_id>/', views.delete_post, name="delete_post"),
    path('delete_comment/<int:comment_id>/<int:post_id>/', views.delete_comment, name="delete_comment"),
    path('applied_jobs/', views.applied_jobs, name="applied_jobs"),
    path('update_application_status/<int:application_id>/', views.update_application_status, name="update_application_status",)
]
