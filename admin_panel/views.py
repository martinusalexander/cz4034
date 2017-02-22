from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from forms import *
from models import *
from django.contrib.auth.models import User

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