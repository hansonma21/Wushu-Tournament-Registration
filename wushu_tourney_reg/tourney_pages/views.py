from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'tourney_pages/index.html')

def learn_more_view(request):
    return render(request, 'tourney_pages/learn_more.html')