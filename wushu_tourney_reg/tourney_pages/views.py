from django.shortcuts import render
from .models import News

# Create your views here.
def index(request):
    # TODO: get the latest news from the database and ONLY show the latest 3 news articles
    news = News.objects.filter(display=True)[:3] # already sorted by date_posted in the model
    context = {'news': news}
    return render(request, 'tourney_pages/index.html', context=context)

def learn_more_view(request):
    return render(request, 'tourney_pages/learn_more.html')

def news_view(request):
    # TODO: get the latest news from the database
    news = News.objects.filter(display=True)
    context = {'news': news}
    return render(request, 'tourney_pages/news.html', context=context)