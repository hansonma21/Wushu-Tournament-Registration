from django.shortcuts import redirect, render

# Create your views here.
def registration_view(request):
    if request.method == 'POST':
        # if the user wants to register for the tournament, TODO: register the user for the tournament
        return redirect('tourney_pages:home')
    else:
        form = None
        
    context = {"form": None}
    
    return render(request, 'tourney_reg/registration.html', context=context)