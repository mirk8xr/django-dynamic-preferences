from django.shortcuts import render
from dynamic_preferences.models import global_preferences
# from dynamic_preferences.registries import autodiscover
# autodiscover(True)


def home(request):
    gp = global_preferences.to_dict()
    return render(request, 'home.html', {
    })
