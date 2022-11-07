from django.shortcuts import render
from django.conf import settings

from dev_dashboard.forms import UserRegistrationForm


import logging

logger = logging.getLogger(__name__)

def dashboard(request):
    # template path
    return render(request, "dashboard/dashboard.html", {'social_google_client_id':settings.SOCIAL_GOOGLE_CLIENT_ID})


def register(request):
    user_form = UserRegistrationForm()
    # template path
    return render(request, "dashboard/register.html", {"user_form": user_form})

