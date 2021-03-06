# !/usr/bin/env python
# encoding:UTF-8

from dynamic_preferences.preferences import UserPreference, GlobalPreference
from dynamic_preferences.types import *
from dynamic_preferences.registries import register


@register
class Title(StringPreference, GlobalPreference):
    section = "auth"
    name = "title"
    default = "title"
    help = "Title"


@register
class ColorHeader(ColorPreference, GlobalPreference):
    section = "auth"
    name = "color_header"
    default = "#34343"
    help = "ColoHeader"


@register
class RegistrationAllowed(BooleanPreference, GlobalPreference):
    """
    Are new registrations allowed?
    """
    section = "auth"
    name = "registration_allowed"
    default = False
    help = "RegistrationAllowed"


@register
class MaxUsers(IntPreference, GlobalPreference):
    """
    Are new registrations allowed?
    """
    section = "auth"
    name = "max_users"
    default = 100


@register
class Header(LongStringPreference, GlobalPreference):
    section = "general"
    name = "presentation"
    default = "You need a presentation"


@register
class ItemsPerPage(IntPreference, GlobalPreference):
    section = "display"
    name = "items_per_page"
    default = 25


@register
class FavoriteVegetable(ChoicePreference, GlobalPreference):
    choices = (
        ("C", "Carrot"),
        ("T", "Tomato. I know, it's not a vegetable"),
        ("P", "Potato")
    )
    section = "auth"
    name = "favorite_vegetable"
    default = "C"


@register
class FavouriteColour(UserPreference, StringPreference):
    """
    What's your favourite colour ?
    """
    section = "misc"
    name = "favourite_colour"
    default = "Green"


@register
class IsZombie(BooleanPreference, UserPreference):
    """
    Are you a zombie?
    """
    section = "misc"
    name = "is_zombie"
    default = True
    help = "IsZombie"


@register
class IsFanOfTokioHotel(BooleanPreference, UserPreference):
    section = "music"
    name = "is_fan_of_tokio_hotel"
    default = False


@register
class FileUpload(FilePreference, GlobalPreference):
    section = "auth"
    name = "file_upload"
    default = "logo.png"
