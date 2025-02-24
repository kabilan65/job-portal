from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobAlertForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from .models import Profile, Post, Applied, SavedJobs, Comment, Job_alerts, Follow
from django.contrib.auth.models import User
from django.db.models.query import Q

@login_required
def home(request):
    saved_posts = SavedJobs.objects.filter(user=request.user)
    save_post = [saved.post for saved in saved_posts]
    location_choices = Post.location_choices

    if request.method == "POST":
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        job_salary = request.POST.get('salary')
        job_type = request.POST.get('job_type')
        experience_level = request.POST.get('experience_level')
        location = request.POST.get('location')

        new_job_post = Post.objects.create(user=request.user, title=job_title, description=job_description, salary=job_salary, job_type=job_type, experience_level=experience_level, location=location)
        new_job_post.save()

        followers = Follow.objects.filter(following=request.user).select_related('follower')
        for follow in followers:
            send_mail(
                subject=f"New Job Alert from {request.user.username}!",
                message=f"{request.user.username} has posted a new job: {job_title}\n\n"
                        f"Job Type: {job_type}\n"
                        f"Location: {location}\n\n"
                        f"{job_description}\n\n",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[follow.follower.email],
                fail_silently=True,
            )


        alerts = Job_alerts.objects.filter(job_type=job_type, location=location)
        for alert in alerts:
            send_mail(
                subject = f"New {job_type} job alert: {job_title}",
                message=f"A new job has been posted in {location}. Check it out!\n\n{job_description}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[alert.user.email],
            )

        messages.success(request, "New job post has been created")
        return redirect('home')

    posts = Post.objects.all()


    applied_post_ids = Applied.objects.filter(user=request.user).values_list('post_id', flat=True)
    
    for post in posts:
        post.applied = post.id in applied_post_ids

    context = {
        'posts' : posts,
        'save_post' : save_post,
        'location_choices' : location_choices,
    }

    return render(request, 'base/home.html', context)


@login_required
def profile_settings(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        profile.bio = request.POST.get('bio', profile.bio)
        profile.skills = request.POST.get('skills', profile.skills)
        profile.education_qualification = request.POST.get('education_qualification', profile.education_qualification)
        profile.location = request.POST.get('location', profile.location)
        profile.phone = request.POST.get('phone', profile.phone)

        if request.FILES.get('pfp'):
            profile.pfp = request.FILES['pfp']

        if request.FILES.get('resume'):
            profile.resume = request.FILES['resume']
    
        profile.save()
        messages.success(request, "Changes saved successfully!")
        return redirect('profile_settings')
    
    return render(request, 'base/profile_settings.html')

@login_required
def views_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(user=user)
    

    is_follow = Follow.objects.filter(follower=request.user, following=user).exists()
    
    context = {
        'profile' : profile,
        'posts' : posts,
        'is_follow' : is_follow,
    }
    return render(request, 'base/profile.html', context)

@login_required
def search(request):
    saved_posts = SavedJobs.objects.filter(user=request.user)
    save_post = [saved.post for saved in saved_posts]

    query = request.GET.get('q')

    search_results = Post.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(salary__icontains=query) | Q(job_type__icontains=query) | Q(experience_level__icontains=query))

    applied_post_ids = Applied.objects.filter(user=request.user).values_list('post_id', flat=True)
    
    for post in search_results:
        post.applied = post.id in applied_post_ids

    context = {
        'query' : query,
        'search_results' : search_results,
        'save_post' : save_post,
    }

    return render(request, 'base/search_result.html', context)

