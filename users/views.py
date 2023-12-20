from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from .models import CustomUser
from easyaudit.models import CRUDEvent, LoginEvent, RequestEvent
from django.contrib.auth.hashers import make_password


def signup(request):
    if request.method == 'POST':
        print("Form submitted via POST.")
        # Extract data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        raw_password = request.POST.get('password')
        
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        
        # Create a CustomUser instance
        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone_number=tel
        )
        # Set the hashed password
        user.password = make_password(raw_password)
        
        # Save the user
        user.save()
        
        # Redirect to login page after registration
        return render(request,'Users/Login.html')
    
    return render(request, 'Users/SignUp.html')



def logs_view(request):
    # Fetching logs from different audit models
    crud_events = CRUDEvent.objects.all().order_by('-datetime')[:50]  # Limiting to the latest 50 events as an example
    login_events = LoginEvent.objects.all().order_by('-datetime')[:50]
    request_events = RequestEvent.objects.all().order_by('-datetime')[:50]

    context = {
        'crud_events': crud_events,
        'login_events': login_events,
        'request_events': request_events,
    }

    return render(request, 'Pages/Logs.html', context)

def Login(request):
    
    return render(request, 'Users/Login.html')