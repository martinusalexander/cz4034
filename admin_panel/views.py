from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from forms import *
from models.models import *
from django.contrib.auth.models import User

from twitter_API import tweepy_dumper

import datetime
import pytz

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
    allowed_to_scrape = False
    scrape_details = None
    search_keyword = request.POST.__getitem__('search_keyword')
    time_now = datetime.datetime.now(pytz.utc)

    # We limit that only one scraping can be done within 15 minutes period.
    # Otherwise, we will get API rate limit error
    scrape_histories = ScrapeHistory.objects.all().order_by('-scraped_at')
    if len(scrape_histories) > 0:
        latest_scrape = scrape_histories[0]
        latest_scrape_time = latest_scrape.scraped_at
        if time_now - latest_scrape_time > datetime.timedelta(minutes=15):
            allowed_to_scrape = True
    else:
        allowed_to_scrape = True

    if allowed_to_scrape:
        tweets = tweepy_dumper.get_all_tweets(search_keyword)
        scrape_name = "Scrape for " + search_keyword + " at " + str(time_now)
        scrape_details = ScrapeHistory(user=request.user, name=scrape_name, keyword=search_keyword, n_tweets=0,
                                       scraped_at=time_now)
        scrape_details.save()
        for tweet in tweets:
            if not Documents.objects.filter(id=tweet['id']).exists():
                document = Documents(id=tweet['id'],
                                     name=tweet['name'],
                                     screen_name=tweet['screen_name'],
                                     status=tweet['status'],
                                     location=tweet['location'],
                                     source=tweet['source'],
                                     created_at=tweet['created_at'],
                                     scrape_history=scrape_details)
                document.save()
        scrape_details = ScrapeHistory.objects.get(name=scrape_name)
        n_tweets = len(tweets)
        setattr(scrape_details, 'n_tweets', n_tweets)
        scrape_details.save()

    return render(request, 'scrape.report.html', {'scrape_details': scrape_details})

def scrape_history_index(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    scrape_histories = ScrapeHistory.objects.all().order_by('-scraped_at')
    return render(request, 'scrape.index.html', {'scrape_histories': scrape_histories})

def scraped_documents_index(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    scrape_history_pk = request.POST.__getitem__('scrape_history_pk')
    scrape_history = ScrapeHistory.objects.get(pk=scrape_history_pk)
    documents = Documents.objects.filter(scrape_history=scrape_history)
    return render(request, 'scrape.result.html', {'scrape_history': scrape_history, 'documents': documents})

def documents_index(request):
    if not request.user.is_authenticated:
        return redirect('/admin/sign_in/')
    documents = Documents.objects.all()
    return render(request, 'documents.all.html', {'documents': documents})