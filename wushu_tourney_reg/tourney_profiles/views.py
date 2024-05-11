from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def signup_view(request):
    form = UserCreationForm()
    return render(request, 'tourney_profiles/signup.html', {'form': form})