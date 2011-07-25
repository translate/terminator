# -*- coding: UTF-8 -*-
from django import forms
from terminator.models import *


class SearchForm(forms.Form):
    search_string = forms.CharField(max_length=100, min_length=2)



class AdvancedSearchForm(SearchForm):
    also_show_partial_matches = forms.BooleanField(required=False)
    filter_by_glossary = forms.ModelChoiceField(queryset=Glossary.objects.all(), required=False)
    filter_by_language = forms.ModelChoiceField(queryset=Language.objects.all(), required=False)
    filter_by_part_of_speech = forms.ModelChoiceField(queryset=PartOfSpeech.objects.all(), required=False)
    filter_by_administrative_status = forms.ModelChoiceField(queryset=AdministrativeStatus.objects.all(), required=False)#TODO quizais sexa mellor poñer un checkbox por cada un ou un campo MultipleChoices (esixirían cambios na vista)



class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ('for_glossary', 'language', 'word', 'definition',)



class CollaborationRequestForm(forms.ModelForm):
    class Meta:
        model = CollaborationRequest
        fields = ('collaboration_role',)



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
        
        grammatical_gender = cleaned_data.get("grammatical_gender")
        # Check that Grammatical gender is only specified when is given a Part of speech
        if not part_of_speech and grammatical_gender:
            msg = u"Don't specify a Grammatical gender without specifying a Part of speech."
            self._errors["grammatical_gender"] = self.error_class([msg])
            # This field is no longer valid. Remove it from the cleaned data.
            del cleaned_data["grammatical_gender"]
        
        # Check that the Part of speech allows specifying a Grammatical 
        # gender for the chosen language, and check that the chosen language
        # allows using the specified Grammatical gender
        if language and part_of_speech and grammatical_gender:
            msg = u""
            if not part_of_speech.allows_grammatical_gender_for_language(language):
                msg = u"The specified Part of speech doesn't allow specifying a Grammatical gender for the chosen language."
            if not language.allows_grammatical_gender(grammatical_gender):
                msg += u"The chosen language doesn't allow specifying this Grammatical gender."
            if msg:
                self._errors["grammatical_gender"] = self.error_class([msg])
                # This field is no longer valid. Remove it from the cleaned data.
                del cleaned_data["grammatical_gender"]
        
        grammatical_number = cleaned_data.get("grammatical_number")
        # Check that Grammatical number is only specified when is given a Part of speech
        if not part_of_speech and grammatical_number:
            msg = u"Don't specify a Grammatical number without specifying a Part of speech."
            self._errors["grammatical_number"] = self.error_class([msg])
            # This field is no longer valid. Remove it from the cleaned data.
            del cleaned_data["grammatical_number"]
        
        # Check that the Part of speech allows specifying a Grammatical 
        # number for the chosen language, and check that the chosen language
        # allows using the specified Grammatical number
        if language and part_of_speech and grammatical_number:
            msg = u""
            if not part_of_speech.allows_grammatical_number_for_language(language):
                msg = u"The specified Part of speech doesn't allow specifying a Grammatical number for the chosen language."
            if not language.allows_grammatical_number(grammatical_number):
                msg += u"The chosen language doesn't allow specifying this Grammatical number."
            if msg:
                self._errors["grammatical_number"] = self.error_class([msg])
                # This field is no longer valid. Remove it from the cleaned data.
                del cleaned_data["grammatical_number"]
        
        administrative_status = cleaned_data.get("administrative_status")
        administrative_status_reason = cleaned_data.get("administrative_status_reason")
        # Check that Administrative status reason is only specified when is 
        # given an Administrative status
        if not administrative_status and administrative_status_reason:
            msg = u"Don't specify an Administrative status reason without specifying an Administrative status."
            self._errors["administrative_status_reason"] = self.error_class([msg])
            # This field is no longer valid. Remove it from the cleaned data.
            del cleaned_data["administrative_status_reason"]
        
        # Check that the Administrative status allows specifying an
        # Administrative status reason, and check that the chosen language
        # allows using the specified Administrative status reason
        if language and administrative_status and administrative_status_reason:
            msg = u""
            if not administrative_status.allows_setting_administrative_status_reason():
                msg = u"The specified Administrative status doesn't allow specifying an Administrative status reason."
            elif not language.allows_administrative_status_reason(administrative_status_reason):
                msg += u"The chosen language doesn't allow specifying this Administrative status reason."
            if msg:
                self._errors["administrative_status_reason"] = self.error_class([msg])
                # This field is no longer valid. Remove it from the cleaned data.
                del cleaned_data["administrative_status_reason"]
        
        # Always return the full collection of cleaned data.
        return cleaned_data



