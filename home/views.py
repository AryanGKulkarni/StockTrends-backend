from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'index.html')


def login_port(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        return ({"error": "Invalid Credentials"})

@csrf_exempt
def register(request):
    if request.method=="POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return redirect('/register.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            User.objects.create(username=username, first_name=firstname, last_name=lastname, email=email, password=password)
            login(request, user)
        return render(request, 'index.html')
        
    return render(request, 'register.html')
