from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from forms import *
from models.models import *

# Create your views here.

def main(request):
    return render(request, 'user.main.html', {'form': SearchDocumentsForm})

def about(request):
    return render(request, 'about.html', {})

def search_documents(request):
    keyword = request.POST.__getitem__('search_keyword')
    documents = Documents.objects.filter(content__icontains=keyword)
    return render(request, 'result.html', {'keyword':keyword, 'documents': documents})