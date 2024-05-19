from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='tourney_profiles:login')
def registration_view(request):
    if request.method == 'POST':
        # if the user wants to register for the tournament, TODO: register the user for the tournament
        # return redirect('tourney_pages:home')
        form = None
    else:
        form = None
        
    context = {"form": form}
    
    return render(request, 'tourney_reg/registration.html', context=context)