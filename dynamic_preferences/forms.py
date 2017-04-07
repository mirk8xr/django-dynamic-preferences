from django import forms
from .registries import global_preferences_registry, user_preferences_registry, site_preferences_registry
from six import string_types
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy


def preference_form_builder(form_base_class, preferences=[], **kwargs):
    """
    Return a form class for updating preferences
    :param form_base_class: a Form class used as the base. Must have a ``registry` attribute
    :param preferences: a list of :py:class:
    :param section: a section where the form builder will load preferences
    """
    registry = form_base_class.registry
    preferences_obj = []
    if len(preferences) > 0:
        # Preferences have been selected explicitly 
        for pref in preferences:
            if isinstance(pref, string_types):
                preferences_obj.append(registry.get(name=pref))
            elif type(pref) == tuple:
                preferences_obj.append(registry.get(name=pref[0], section=pref[1]))
            else:
                raise NotImplementedError("The data you provide can't be converted to a Preference object")
    else:
        # Try to use section param
        preferences_obj = registry.preferences(section=kwargs.get('section', None))

    fields = {}
    instances = []
    for preference in preferences_obj:
        f = preference.field
        model_kwargs = kwargs.get('model', {})
        instance = preference.to_model(**model_kwargs)
        f.initial = instance.value
        fields[preference.identifier()] = f
        instances.append(instance)

    form_class = type('Custom' + form_base_class.__name__, (form_base_class,), {})
    form_class.base_fields = fields
    form_class.preferences = preferences_obj
    form_class.instances = instances
    return form_class


def global_preference_form_builder(preferences=[], **kwargs):
    """
    A shortcut :py:func:`preference_form_builder(GlobalPreferenceForm, preferences, **kwargs)`
    """
    return preference_form_builder(GlobalPreferenceForm, preferences, **kwargs)


def user_preference_form_builder(user, preferences=[], **kwargs):
    """
    A shortcut :py:func:`preference_form_builder(UserPreferenceForm, preferences, **kwargs)`
    :param user: a :py:class:`django.contrib.auth.models.User` instance
    """
    return preference_form_builder(UserPreferenceForm, preferences, model={'user': user}, **kwargs)


def site_preference_form_builder(preferences=[], **kwargs):
    """
    A shortcut :py:func:`preference_form_builder(SitePreferenceForm, preferences, **kwargs)`
    """
    return preference_form_builder(SitePreferenceForm, preferences, **kwargs)


class PreferenceForm(forms.Form):
    registry = None

    def update_preferences(self, **kwargs):
        for instance in self.instances:
            instance.value = self.cleaned_data[instance.preference.identifier()]
            instance.save()


class GlobalPreferenceForm(PreferenceForm):
    registry = global_preferences_registry


class UserPreferenceForm(PreferenceForm):
    registry = user_preferences_registry


class SitePreferenceForm(PreferenceForm):
    registry = site_preferences_registry


class OptimisedClearableFileInput(forms.ClearableFileInput):

    template_with_initial = (
        '%(initial_text)s: <a href="%(initial_url)s">%(initial)s</a> <br>'
        '<span class="clear-file"> %(clear_template)s</span> <span>%(input_text)s: %(input)s </span>'
    )

    clear_checkbox_label = ugettext_lazy('Remove this file')

    template_with_clear = '%(clear)s %(clear_checkbox_label)s -'

    def __init__(self, *args, **kwargs):
        super(OptimisedClearableFileInput, self).__init__(*args, **kwargs)

    def is_initial(self, value):
        """
        Return whether value is considered to be initial value.
        """
        return bool(value)

    def get_template_substitution_values(self, value):
        """
        Return value-related substitutions.
        """
        return {
            'initial': conditional_escape(value),
            'initial_url': conditional_escape(value),
        }

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': 'File name',
            'input_text': 'File',
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        substitutions['input'] = super(forms.ClearableFileInput, self).render(name, value, attrs)

        if self.is_initial(value):
            template = self.template_with_initial
            substitutions.update(self.get_template_substitution_values(value))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = '<input type="checkbox" id="%(id)s" name="%(name)s">' % {
                    'id': substitutions['clear_checkbox_id'],
                    'name': substitutions['clear_checkbox_name'],
                }
                substitutions['clear_template'] = self.template_with_clear % substitutions
        return mark_safe(template % substitutions)
