from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from haystack.query import SearchQuerySet

from forms import *
from models.models import *
from query_optimization.query_optimizer import optimize
from query_optimization.spelling import correction as spell_correction

import datetime

# Create your views here.

def main(request):
    return render(request, 'user.main.html', {'form': SearchDocumentsForm})

def about(request):
    return render(request, 'about.html', {})

def search_documents(request):

    start_time = datetime.datetime.now()
    # Get pages
    try:
        page = request.POST.__getitem__('page')
        page = int(page)
    except KeyError:
        page = 1
    if page <= 0:
        page = 1

    # Get original query entered by user
    search_keyword_original = request.POST.__getitem__('search_keyword')

    # Find whether user wants spell correction
    try:
        need_spell_correction = request.POST.__getitem__('need_spell_correction')
        if need_spell_correction == 'false':
            need_spell_correction = False
        else:
            need_spell_correction = True
    except KeyError:
        need_spell_correction = True

    search_keyword = optimize(search_keyword_original, do_spell_correction=need_spell_correction)

    # Find the corrected spelling
    if need_spell_correction:
        search_keyword_spell_correct = spell_correction(search_keyword_original)
        if search_keyword_spell_correct == search_keyword_original:
            need_spell_correction = False
        else:
            need_spell_correction = True
    else:
        search_keyword_spell_correct = search_keyword_original
        need_spell_correction = False

    # Search
    documents = SearchQuerySet().autocomplete(content=search_keyword).highlight().models(Hotel_Review)

    # Paging
    complete_documents = documents
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

    if len(complete_documents) > page * 10:
        has_next_page = True
    else:
        has_next_page = False

    end_time = datetime.datetime.now()
    execution_time = end_time - start_time
    time = 'Executed in ' + str(execution_time.seconds) + '.' + str(execution_time.microseconds)+ ' second(s).'

    return render(request, 'result.html', {'search_keyword':search_keyword_original, 'documents': documents, 'page': page,
                                           'need_spell_correction': need_spell_correction,
                                           'search_keyword_spell_correct': search_keyword_spell_correct,
                                           'time': time,
                                           'has_previous_page': has_previous_page, 'has_next_page': has_next_page})

