from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from base.models import Profile

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        check_by_username = User.objects.filter(username=username)
        check_by_email = User.objects.filter(email=email)

        if check_by_username:
            messages.warning(request, 'Username already does exists! please try another')
            return redirect('signup')
        
        elif check_by_email:
            messages.warning(request, 'Email already being used! try signing in?')
            return redirect('signup')

        elif password1 != password2:
            messages.warning(request, "Password doesn't matching!")
            return redirect('signup')
        
        elif password1 == password2:
            if len(password1) <= 7:
                messages.warning(request, 'Password should be atleast 8 characters!')
            
            else:
                new_user = User.objects.create_user(username=username, email=email, password=password1)
                new_user.save()
                Profile.objects.create(user=new_user, userid=new_user.id, role=role)
                messages.success(request, 'Account created successfully! Please signin')
                return redirect('signin')

    return render(request, 'user/signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        validate_user = authenticate(username=username, password=password)

        if validate_user:
            login(request, validate_user)
            messages.success(request, 'Successfullly signed in!')
            return redirect('home')
        else:
            messages.warning(request, 'Invalid credentials!')
            return redirect('signin')

    return render(request, 'user/signin.html')

def signout(request):
    logout(request)
    messages.success(request, 'Signed out successfully!')
    return redirect('signin')