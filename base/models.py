from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = [
        ('Job Seeker', 'Job Seeker'),
        ('Recruiter', 'Recruiter'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userid = models.IntegerField(editable=False)
    phone = models.PositiveIntegerField(blank=True, null=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    education_qualification = models.CharField(max_length=500, null=True, blank=True)
    pfp = models.ImageField(upload_to='profile_images', default="profile_images/blank-profile-picture.png")
    location = models.CharField(max_length=500, blank=True, null=True)
    skills = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to="user_resume", blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Job Seeker')  # Add this field


    def __str__(self):
        return self.user.username


class Post(models.Model):
    jobtype_choice = [
        ('full-time', 'full-time'),
        ('part-time', 'part-time'),
        ('remote', 'remote'),
        ('internship', 'internship'),
    ]
    experience_choice = [
        ('fresher', 'fresher'),
        ('1-3 years', '1-3 years'),
        ('4-6 years', '4-6 years'),
        ('7+ years', '7+ years'),
    ]
    location_choices = [
        ('Ahmedabad', 'Ahmedabad'),
        ('Bengaluru', 'Bengaluru'),
        ('Bhopal', 'Bhopal'),
        ('Bhubaneswar', 'Bhubaneswar'),
        ('Chandigarh', 'Chandigarh'),
        ('Chennai', 'Chennai'),
        ('Coimbatore', 'Coimbatore'),
        ('Delhi', 'Delhi'),
        ('Faridabad', 'Faridabad'),
        ('Ghaziabad', 'Ghaziabad'),
        ('Gurgaon', 'Gurgaon'),
        ('Guwahati', 'Guwahati'),
        ('Hyderabad', 'Hyderabad'),
        ('Indore', 'Indore'),
        ('Jaipur', 'Jaipur'),
        ('Jalandhar', 'Jalandhar'),
        ('Jamshedpur', 'Jamshedpur'),
        ('Kanpur', 'Kanpur'),
        ('Kochi', 'Kochi'),
        ('Kolkata', 'Kolkata'),
        ('Lucknow', 'Lucknow'),
        ('Ludhiana', 'Ludhiana'),
        ('Madurai', 'Madurai'),
        ('Meerut', 'Meerut'),
        ('Mumbai', 'Mumbai'),
        ('Mysuru', 'Mysuru'),
        ('Nagpur', 'Nagpur'),
        ('Nashik', 'Nashik'),
        ('Noida', 'Noida'),
        ('Patna', 'Patna'),
        ('Pune', 'Pune'),
        ('Raipur', 'Raipur'),
        ('Rajkot', 'Rajkot'),
        ('Ranchi', 'Ranchi'),
        ('Siliguri', 'Siliguri'),
        ('Surat', 'Surat'),
        ('Thane', 'Thane'),
        ('Thrissur', 'Thrissur'),
        ('Tiruchirapalli', 'Tiruchirapalli'),
        ('Udaipur', 'Udaipur'),
        ('Vadodara', 'Vadodara'),
        ('Varanasi', 'Varanasi'),
        ('Vijayawada', 'Vijayawada'),
        ('Visakhapatnam', 'Visakhapatnam'),
        ('Not Disclosed', 'Not Disclosed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
    job_type = models.CharField(default="full-time", choices=jobtype_choice, max_length=20)
    experience_level = models.CharField(max_length=30, default="fresher", choices=experience_choice)
    location = models.CharField(max_length=50, choices=location_choices, default='Not Disclosed')


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']


class Applied(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICE = [
        ('Applied', 'Applied'),
        ('Under review', 'Under review'),
        ('Rejected', 'Rejected'),
        ('Shortlisted', 'Shortlisted'),
    ]
    application_status = models.CharField(max_length=30, choices=STATUS_CHOICE, default="Applied")

    def self(self):
        return f"{self.user.username} - {self.post.title} ({self.application_status})"

class SavedJobs(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'comment made by {self.author.username}'
    
class Job_alerts(models.Model):
    jobtype_choice = [
        ('full-time', 'full-time'),
        ('part-time', 'part-time'),
        ('remote', 'remote'),
        ('internship', 'internship'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=100, choices=jobtype_choice)
    location = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Job alert created by {self.user.username}'
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    