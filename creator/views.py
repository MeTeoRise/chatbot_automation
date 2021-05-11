from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'Author1',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 27, 2021'
    },
    {
        'author': 'Author2',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 28, 2021'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'creator/home.html', context)

def about(request):
    return render(request, 'creator/about.html')
