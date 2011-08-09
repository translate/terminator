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



class ExportForm(forms.Form):
    from_glossary = forms.ModelMultipleChoiceField(queryset=Glossary.objects.all())
    #also_non_finalized_concepts = forms.BooleanField(required=False)
    export_not_finalized_definitions = forms.BooleanField(required=False)
    export_admitted_translations = forms.BooleanField(required=False)
    export_not_recommended_translations = forms.BooleanField(required=False)
    export_not_finalized_translations = forms.BooleanField(required=False)
    for_languages = forms.ModelMultipleChoiceField(queryset=Language.objects.all(), required=False)#TODO filtrar os idiomas presentes no glosario#TODO ou nube de checkboxes?
    
    def clean(self):
        super(forms.Form, self).clean()
        cleaned_data = self.cleaned_data
        export_admitted = cleaned_data.get("export_admitted_translations")
        export_not_recommended = cleaned_data.get("export_not_recommended_translations")
        export_not_finalized = cleaned_data.get("export_not_finalized_translations")
        
        if export_not_recommended and not export_admitted:
            msg = u"You cannot export not recommended translations unless you also export admitted translations."
            self._errors["export_not_recommended_translations"] = self.error_class([msg])
            # This field is no longer valid. Remove it from the cleaned data.
            del cleaned_data["export_not_recommended_translations"]
        
        if export_not_finalized and (not export_not_recommended or not export_admitted):
            msg = u"You cannot export not finalized translations unless you also export not recommended and admitted translations."
            self._errors["export_not_finalized_translations"] = self.error_class([msg])
            # This field is no longer valid. Remove it from the cleaned data.
            del cleaned_data["export_not_finalized_translations"]
        
        # Always return the full collection of cleaned data.
        return cleaned_data



class SubscribeForm(forms.Form):
    subscribe_to_this_glossary = forms.BooleanField(initial=False)



class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ('for_glossary', 'language', 'word', 'definition',)



class CollaborationRequestForm(forms.ModelForm):
    class Meta:
        model = CollaborationRequest
        fields = ('collaboration_role',)



class TerminatorConceptAdminForm(forms.ModelForm):
    class Meta:
        model = Concept
    
    def clean(self):
        super(forms.ModelForm, self).clean()
        
        cleaned_data = self.cleaned_data
        glossary = cleaned_data.get("glossary")
        subject_field = cleaned_data.get("subject_field")
        
        if subject_field and glossary:
            if not subject_field.glossary == glossary:
                msg = u"Specify only Subject fields that belong to the chosen glossary."
                self._errors["subject_field"] = self.error_class([msg])
                # This field is no longer valid. Remove it from the cleaned data.
                del cleaned_data["subject_field"]
            #TODO filtrar o caso de que o subject_field sexa o concepto para o que se define
        
        broader_concept = cleaned_data.get("broader_concept")
        if broader_concept and glossary:
            if not broader_concept.glossary == glossary:
                msg = u"Specify only Broader concepts that belong to the chosen glossary."
                self._errors["broader_concept"] = self.error_class([msg])
                # This field is no longer valid. Remove it from the cleaned data.
                del cleaned_data["broader_concept"]
            #TODO filtrar o caso de que o broader_concept sexa o concepto para o que se define
        
        related_concepts = cleaned_data.get("related_concepts")
        if related_concepts and glossary:
            for related_concept in related_concepts:
                if not related_concept.glossary == glossary:
                    msg = u"Specify only Related concepts that belong to the chosen glossary."
                    self._errors["related_concepts"] = self.error_class([msg])
                    # This field is no longer valid. Remove it from the cleaned data.
                    del cleaned_data["related_concepts"]
                #TODO filtrar o caso de que algún related_concept sexa o concepto para o que se define
        
        # Always return the full collection of cleaned data.
        return cleaned_data



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
        
        process_status = cleaned_data.get("process_status")
        # Check that the process_status is not set to True when the part of 
        # speech or the administrative status are not set.
        if process_status and (not administrative_status or not part_of_speech):
            msg = u"You cannot set 'is_finalized' to True unless an Administrative status and a Part of Speech are set."
            self._errors["process_status"] = self.error_class([msg])
            # This field is no longer valid. Remove it from the cleaned data.
            del cleaned_data["process_status"]
        
        # Always return the full collection of cleaned data.
        return cleaned_data



