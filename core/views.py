from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.shortcuts import render
from base.models import Blog
from core.models import TenantProfile
from .models import Client, Domain
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.models import User
from django_tenants.utils import schema_context

from django_tenants.utils import schema_context


def index(request):
    # if request.user.is_authenticated:
    #     return redirect('admindash')

    return render(request, 'index.html')


def createInstance(request):
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in')
        return redirect('admindash')

    if request.method == 'POST':
        appname : str = request.POST['appname']
        first_name : str = request.POST['firstname']
        last_name : str = request.POST['lastname']
        email : str = request.POST['email']
        username : str = request.POST['username']
        # phone : str = request.POST['phone_number']
        
        password : str = request.POST['password']
        confirm_password : str = request.POST['password2']
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        
        if password == confirm_password:
            try:
                validate_password(password)
            except ValidationError as e:
                messages.error(request, "Password validation failed: {}".format(e))

        
            try:        
                user = User.objects.create(
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    username = username,
                )
                
                user.set_password(password)
                user.save()
                
                
            
                if not Client.objects.filter(schema_name=appname.lower()).exists() or not Domain.objects.filter(appname.lower()).exists():
                    tenant = Client(schema_name=appname.lower(), name = appname.lower())
                    tenant.save()
                    new_domain = Domain(domain=f'{appname.lower()}.localhost', tenant=tenant ,is_primary=True)
                    new_domain.save()
                    TenantProfile.objects.create(
                        user = user,
                        tenant = appname.lower()
                    )
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(request, f'Tenant {appname} successfully created')
                    return redirect('admindash')
                    return HttpResponse(f"<h1>{appname} successfully created</h1>")
                
                else:
                    messages(request, f"<h1>{appname} IS ALREADY created</h1>")

            except Exception as e:
                messages.error(request, e)
            
    
    return render(request, 'core_login.html', )

def core_login(request):
    """
        This view logs in a user. It takes a username and password. It validates the
        user details and returns a message on success and failure 
    """

    page = "login"

    if request.user.is_authenticated:
        return redirect('admindash')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"WELCOME BACK {str(user.username).upper()}")
            return redirect('adminDash')
        else:
            messages.error(request, "There is a problem with log in, Check Credentials")


    context = {"page": page}
    return render(request, 'core_login.html', context)


def adminDash(request):
    tenant_user = request.user
    tenant_profile = request.user.tenant_profile
    print(tenant_profile.tenant)
    with schema_context(tenant_profile.tenant.lower()):
        users_count = User.objects.count()
        blogs_count = Blog.objects.count()
    
    context = {'tenant_profile': tenant_profile, 'blog_count': blogs_count,
               'tenant_user': tenant_user, 'users_count':users_count,}
    return render(request, 'dashboard.html', context)


def logoutUser(request):
    logout(request)
    return redirect('core_login')
    