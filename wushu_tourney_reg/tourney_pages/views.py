from django.shortcuts import render

# Create your views here.
def index(request):
    # TODO: get the latest news from the database and ONLY show the latest 3 news articles
    return render(request, 'tourney_pages/index.html')

def learn_more_view(request):
    return render(request, 'tourney_pages/learn_more.html')

def news_view(request):
    # TODO: get the latest news from the database
    return render(request, 'tourney_pages/news.html')