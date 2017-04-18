# !/usr/bin/env python
# encoding:UTF-8

from django.contrib import admin
from dynamic_preferences.models import GlobalPreferenceModel, UserPreferenceModel
from django import forms
from dynamic_preferences.types import FilePreference


class PreferenceChangeListForm(forms.ModelForm):
    """
    A form that integrate dynamic-preferences into django.contrib.admin
    """
    # Me must use an acutal model field, so we use raw_value. However, 
    # instance.value will be displayed in form.
    raw_value = forms.CharField()

    def is_multipart(self):
        """
        Returns True if the form needs to be multipart-encoded, i.e. it has
        FileInput. Otherwise, False.
        """
        for section in self.instance.registry:
            for pref in self.instance.registry[section]:
                if isinstance(self.instance.registry[section][pref], FilePreference):
                    return True
        return False

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super(PreferenceChangeListForm, self).__init__(*args, **kwargs)
        self.fields['raw_value'] = self.instance.preference.setup_field()

    def save(self, *args, **kwargs):
        ikargs = {}
        if isinstance(self.instance.preference, FilePreference):
            ikargs['delete_filename'] = self.initial['raw_value']
        self.cleaned_data['raw_value'] = self.instance.preference.serializer.serialize(self.cleaned_data['raw_value'],
                                                                                       **ikargs)
        return super(PreferenceChangeListForm, self).save(*args, **kwargs)


class GlobalPreferenceChangeListForm(PreferenceChangeListForm):
    class Meta:
        model = GlobalPreferenceModel


class UserPreferenceChangeListForm(PreferenceChangeListForm):
    class Meta:
        model = UserPreferenceModel


class DynamicPreferenceAdmin(admin.ModelAdmin):
    changelist_form = PreferenceChangeListForm
    readonly_fields = ('section', 'name', 'value', 'help')
    fields = ("raw_value",)
    list_display = ['section', 'name', 'raw_value', 'help']
    list_display_links = ['name', ]
    list_editable = ('raw_value',)
    #search_fields = ['section', 'name', 'help']
    search_fields = []
    list_filter = ('section',)
    ordering = ('section', 'name')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        return []

    def get_changelist_form(self, request, **kwargs):
        return self.changelist_form

    # def get_search_results(self, request, queryset, search_term):
    #     queryset_original = queryset
    #     queryset, use_distinct = super(DynamicPreferenceAdmin, self).get_search_results(request, queryset, search_term)
    #     if not len(queryset):
    #         # self.message_user(request, "No result found for: '" + search_term + "'", messages.SUCCESS)
    #         queryset = queryset_original
    #     return queryset, use_distinct


class GlobalPreferenceAdmin(DynamicPreferenceAdmin):
    form = GlobalPreferenceChangeListForm
    changelist_form = GlobalPreferenceChangeListForm


admin.site.register(GlobalPreferenceModel, GlobalPreferenceAdmin)


class UserPreferenceAdmin(DynamicPreferenceAdmin):
    form = UserPreferenceChangeListForm
    changelist_form = UserPreferenceChangeListForm
    list_display = ['user'] + DynamicPreferenceAdmin.list_display
    #search_fields = ['user__username'] + DynamicPreferenceAdmin.search_fields
    search_fields = []


admin.site.register(UserPreferenceModel, UserPreferenceAdmin)