@login_required
def apply_for_job(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    profile = Profile.objects.get(user=request.user)

    if not profile.resume:
        messages.warning(request, 'You need to upload your resume to apply for jobs')
        return redirect('profile_settings')
    
    subject = f"Job Application for {post.title}"
    message = (
        f"Hello {post.user.username},\n\n"
        f"{request.user.username} is interested in applying for the job titled '{post.title}'.\n"
        f"Please find the applicant's resume attached.\n\n"
        f"Best regards,\nJob Portal Team"
    )

    recipient_email = post.user.email
    sender_email = settings.DEFAULT_FROM_EMAIL

    email = EmailMessage(
            subject,
            message,
            sender_email,        
            [recipient_email],
        )
    
    resume_path = profile.resume.path
    resume_name = profile.resume.name.split('/')[-1]
    try:
        with open(resume_path, 'rb') as resume_file:
            email.attach(resume_name, resume_file.read(), 'application/pdf')
    except FileNotFoundError:
        messages.warning(request, "Your resume could not be found")
        return redirect('home')
    
    try:
        email.send(fail_silently=False)
        applied = Applied.objects.create(user=request.user, post=post)
        applied.save()
        messages.success(request, "Your application has been sent successfully!")
    except Exception as e:
        messages.error(request, f"An error occurred while sending your application: {e}")


    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def post_detail(request, post_id):
    
    if request.method == "POST":
        user = request.user
        post = get_object_or_404(Post, id=post_id)
        comment = request.POST.get('comment')
        new_comment = Comment.objects.create(author=user, post=post, comment=comment)
        new_comment.save()
        return redirect('post_detail', post_id)

    saved_posts = SavedJobs.objects.filter(user=request.user)
    save_post = [saved.post for saved in saved_posts]

    post = get_object_or_404(Post, id=post_id)

    applied_post_ids = Applied.objects.filter(user=request.user, post=post)
    post.applied = applied_post_ids

    comments = Comment.objects.filter(post=post)

    context = {
        'post' : post,
        'save_post' : save_post,
        'comments' : comments,
    }

    return render(request, 'base/post_detail.html', context)

def applied_jobs(request):
    if request.user.profile.role == "Job Seeker":
        applied_jobs = Applied.objects.filter(user=request.user)
    else:
        applied_jobs = Applied.objects.filter(post__user=request.user)

    context = {
        'applied_jobs' : applied_jobs,
    }
    
    return render(request, 'base/applications.html', context)

def update_application_status(request, application_id):
    application = get_object_or_404(Applied, id=application_id)
    
    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in ['Applied', 'Under review', 'Rejected', 'Shortlisted']:
            application.application_status = new_status
            application.save()

        subject = f"Update on your application status!"
        message = (
            f"Hello {application.user.username},\n\n"
            f"You've applied for the job titled '{application.post.title}'.\n"
        )
        
        if new_status == "Under review":
            message += f"Your application have been viewed by the recruiter and in under review.\n"
            message += f"Please stay connected for more updates on your application.\n"
        elif new_status == "Rejected":
            message += f"Your application have been rejected by the recruiter.\n"
            message += f"Don't feel low focus and learn more and keep applying.\n"
        elif new_status == "Shortlisted":
            message += f"Congratulations! Your application have been shortlisted by the recuriter.\n"
            message += f"Please stay connected to know the next steps!.\n"
        
        message += f"Best regards,\nJob Portal Team"
        

        recipient_email = application.user.email
        sender_email = settings.DEFAULT_FROM_EMAIL

        email = EmailMessage(
                subject,
                message,
                sender_email,        
                [recipient_email],
            )
        
        try:
            email.send(fail_silently=False)
            messages.success(request, f"Application status updated to {new_status}!")
        except Exception as e:
            messages.warning(request, f"An error occurred while changing application status: {e}")

    return redirect('applied_jobs')

def save_post(request, postid):
    post = get_object_or_404(Post, id=postid)
    saved_post = SavedJobs.objects.filter(user=request.user, post=post)
    if saved_post.exists():
        saved_post.delete()
    else:
        SavedJobs.objects.create(user=request.user, post=post)

    return redirect(request.META.get('HTTP_REFERER', '/'))

def saved_jobs(request):
    saved_posts = SavedJobs.objects.filter(user=request.user)
    posts = [saved.post for saved in saved_posts]
    # saved_posts = SavedJobs.objects.filter(user=request.user).values_list('post_id', flat=True)
    # posts = SavedJobs.objects.filter(id__in=saved_posts)
    context = {
        'posts' : posts,
    }

    return render(request, 'base/saved_jobs.html', context)

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, "Post deleted successfully!")

    return redirect(request.META.get('HTTP_REFERER', '/'))

def delete_comment(request, comment_id, post_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, 'Comment deleted successfully')
    return redirect('post_detail', post_id)   

def job_alerts(request):
    if request.method == "POST":
        form =  JobAlertForm(request.POST)
        if form.is_valid():
            new_alert = form.save(commit=False)
            new_alert.user = request.user
            new_alert.save()
            return redirect('job_alerts')
    else:
        form = JobAlertForm()

    alerts = Job_alerts.objects.filter(user=request.user)
    context = {
        'alerts' : alerts,
        'form' : form,
    }
    return render(request, 'base/job_alerts.html', context)

def delete_alert(request, alert_id):
    alert = get_object_or_404(Job_alerts, id=alert_id)
    alert.delete()
    messages.success(request, 'job alert has been removed sucessfully!')
    return redirect('job_alerts')

def follow(request, username):
    if request.method == "POST":

        following = get_object_or_404(User, username=username)
        follow_entry = Follow.objects.filter(follower=request.user, following=following)

        if follow_entry.exists():
            follow_entry.delete()
        else:
            Follow.objects.create(follower=request.user, following=following)
            
    return redirect('profile', username)