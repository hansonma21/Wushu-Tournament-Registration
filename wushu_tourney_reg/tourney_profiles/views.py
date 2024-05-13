from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save() # returned the newly created user
            # log the user in
            login(request, new_user)
            # then redirect to home page
            return redirect('tourney_pages:home')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'tourney_profiles/signup.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            user = form.get_user()
            login(request, user)
            # then redirect to home page
            return redirect('tourney_pages:home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'tourney_profiles/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        # then redirect to home page
        return redirect('tourney_pages:home')