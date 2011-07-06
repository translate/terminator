# -*- coding: UTF-8 -*-
from django import forms
from terminator.models import *


class SearchForm(forms.Form):
    search_string = forms.CharField(max_length=100, min_length=2, required=False)


class TerminatorTranslationAdminForm(forms.ModelForm):
    class Meta:
        model = Translation
    
    def clean(self):
        super(forms.ModelForm, self).clean()
        
        cleaned_data = self.cleaned_data
        language = cleaned_data.get("language")
        part_of_speech = cleaned_data.get("part_of_speech")
        
        # Check that the specified part of speech is allowed by the chosen language
        if language and part_of_speech:
            # Only do something if both fields are valid so far.
            if not language.allows_part_of_speech(part_of_speech):
                msg = u"Specify only Parts of speech allowed by the chosen language."
                self._errors["part_of_speech"] = self.error_class([msg])
                # This field is no longer valid. Remove it from the cleaned data.
                del cleaned_data["part_of_speech"]
        
        # Always return the full collection of cleaned data.
        return cleaned_data



