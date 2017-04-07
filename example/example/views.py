from dynamic_preferences.models import global_preferences, global_preferences_registry
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {
        'global_preferences': global_preferences.to_dict(),
    })

def storemodel(request):
    preferences = global_preferences_registry.preferences()
    for p in preferences:
        p.to_model()
    return render(request, 'home.html', {
        'global_preferences': global_preferences.to_dict(),
    })
