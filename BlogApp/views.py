from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def blogdetails(request, id):
    blogdata = BlogData.objects.get(id=id)
    return render(request, 'blog-details.html',context = {'blog':blogdata})

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        usermessage = ContactMessages.objects.create(name=name, email=email, subject=subject, message=message)
        messages.success(request, "We have Received your Message will contact you soon....")
    return render(request, 'contact.html')

def blog(request):
    blogdata = BlogData.objects.all().values()
    return render(request, 'blog.html', context={'blogdata': blogdata})

def team(request):
    return render(request, 'team.html')

def signup(request):
    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('useremail')
        password = request.POST.get('userpassword')
        confpass = request.POST.get('confirmpassword')
        # userprof = request.FILES['userprofile']
        # fs = FileSystemStorage()
        # file = fs.save(userprof.name, userprof)
        # file_url = fs.url(file)
        if UsersRegistered.objects.filter(email = email).exists():
            messages.error(request, "User already Exists !!!")
        else:
            if password == confpass:
                    userdata = UsersRegistered.objects.create(name= name, email=email, password= make_password(password))
                    messages.success(request, "Registration Successfull !!!")
            else:
                messages.error(request, "Both password must be same")
    return render(request, "signup.html")

def userlogin(request):
    if request.method == "POST":
        useremail = request.POST.get('useremail')
        userpassword = request.POST.get('userpassword')
        if UsersRegistered.objects.filter(email = useremail):
            user = UsersRegistered.objects.get(email = useremail)
            success = check_password(userpassword, user.password)
            if success == True:
                return redirect('index')
            else:
                messages.error(request, "Please Enter Valid Password")
        else:
            messages.error(request, "User Doesn't Exits !!!")
    return render(request, "login.html")

@login_required(login_url="/userlogin")
def createblog(request):
    if request.method == "POST":
        blogimage = request.FILES['blog-image']
        blogtitle = request.POST.get('blog-title')
        smalldesc = request.POST.get('small-desc')
        maincontent = request.POST.get('main-content')
        fs = FileSystemStorage()
        file = fs.save(blogimage.name, blogimage)
        file_url = fs.url(file)
        blogdata = BlogData.objects.create(image = file_url, title = blogtitle, smalldesc = smalldesc, maincontent = maincontent )
        messages.success(request, "Your Blog Post was Published Successfully")
    return render(request, 'create-blog.html')

def userlogout(request):
    logout(request)
    return redirect("index")