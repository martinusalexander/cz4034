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

    try:
        page = request.POST.__getitem__('page')
        page = int(page)
    except KeyError:
        page = 1
    if page <= 0:
        page = 1
    print(page)
    search_keyword = request.POST.__getitem__('search_keyword')

    documents = SearchQuerySet().autocomplete(content=search_keyword).highlight().models(Hotel_Review)

    paginator = Paginator(documents, 10)
    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        documents = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        documents = paginator.page(paginator.num_pages)

    if page != 1:
        has_previous_page = True
    else:
        has_previous_page = False

    if len(documents) > page * 10:
        has_next_page = True
    else:
        has_next_page = False

    return render(request, 'result.html', {'search_keyword':search_keyword, 'documents': documents, 'page': page,
                                           'has_previous_page': has_previous_page, 'has_next_page': has_next_page})

