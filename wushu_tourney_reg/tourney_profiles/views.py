from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomProfileCreationForm

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = CustomProfileCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save() # returned the newly created user
            # log the user in
            login(request, new_user)
            messages.success(request, 'You have successfully signed up. You are now logged in.')
            # then redirect to home page
            return redirect('tourney_pages:home')
    else:
        form = CustomProfileCreationForm()
    
    context = {'form': form}
    return render(request, 'tourney_profiles/signup.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            # then redirect to home page
            return redirect('tourney_pages:home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'tourney_profiles/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have successfully logged out.')
        # then redirect to home page
        return redirect('tourney_pages:home')

def profile_view(request):
    if request.method == 'POST':
        # if the user wants to update their profile, TODO: update the user's profile
        return redirect('tourney_pages:home')
    else:
        # if the user wants to view their profile
        if request.user.is_anonymous:
            # if not logged in, redirect to login page
            return redirect('tourney_profiles:login')
        else:
            # if logged in, show the user's profile
            profile_info = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
            context = {'profile_info': profile_info}
            return render(request, 'tourney_profiles/profile.html', context)