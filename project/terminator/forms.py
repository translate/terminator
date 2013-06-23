# -*- coding: UTF-8 -*-
#
# Copyright 2011, 2013 Leandro Regueiro
#
# This file is part of Terminator.
#
# Terminator is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Terminator is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Terminator. If not, see <http://www.gnu.org/licenses/>.

from django import forms
from django.utils.translation import ugettext_lazy as _

from terminator.models import *


class SearchForm(forms.Form):
    search_string = forms.CharField(max_length=100, min_length=2, label=_("Search string"))


class AdvancedSearchForm(SearchForm):
    also_show_partial_matches = forms.BooleanField(required=False,
        label=_("Also show partial matches")
    )
    filter_by_glossary = forms.ModelChoiceField(
        queryset=Glossary.objects.all(), required=False,
        label=_("Filter by glossary")
    )
    filter_by_language = forms.ModelChoiceField(
        queryset=Language.objects.all(), required=False,
        label=_("Filter by language")
    )
    filter_by_part_of_speech = forms.ModelChoiceField(
        queryset=PartOfSpeech.objects.all(), required=False,
        label=_("Filter by part of speech")
    )
    #TODO Perhaps for the filter_by_administrative_status field it should be
    # better to put a checkbox for each one, or a MultipleChoices field. Both
    # approachs would require changes in the view.
    filter_by_administrative_status = forms.ModelChoiceField(
        queryset=AdministrativeStatus.objects.all(), required=False,
        label=_("Filter by administrative status")
    )


class ImportForm(forms.ModelForm):
    imported_file = forms.FileField(label=_("File"))

    class Meta:
        model = Glossary
        exclude = ('subscribers', 'subject_fields')

    def clean(self):
        super(forms.ModelForm, self).clean()
        cleaned_data = self.cleaned_data
        if Glossary.objects.filter(name=cleaned_data.get("name")):
            msg = _(u"Already exists a glossary with the given name. You should provide another one.")
            self._errors["name"] = self.error_class([msg])
            # This field is no longer valid. So remove it from the cleaned data.
            del cleaned_data["name"]
        # Always return the full collection of cleaned data.
        return cleaned_data


class ExportForm(forms.Form):
    from_glossaries = forms.ModelMultipleChoiceField(queryset=Glossary.objects.all(), label=_("From glossaries"))
    #also_not_finalized_concepts = forms.BooleanField(required=False, label=_("Also not finalized concepts"))
    export_not_finalized_definitions = forms.BooleanField(required=False, label=_("Export not finalized definitions"))
    export_admitted_translations = forms.BooleanField(required=False, label=_("Export admitted translations"))
    export_not_recommended_translations = forms.BooleanField(required=False, label=_("Export not recommended translations"))
    export_not_finalized_translations = forms.BooleanField(required=False, label=_("Export not finalized translations"))
    #TODO In the for_languages field show only the languages present on the
    # chosen glossaries. Perhaps show a cloud of checkboxes?
    for_languages = forms.ModelMultipleChoiceField(queryset=Language.objects.all(), required=False, label=_("For languages"))

    def clean(self):
        super(forms.Form, self).clean()
        cleaned_data = self.cleaned_data
        export_admitted = cleaned_data.get("export_admitted_translations")
        export_not_recommended = cleaned_data.get("export_not_recommended_translations")
        export_not_finalized = cleaned_data.get("export_not_finalized_translations")

        if export_not_recommended and not export_admitted:
            msg = _(u"You cannot export not recommended translations unless you also export admitted translations.")
            self._errors["export_not_recommended_translations"] = self.error_class([msg])
            # This field is no longer valid. So remove it from the cleaned data.
            del cleaned_data["export_not_recommended_translations"]

        if export_not_finalized and (not export_not_recommended or not export_admitted):
            msg = _(u"You cannot export not finalized translations unless you also export not recommended and admitted translations.")
            self._errors["export_not_finalized_translations"] = self.error_class([msg])
            # This field is no longer valid. So remove it from the cleaned data.
            del cleaned_data["export_not_finalized_translations"]

        # Always return the full collection of cleaned data.
        return cleaned_data


