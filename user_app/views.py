from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from haystack.query import SearchQuerySet
from django.views.generic import ListView, DetailView

from forms import *
from models.models import *

# Create your views here.

def main(request):
    return render(request, 'user.main.html', {'form': SearchDocumentsForm})

def about(request):
    return render(request, 'about.html', {})

def search_documents(request):
    # if 'keyword' in request.POST:
    #     keyword = request.POST.get['search_keyword']
    keyword = request.POST.__getitem__('search_keyword')
    documents = SearchQuerySet().autocomplete(content=keyword).highlight().models(Hotel_Review)
    document_list = documents.all()

    page = request.GET.get('page',1)
    paginator = Paginator(document_list, 10)

    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        documents = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        documents = paginator.page(paginator.num_pages)

    return render(request, 'result.html', {'keyword':keyword, 'documents': documents})

