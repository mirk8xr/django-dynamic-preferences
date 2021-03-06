# !/usr/bin/env python
# encoding:UTF-8

"""
    Class defined here are used by dynamic_preferences.preferences to specify
    preferences types (Bool, int, etc.) and rules according validation

"""
from django import forms
from dynamic_preferences.forms import OptimisedClearableFileInput, ColorInput
from dynamic_preferences.serializers import *
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _


class BasePreferenceType(object):
    # A form field that will be used to display and edit the preference
    # use a class, not an instance
    field_class = None

    # these default will merged with ones from field_attributes
    # then pass to class provided in field in order to instantiate the actual field

    _default_field_attributes = {
        "required": True,
    }

    # Override this attribute to change field behaviour
    field_attributes = {}

    # A serializer class (see dynamic_preferences.serializers)
    serializer = None

    #: a default value or a callable that return a value to be used as default
    default_value = None

    # Help text
    help = ""

    _field = None

    def get_field_kwargs(self):
        field_kwargs = dict(self._default_field_attributes)
        try:
            field_kwargs['initial'] = self.initial
        except AttributeError:
            pass
        field_kwargs.update(self.field_attributes)
        return field_kwargs

    @cached_property
    def default(self):
        """
        :return: If default_value is a a callable, return the callable result, else, return default_value as is
        """
        if hasattr(self.default_value, '__call__'):
            return self.default_value()
        else:
            return self.default_value

    @property
    def initial(self):
        """
        :return: initial data for form field, from field_attribute['initial'], _default_field_attribute['initial'] or
         default
        """
        return self.field_attributes.get('initial', self._default_field_attributes.get('initial', self.default))

    @property
    def field(self):
        return self.setup_field()

    def setup_field(self):
        """
        Create an actual instance of self.field
        Override this method if needed
        """
        return self.field_class(**self.get_field_kwargs())


class BooleanPreference(BasePreferenceType):
    BOOL_CHOICES = ((True, _('yes')), (False, _('no')))

    _default_field_attributes = {
        "choices": BOOL_CHOICES,
        "widget": forms.RadioSelect,
        "coerce": lambda x: x == 'True',
    }
    default = False
    field_class = forms.TypedChoiceField
    serializer = BooleanSerializer


class IntPreference(BasePreferenceType):
    field_class = forms.IntegerField
    serializer = IntSerializer


class StringPreference(BasePreferenceType):
    _default_field_attributes = {
        "widget": forms.TextInput(attrs={'style': 'width:90%;'}),
    }
    field_class = forms.CharField
    serializer = StringSerializer
    default = ""


class ColorPreference(StringPreference):
    _default_field_attributes = {
        "widget": ColorInput(attrs={'type': 'color'}),
    }


class LongStringPreference(StringPreference):
    _default_field_attributes = {
        "widget": forms.Textarea(attrs={'style': 'width:90%;', 'rows': '3'}),
    }


class ChoicePreference(BasePreferenceType):
    choices = ()
    field_class = forms.ChoiceField
    serializer = StringSerializer

    def get_field_kwargs(self):
        field_kwargs = super(ChoicePreference, self).get_field_kwargs()
        field_kwargs['choices'] = self.choices or self.field_attributes['initial']
        return field_kwargs


class FilePreference(BasePreferenceType):
    _default_field_attributes = {
        "widget": OptimisedClearableFileInput,
        "required": False
    }
    field_class = forms.FileField
    serializer = FileSerializer