class SubscribeForm(forms.Form):
    subscribe_to_this_glossary = forms.BooleanField(initial=False, label=_("Subscribe to this glossary"))


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ('for_glossary', 'language', 'word', 'definition',)


class CollaborationRequestForm(forms.ModelForm):
    class Meta:
        model = CollaborationRequest
        fields = ('collaboration_role',)


class TerminatorGlossaryAdminForm(forms.ModelForm):
    class Meta:
        model = Glossary

    def clean(self):
        super(forms.ModelForm, self).clean()

        cleaned_data = self.cleaned_data
        name = cleaned_data.get("name")
        subject_fields = list(cleaned_data.get("subject_fields"))

        if subject_fields and name:
            glossary = Glossary.objects.get(name=name)
            for subject_field in subject_fields:
                if subject_field.glossary != glossary:
                    msg = _(u"Specify only concepts that belong to the chosen glossary.")
                    self._errors["subject_fields"] = self.error_class([msg])
                    # This field is no longer valid. So remove it from the
                    # cleaned data.
                    del cleaned_data["subject_fields"]
                    break
            #TODO When removing a subject field from the list of subject
            # fields for a given glossary make sure that this concept is not
            # the subject field or other concepts in the glossary.

        # Always return the full collection of cleaned data.
        return cleaned_data


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
                msg = _(u"Specify only Subject fields that belong to the chosen glossary.")
                self._errors["subject_field"] = self.error_class([msg])
                # This field is no longer valid. So remove it from the cleaned
                # data.
                del cleaned_data["subject_field"]
            elif not subject_field in subject_field.glossary.subject_fields.all():
                msg = _(u"Specify only Subject fields that belong to the chosen glossary available subject fields.")
                self._errors["subject_field"] = self.error_class([msg])
                # This field is no longer valid. So remove it from the cleaned
                # data.
                del cleaned_data["subject_field"]
            #TODO Filter the case in which the concept sets itself as its
            # subject_field.

        broader_concept = cleaned_data.get("broader_concept")
        if broader_concept and glossary:
            if not broader_concept.glossary == glossary:
                msg = _(u"Specify only Broader concepts that belong to the chosen glossary.")
                self._errors["broader_concept"] = self.error_class([msg])
                # This field is no longer valid. So remove it from the cleaned
                # data.
                del cleaned_data["broader_concept"]
            #TODO Filter the case in which the concept sets itself as its
            # broader_concept.

        related_concepts = cleaned_data.get("related_concepts")
        if related_concepts and glossary:
            for related_concept in related_concepts:
                if not related_concept.glossary == glossary:
                    msg = _(u"Specify only Related concepts that belong to the chosen glossary.")
                    self._errors["related_concepts"] = self.error_class([msg])
                    # This field is no longer valid. So remove it from the
                    # cleaned data.
                    del cleaned_data["related_concepts"]
                #TODO Filter the case in which the concept sets itself as one
                # of its related_concept.

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

        # Check that the specified Part of Speech is allowed by the chosen
        # language.
        if language and part_of_speech:
            # Only do something if both fields are valid so far.
            if not language.allows_part_of_speech(part_of_speech):
                msg = _(u"Specify only Parts of speech allowed by the chosen language.")
                self._errors["part_of_speech"] = self.error_class([msg])
                # This field is no longer valid. So remove it from the cleaned
                # data.
                del cleaned_data["part_of_speech"]

        grammatical_gender = cleaned_data.get("grammatical_gender")
        # Check that Grammatical Gender is only specified when is given a Part
        # of Speech.
        if not part_of_speech and grammatical_gender:
            msg = _(u"Don't specify a Grammatical gender without specifying a Part of speech.")
            self._errors["grammatical_gender"] = self.error_class([msg])
            # This field is no longer valid. So remove it from the cleaned data.
            del cleaned_data["grammatical_gender"]

        # Check that the Part of Speech allows specifying a Grammatical Gender
        # for the chosen language, and check that the chosen language allows
        # using the specified Grammatical Gender.
        if language and part_of_speech and grammatical_gender:
            msg = u""
            if not part_of_speech.allows_grammatical_gender_for_language(language):
                msg = _(u"The specified Part of speech doesn't allow specifying a Grammatical gender for the chosen language.")
            if not language.allows_grammatical_gender(grammatical_gender):
                msg += _(u"The chosen language doesn't allow specifying this Grammatical gender.")
            if msg:
                self._errors["grammatical_gender"] = self.error_class([msg])
                # This field is no longer valid. So remove it from the cleaned
                # data.
                del cleaned_data["grammatical_gender"]

        grammatical_number = cleaned_data.get("grammatical_number")
        # Check that Grammatical Number is only specified when is given a Part
        # of Speech.
        if not part_of_speech and grammatical_number:
            msg = _(u"Don't specify a Grammatical number without specifying a Part of speech.")
            self._errors["grammatical_number"] = self.error_class([msg])
            # This field is no longer valid. So remove it from the cleaned data.
            del cleaned_data["grammatical_number"]

        # Check that the Part of Speech allows specifying a Grammatical Number
        # for the chosen language, and check that the chosen language allows
        # using the specified Grammatical Number.
        if language and part_of_speech and grammatical_number:
            msg = u""
            if not part_of_speech.allows_grammatical_number_for_language(language):
                msg = _(u"The specified Part of speech doesn't allow specifying a Grammatical number for the chosen language.")
            if not language.allows_grammatical_number(grammatical_number):
                msg += _(u"The chosen language doesn't allow specifying this Grammatical number.")
            if msg:
                self._errors["grammatical_number"] = self.error_class([msg])
                # This field is no longer valid. So remove it from the cleaned
                # data.
                del cleaned_data["grammatical_number"]

        administrative_status = cleaned_data.get("administrative_status")
        administrative_status_reason = cleaned_data.get("administrative_status_reason")
        # Check that Administrative Status Reason is only specified when is
        # given an Administrative Status.
        if not administrative_status and administrative_status_reason:
            msg = _(u"Don't specify an Administrative status reason without specifying an Administrative status.")
            self._errors["administrative_status_reason"] = self.error_class([msg])
            # This field is no longer valid. So remove it from the cleaned data.
            del cleaned_data["administrative_status_reason"]

        # Check that the Administrative Status allows specifying an
        # Administrative Status Reason, and check that the chosen language
        # allows using the specified Administrative Status Reason.
        if language and administrative_status and administrative_status_reason:
            msg = u""
            if not administrative_status.allows_administrative_status_reason:
                msg = _(u"The specified Administrative status doesn't allow specifying an Administrative status reason.")
            elif not language.allows_administrative_status_reason(administrative_status_reason):
                msg += _(u"The chosen language doesn't allow specifying this Administrative status reason.")
            if msg:
                self._errors["administrative_status_reason"] = self.error_class([msg])
                # This field is no longer valid. So remove it from the cleaned
                # data.
                del cleaned_data["administrative_status_reason"]

        process_status = cleaned_data.get("process_status")
        # Check that the process_status is not set to True when the Part of
        # Speech or the Administrative Status are not set.
        if process_status and (not administrative_status or not part_of_speech):
            msg = _(u"You cannot set 'is finalized' to True unless an Administrative status and a Part of Speech are set.")
            self._errors["process_status"] = self.error_class([msg])
            # This field is no longer valid. So remove it from the cleaned data.
            del cleaned_data["process_status"]

        # Always return the full collection of cleaned data.
        return cleaned_data
