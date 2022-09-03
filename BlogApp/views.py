from urllib import request

from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q
import random

# Create your views here.


def index(request):
    if 'userdata' in request.session:
        curr_user = request.session['userdata']
        curr_user_details = UsersRegistered.objects.get(id=curr_user)
        blog_data = BlogData.objects.order_by('?').first()
        return render(request, 'index.html', context={'user':curr_user_details, "randomblog":blog_data})
    blog_data = BlogData.objects.order_by('?').first()
    return render(request, 'index.html', context={'randomblog':blog_data})

def about(request):
    if 'userdata' in request.session:
        curr_user = request.session['userdata']
        curr_user_details = UsersRegistered.objects.get(id=curr_user)
        return render(request, 'about.html', context={'user': curr_user_details})
    return render(request, 'about.html')

def blogdetails(request, id):
    if 'userdata' in request.session:
        curr_user = request.session['userdata']
        curr_user_details = UsersRegistered.objects.get(id=curr_user)
        blogdata = BlogData.objects.get(id=id)
        return render(request, 'blog-details.html', context={'user': curr_user_details, 'blog':blogdata})
    blogdata = BlogData.objects.get(id=id)
    return render(request, 'blog-details.html', context = {'blog':blogdata})

def contact(request):
    if 'userdata' in request.session:
        curr_user = request.session['userdata']
        curr_user_details = UsersRegistered.objects.get(id=curr_user)
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            usermessage = ContactMessages.objects.create(name=name, email=email, subject=subject, message=message)
            messages.success(request, "We have Received your Message will contact you soon....")
        return render(request, 'contact.html', context={'user': curr_user_details})
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        usermessage = ContactMessages.objects.create(name=name, email=email, subject=subject, message=message)
        messages.success(request, "We have Received your Message will contact you soon....")
    return render(request, 'contact.html')

def blog(request):
    if 'userdata' in request.session:
        search_post = request.GET.get('q')
        if search_post:
            blogdata = BlogData.objects.filter(Q(title__icontains=search_post) & Q(smalldesc__icontains=search_post))
        else:
            blogdata = BlogData.objects.all().values()
        curr_user = request.session['userdata']
        curr_user_details = UsersRegistered.objects.get(id=curr_user)
        paginator = Paginator(blogdata, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog.html', context={'user': curr_user_details, 'blogdata': page_obj})
    search_post = request.GET.get('q')
    if search_post:
        blogdata = BlogData.objects.filter(Q(title__icontains=search_post) & Q(smalldesc__icontains=search_post))
    else:
        blogdata = BlogData.objects.all().values()
    paginator = Paginator(blogdata, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', context={'blogdata': page_obj})

def team(request):
    if 'userdata' in request.session:
        blogger = UsersRegistered.objects.all()
        curr_user = request.session['userdata']
        curr_user_details = UsersRegistered.objects.get(id=curr_user)
        return render(request, 'team.html', context={'user': curr_user_details, "blogger":blogger})
    blogger = UsersRegistered.objects.all()
    return render(request, 'team.html', context={"blogger":blogger})

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        occupation = request.POST.get('occupation')
        summary = request.POST.get('summary')
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
                    userdata = UsersRegistered.objects.create(firstname= firstname, lastname=lastname, occupation=occupation, summary=summary, email=email, password= make_password(password))
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
                # succ = "Logged in successfull"
                # return render(request, "index.html", context={"success":succ, "user":user})
                request.session['userdata'] = user.id
                return redirect('index')
            else:
                messages.error(request, "Please Enter Valid Password")
        else:
            messages.error(request, "User Doesn't Exits !!!")

    return render(request, "login.html")


def createblog(request):
    if 'userdata' in request.session:
        if request.method == "POST":
            curr_user = request.session['userdata']
            curr_user_details = UsersRegistered.objects.get(id=curr_user)
            bloggername = curr_user_details.firstname +" "+ curr_user_details.lastname
            blogimage = request.FILES['blog-image']
            blogtitle = request.POST.get('blog-title')
            smalldesc = request.POST.get('small-desc')
            maincontent = request.POST.get('main-content')
            fs = FileSystemStorage()
            file = fs.save(blogimage.name, blogimage)
            file_url = fs.url(file)
            blogdata = BlogData.objects.create(authorid = curr_user_details,author = bloggername, image = file_url, title = blogtitle, smalldesc = smalldesc, maincontent = maincontent )
            messages.success(request, "Your Blog Post was Published Successfully")
        return render(request, 'create-blog.html')
    else:
        return redirect('userlogin')
    return render(request, 'login.html')

def userlogout(request):
    try:
        del request.session['userdata']
    except:
        return redirect('index')
    return redirect('index')

def authorblogs(request, id):
    if 'userdata' in request.session:
        blogs = UsersRegistered.objects.get(id=id).blogdata_set.all()
        return render(request, 'authorblogs.html', context={'blogs':blogs})
    else:
        return redirect('userlogin')
    return render(request, 'login.html')

def editblog(request, id):
    if 'userdata' in request.session:
        blogdata = BlogData.objects.get(id=id)
        return render(request, 'editblog.html', context={'blogdata':blogdata})
    else:
        return redirect('userlogin')
    return render(request, 'login.html')

def updateblogs(request, id):
    if 'userdata' in request.session:
        if request.method == "POST":
            # blogimage = request.FILES['blog-image']
            blogtitle = request.POST.get('blog-title')
            smalldesc = request.POST.get('small-desc')
            maincontent = request.POST.get('main-content')
            blogdata = BlogData.objects.get(id=id)
            # blogdata.image = blogimage
            blogdata.title = blogtitle
            blogdata.smalldesc = smalldesc
            blogdata.maincontent = maincontent
            BlogData.objects.update(title=blogtitle, smalldesc=smalldesc, maincontent=maincontent)
            messages.success(request, "Your Blog Post was Updated Successfully")
            return redirect('index')
    else:
        return redirect('userlogin')
    return render(request, 'login.html')

def deleteblog(request, id):
    if 'userdata' in request.session:
        blogdata = BlogData.objects.get(id=id)
        blogdata.delete()
        # return redirect('authorblogs')
        return redirect('index')
    else:
        return redirect('userlogin')
    return render(request, 'login.html')




