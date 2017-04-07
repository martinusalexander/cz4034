import datetime
import os
import shlex
import subprocess

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect

from models.models import *
from forms import *
from crawling import spider as crawler
from classification.classification_data_retriever import retrieve as retrieve_classification_data
from classification.classification_data_processor import process as preprocess_classification_data
from classification.classifier import build_classifier
from classification.classifier import get_classifier

from nltk.tokenize import word_tokenize

# Create your views here.


def main(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    return render(request, 'admin.main.html', {})


def user_sign_in(request):
    if request.user.is_authenticated:
        return redirect('/admin/')
    return render(request, 'account.signin.html', {'form':SignInForm})


def user_sign_in_submit(request):
    if request.user.is_authenticated:
        return redirect('/admin/')
    username = request.POST.__getitem__('username')
    password = request.POST.__getitem__('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')
    else:
        return redirect('/admin/sign_in/')


def create_account(request):
    if request.user.is_authenticated:
        return redirect('/admin/')
    return render(request, 'account.new.html', {'form': CreateUserForm})


def create_account_submit(request):
    if request.user.is_authenticated:
        return redirect('/admin/')
    username = request.POST.__getitem__('username')
    password = request.POST.__getitem__('password')
    email = request.POST.__getitem__('email')
    last_name = request.POST.__getitem__('last_name')
    first_name = request.POST.__getitem__('first_name')
    User.objects.create_user(username=username,
                             password=password,
                             email=email,
                             last_name=last_name,
                             first_name=first_name,
                             is_staff=True,
                             is_active=True
                             )
    user = authenticate(username=username, password=password)
    login(request, user)
    return redirect('/admin/')


def update_account(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    return render(request, 'account.update.html', {'form':
                                                   UpdateUserForm(initial=
                                                   {
                                                       'username':
                                                           request.user.username,
                                                       'password':
                                                           request.user.password,
                                                       'email':
                                                           request.user.email,
                                                       'first_name':
                                                           request.user.first_name,
                                                       'last_name':
                                                           request.user.last_name
                                                   }
                                                   )})


def update_account_submit(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    update_user = request.user
    if any(request.POST.getlist('username')):
        update_user.username = request.POST.__getitem__('username')
    if any(request.POST.getlist('password')):
        update_user.password = request.POST.__getitem__('password')
    if any(request.POST.getlist('email')):
        update_user.email = request.POST.__getitem__('email')
    if any(request.POST.getlist('first_name')):
        update_user.first_name = request.POST.__getitem__('first_name')
    if any(request.POST.getlist('last_name')):
        update_user.last_name = request.POST.__getitem__('last_name')
    update_user.save()
    return redirect('/admin/')


def sign_out(request):
    logout(request)
    return redirect('/')


def crawl_main(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    return render(request, 'crawl.main.html', {'form': CrawlForm})


def perform_crawl(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')

    start_time = datetime.datetime.now()

    location_id = request.POST.__getitem__('location_id')
    reviews = crawler.get_all_hotel_review(location_id)
    review_counter = 0
    for review in reviews:
        try:
            hotel = Hotel.objects.filter(name=review['hotel_name'],
                                         star=float(review['starRating']))
            if not hotel.exists():
                # Create a hotel record, because if does not exist
                hotel = Hotel(name=review['hotel_name'],
                              star=float(review['starRating']),
                              rating=float(review['hotelReviewScore']),
                              url=review['url'],
                              image_url=review['imageUrl'])
                hotel.save()
            else:
                hotel = Hotel.objects.get(name=review['hotel_name'],
                                          star=float(review['starRating']))
                hotel.rating = float(review['hotelReviewScore'])
                hotel.save()
            if not Hotel_Review.objects.filter(hotel=hotel,
                                               title=review['title'],
                                               content=review['content'],
                                               rating=float(review['rating'])).exists():
                review_counter = review_counter + 1
                # Preprocess review date
                original_date = review['date'].replace("Reviewed ", "")
                converted_date = datetime.datetime.strptime(original_date, '%B %d, %Y')
                hotel_label = Hotel_Label()
                hotel_label.save()
                hotel_review = Hotel_Review(hotel=hotel,
                                            title=review['title'],
                                            content=review['content'],
                                            rating=float(review['rating']),
                                            label=hotel_label,
                                            date=converted_date)
                hotel_review.save()
        except: # Any unexpected error from data and database
            continue

    reviews = Hotel_Review.objects.filter(created_at__gte=start_time)

    return render(request, 'crawl.report.html', {'crawl_details': "Crawled " + str(review_counter),
                                                 'reviews': reviews})

def content_index(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    reviews = Hotel_Review.objects.all()
    # Get pages
    try:
        page = request.POST.__getitem__('page')
        page = int(page)
    except KeyError:
        page = 1
    if page <= 0:
        page = 1
    # Paging
    complete_reviews = reviews
    paginator = Paginator(reviews, 100)
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reviews = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        reviews = paginator.page(paginator.num_pages)
    if page != 1:
        has_previous_page = True
    else:
        has_previous_page = False

    if len(complete_reviews) > page * 10:
        has_next_page = True
    else:
        has_next_page = False
    return render(request, 'content.all.html', {'reviews': reviews, 'page':page,
                                                'has_next_page': has_next_page,
                                                'has_previous_page': has_previous_page})


def statistic(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    reviews = Hotel_Review.objects.all()
    n_reviews = len(reviews)
    words = []
    for review in reviews:
        words.extend(word_tokenize(review.content, language='english'))
    n_words = len(words)
    n_unique_words = len(set(words))
    n_manually_labelled_data = 2000
    n_automatically_labelled_data = n_reviews - n_manually_labelled_data
    classification_confusion_matrix = 'plot.png'
    return render(request, 'statistic.html', {'n_reviews': n_reviews, 'n_words': n_words, 'n_unique_words': n_unique_words,
                                              'n_manually_labelled_data': n_manually_labelled_data,
                                              'n_automatically_labelled_data': n_automatically_labelled_data,
                                              'classification_confusion_matrix':
                                                  classification_confusion_matrix})


def index_management(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    return render(request, 'index.management.main.html', {})


def clear_index(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    build_schema_command = "python manage.py clear_index"
    args = shlex.split(build_schema_command)
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Admin needs to respond 'yes'
    process.stdin.write('yes')
    outs, errs = process.communicate()
    return render(request, 'index.management.report.html', {'result': 'Index cleared successfully.', 'details': outs})


def update_index(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    build_schema_command = "python manage.py update_index"
    args = shlex.split(build_schema_command)
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errs = process.communicate()
    return render(request, 'index.management.report.html', {'result': 'Index updated successfully.', 'details': outs})


def rebuild_index(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    build_schema_command = "python manage.py update_index"
    args = shlex.split(build_schema_command)
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Admin needs to respond 'y'
    process.stdin.write('y')
    outs, errs = process.communicate()

    return render(request, 'index.management.report.html', {'result': 'Index rebuilt successfully.', 'details': outs})


def labelling(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    reviews = Hotel_Review.objects.all()[:2000]
    for review in reviews:
        if review.label is not None:
            review.form = UpdateLabelForm(initial=
                                          {'id': review.id,
                                           'label': review.label.label})
        else:
            review.form = UpdateLabelForm(initial=
                                          {'id': review.id,
                                           'label': 'None'})
    return render(request, 'labelling. manual.html', {'reviews':reviews})


def change_label(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden
    review_id = request.POST.__getitem__('id')
    label = request.POST.__getitem__('label')
    hotel_review = Hotel_Review.objects.get(pk=review_id)
    hotel_label = hotel_review.label
    hotel_label.label = label
    hotel_label.method = 'Manual'
    hotel_label.save()
    return HttpResponse()


def classification_management(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    return render(request, 'classification.main.html', {})


def classification_import_data(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    report = retrieve_classification_data()
    return render(request, 'classification.result.html', {'result': report})


def classification_preprocess(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    report = preprocess_classification_data()
    return render(request, 'classification.result.html', {'result': report})


def classification_train(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    report = build_classifier()
    return render(request, 'classification.result.html', {'result': report})


def classification_classify(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    classifier = get_classifier()
    if classifier is None:
        prediction_done = False
        report = 'Error.. Model is not found. Please start the whole process again.'
        return render(request, 'labelling.automatic.html', {'prediction_done': prediction_done,
                                                            'report': report})
    reviews = Hotel_Review.objects.filter(label__method='Automatic')
    for review in reviews:
        prediction = classifier.predict([review.content])[0]
        review_label = review.label
        review_label.label = prediction
        review_label.save()
    prediction_done = True
    report = "Labelled " + str(len(reviews)) + " successfully."
    return render(request, 'labelling.automatic.html', {'prediction_done': prediction_done,
                                                        'reviews': reviews, 'report': report})


def classified_data_index(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    reviews = Hotel_Review.objects.filter(label__method='Automatic')
    # Get pages
    try:
        page = request.POST.__getitem__('page')
        page = int(page)
    except KeyError:
        page = 1
    if page <= 0:
        page = 1
    # Paging
    complete_reviews = reviews
    paginator = Paginator(reviews, 100)
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reviews = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        reviews = paginator.page(paginator.num_pages)
    if page != 1:
        has_previous_page = True
    else:
        has_previous_page = False

    if len(complete_reviews) > page * 10:
        has_next_page = True
    else:
        has_next_page = False
    return render(request, 'labelling.automatic.html', {'reviews': reviews, 'page':page,
                                                        'has_previous_page': has_previous_page,
                                                        'has_next_page': has_next_page})

