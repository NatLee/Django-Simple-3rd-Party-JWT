from django.shortcuts import render
from django.conf import settings

from dev_dashboard.forms import UserRegistrationForm

import logging

logger = logging.getLogger(__name__)

def dashboard(request):
    # template path
    return render(request, "dashboard.html", {
        'social_google_client_id':settings.SOCIAL_GOOGLE_CLIENT_ID,
        'social_microsoft_client_id': settings.SOCIAL_MICROSOFT_CLIENT_ID,
    })

def register(request):
    user_form = UserRegistrationForm()
    # template path
    return render(request, "register.html", {
        "user_form": user_form,
        'social_google_client_id': settings.SOCIAL_GOOGLE_CLIENT_ID,
    })

# override registration login form
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # login
            auth_login(request, form.get_user())
            # redirect
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = AuthenticationForm(request)
    return render(request, 'login.html', {
        'form': form,
        'social_google_client_id': settings.SOCIAL_GOOGLE_CLIENT_ID,
    })


# override session logout
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))
