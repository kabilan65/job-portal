from django.contrib import admin
from .models import Profile,Post, Applied, SavedJobs, Comment, Job_alerts, Follow

admin.site.register(Profile)
admin.site.register(Job_alerts)
admin.site.register(Comment)
admin.site.register(SavedJobs)
admin.site.register(Post)
admin.site.register(Applied)
admin.site.register(Follow)