from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from forms import *
from models.models import *
from django.contrib.auth.models import User

from twitter_API import tweepy_dumper
from hotel_review_crawler import spider as crawler

import re

import datetime
import pytz

import os
import shlex
import subprocess

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

def scrape_main(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    return render(request, 'scrape.main.html', {'form': ScrapeForm})

def perform_scrape(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')

    location_id = 4064
    reviews = crawler.get_all_hotel_review(location_id)
    # tweets = tweepy_dumper.get_all_tweets(search_keyword)
    review_counter = 0
    for review in reviews:
        try:
            hotel = Hotel.objects.filter(name=review['hotel_name'],
                                         star=float(review['starRating']),
                                         rating=float(review['hotelReviewScore']))
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
                                          star=float(review['starRating']),
                                          rating=float(review['hotelReviewScore']))
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

    return render(request, 'scrape.report.html', {'scrape_details': "Scraped " + str(review_counter)})

def documents_index(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    reviews = Hotel_Review.objects.all()
    return render(request, 'documents.all.html', {'reviews': reviews})

def index_management(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    return render(request, 'index.management.main.html', {})

def build_solr_schema(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    build_schema_command = "python manage.py build_solr_schema"
    args = shlex.split(build_schema_command)
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errs = process.communicate()
    solr_config_dirs = os.path.join(os.path.join("models", "templates"), "search_configuration")
    if not os.path.exists(solr_config_dirs):
        os.makedirs(solr_config_dirs)
    with open(os.path.join(os.getcwd(), os.path.join(solr_config_dirs, "schema.xml")), 'w+') as schema_file:
        schema_file.write(outs)
    return render(request, 'index.management.report.html', {'result': 'SOLR schema build successfully.', 'details': outs})

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
    # import pysolr
    # instance = pysolr.Solr('http://localhost:8983/solr/')
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
    return render(request, 'labelling.html', {'reviews':reviews})

def change_label(request):
    review_id = request.POST.__getitem__('id')
    label = request.POST.__getitem__('label')
    hotel_review = Hotel_Review.objects.get(pk=review_id)
    hotel_label = hotel_review.label
    hotel_label.label = label
    hotel_label.method = 'Manual'
    hotel_label.save()
    return HttpResponse()
