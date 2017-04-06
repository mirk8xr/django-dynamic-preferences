from dynamic_preferences.models import global_preferences
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {
        'global_preferences': global_preferences.to_dict(),
    })
