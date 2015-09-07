#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.translation import ugettext as _

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        form = AuthenticationForm(request)

    next = request.GET.get('next', '/')
    context = {'form': form, 'next': next}
    return TemplateResponse(request, 'users/login.html', context)


def logout(request):
    auth_logout(request)
    context = {'title': _('Logged out')}
    return TemplateResponse(request, 'users/logout.html', context)


def home(request):
    return TemplateResponse(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            auth_login(request, new_user)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        form = UserCreationForm()

    next = request.GET.get('next', '/')
    context = {'form': form, 'next': next}
    return TemplateResponse(request, 'users/register.html', context)