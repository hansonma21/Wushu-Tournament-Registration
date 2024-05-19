from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
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
            next_url = request.POST.get('next')  # Get the URL to redirect to
            if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)  # Redirect to the URL the user was trying to access
            else:
                return redirect('tourney_pages:home')  # Redirect to home page if there is no next URL or if it is not safe
    else:
        form = AuthenticationForm()
    
    return render(request, 'tourney_profiles/login.html', {'form': form})

@login_required(login_url='tourney_profiles:login', redirect_field_name=None)
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have successfully logged out.')
        # then redirect to home page
        return redirect('tourney_pages:home')

@login_required(login_url='tourney_profiles:login', redirect_field_name=None)
def profile_view(request):
    if request.method == 'POST':
        # if the user wants to update their profile, TODO: update the user's profile
        return redirect('tourney_pages:home')
    else:
        # if logged in, show the user's profile
        profile_info = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        context = {'profile_info': profile_info}
        return render(request, 'tourney_profiles/profile.html', context)