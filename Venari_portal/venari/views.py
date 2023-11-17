from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from . models import *

def user_login(request):
    if request.user.is_authenticated:
        messages.error(request, "Already logged in.")
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST.get('Username')
            password = request.POST.get('Password')
            try:
               #account exist
                user = authenticate(username=User.objects.get(username=username), password=password)
            except User.DoesNotExist:
                #account didnt exist
                user = None
            #invalid username/password
            if user is None:
                messages.error(request, "Please enter a valid username or password.")
                return redirect('/user_login')
            elif user.is_superuser:
                messages.error(request, "Please enter a valid username or password.")
                return redirect('/user_login')
            
            else:
                #check for login if it activate or not
                try:
                    user1 = job_seeker.objects.get(user=user)
                except:
                    user1 = company.objects.get(user=user)    
                if user1.user_type == "applicant" and user1.status=="Activate":
                    login(request, user)
                    return redirect("/signup")  
                elif user1.user_type == "applicant" and user1.status=="Deactivate":
                    messages.error(request, "Account is deactivated. Please contact the admin.")
                    return redirect('/user_login')
                elif user1.user_type == "company":
                    messages.error(request, "Please enter a valid username or password.")
                    return redirect('/user_login')
                else:
                    messages.error(request, "Please enter a valid username or password.")
                    return redirect('/user_login')      

    return render(request, "login.html")

def signup(request):
    if request.method=="POST":   
        username = request.POST['Username']
        email = request.POST['Username']
        first_name=request.POST['First_name']
        last_name=request.POST['Last_name']
        password = request.POST['Password']
        cpass = request.POST['Confirm_password']
        phone = request.POST['Phone_number']
        gender = request.POST['Gender']
        #image = "none"
        uniqueemail = User.objects.filter(email=email)
        uniqueuser = User.objects.filter(username=username)
        if uniqueemail:
            messages.error(request, "Email exists.")
            return redirect('/login')
        elif uniqueuser:
            messages.error(request, "Username exists.")
            return redirect('/login')
        elif password != cpass:
            messages.error(request, "Password doesn't match.")
            return redirect('/login')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=email, password=password)
        applicants = job_seeker.objects.create(user=user, email=email, phone_number=phone, password=password, gender=gender, user_type="applicant", status="Activate")
        user.save()
        applicants.save()
        #logout(request)
        return render(request, "login.html")
    return render(request, "signup.html")

