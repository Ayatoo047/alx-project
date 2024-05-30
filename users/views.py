from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



def loginuser(request):
    """
        This view logs in a user. It takes a username and password. It validates the
        user details and returns a message on success and failure 
    """

    page = "login"

    if request.user.is_authenticated:
        return redirect('home')

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
            return redirect('home')
        else:
            messages.error(request, "There is a problem with log in, Check Credentials")


    context = {"page": page}
    return render(request, 'users/login_register.html', context)


def logoutuser(request):
    logout(request)
    return redirect("home")


def Register(request):
    """
        This view registers in a user. It takes a username, password and password corfirm. It validates the
        user details (checking if the user exist and ensure the password correlates) and returns a proper
        message on success and failure 
    """

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']


        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exist')
        
        if password1 != password2:
            messages.error(request, 'Password doesnt match')


        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Registration successful')
            login(request, user)

            return redirect('home')
        else:
            messages.error(request, 'There is error in registration')

    context = {'form': form}
    return render(request, 'users/login_register.html', context)