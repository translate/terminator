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

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from guardian.shortcuts import assign


@receiver(post_save, sender=User, dispatch_uid="user_profile_creation_handler_unique_identifier")
def user_profile_creation_handler(sender, instance, created, **kwargs):
    if created:
        # Django-guardian requires that anonymous_user should have an id=-1 so
        # check this to not create a user_profile for anonymous_user.
        if instance.pk > 0:
            UserProfile.objects.get_or_create(user=instance)


class PartOfSpeech(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("name"))
    tbx_representation = models.CharField(max_length=100, verbose_name=_("TBX representation"))
    description = models.TextField(blank=True, verbose_name=_("description"))

    class Meta:
        verbose_name = _("part of speech")
        verbose_name_plural = _("parts of speech")

    def __unicode__(self):
        return self.name

    def allows_grammatical_gender_for_language(self, language):
        try:
            response = self.partofspeechforlanguage_set.get(language=language).allows_grammatical_gender
        except ObjectDoesNotExist:
            response = False
        return response

    def allows_grammatical_number_for_language(self, language):
        try:
            response = self.partofspeechforlanguage_set.get(language=language).allows_grammatical_number
        except ObjectDoesNotExist:
            response = False
        return response


class GrammaticalGender(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("name"))
    tbx_representation = models.CharField(max_length=100, verbose_name=_("TBX representation"))
    description = models.TextField(blank=True, verbose_name=_("description"))

    class Meta:
        verbose_name = _("grammatical gender")
        verbose_name_plural = _("grammatical genders")

    def __unicode__(self):
        return self.name


class GrammaticalNumber(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("name"))
    tbx_representation = models.CharField(max_length=100, verbose_name=_("TBX representation"))
    description = models.TextField(blank=True, verbose_name=_("description"))

    class Meta:
        verbose_name = _("grammatical number")
        verbose_name_plural = _("grammatical numbers")

    def __unicode__(self):
        return self.name


class Language(models.Model):
    iso_code = models.CharField(primary_key=True, max_length=10, verbose_name=_("ISO code"))
    name = models.CharField(max_length=50, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    parts_of_speech = models.ManyToManyField(PartOfSpeech, through='PartOfSpeechForLanguage', verbose_name=_("parts of speech"))
    grammatical_genders = models.ManyToManyField(GrammaticalGender, verbose_name=_("grammatical genders"))
    grammatical_numbers = models.ManyToManyField(GrammaticalNumber, verbose_name=_("grammatical numbers"))

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")

    def __unicode__(self):
        return unicode(_(u"%(language_name)s (%(iso_code)s)" % {'language_name': self.name, 'iso_code': self.iso_code}))

    def allows_part_of_speech(self, part_of_speech):
        return part_of_speech in self.parts_of_speech.all()

    def allows_grammatical_gender(self, grammatical_gender):
        return grammatical_gender in self.grammatical_genders.all()

    def allows_grammatical_number(self, grammatical_number):
        return grammatical_number in self.grammatical_numbers.all()

    def allows_administrative_status_reason(self, administrative_status_reason):
        return administrative_status_reason in self.administrativestatusreason_set.all()


class PartOfSpeechForLanguage(models.Model):
    language = models.ForeignKey(Language, verbose_name=_("language"))
    part_of_speech = models.ForeignKey(PartOfSpeech, verbose_name=_("part of speech"))
    allows_grammatical_gender = models.BooleanField(default=False, verbose_name=_("allows grammatical gender"))
    allows_grammatical_number = models.BooleanField(default=False, verbose_name=_("allows grammatical number"))

    class Meta:
        verbose_name_plural = _("parts of speech for languages")
        unique_together = ("language", "part_of_speech")

    def __unicode__(self):
        return unicode(_(u"%(part_of_speech)s (%(language)s)" % {'part_of_speech': self.part_of_speech, 'language': self.language}))


class AdministrativeStatus(models.Model):
    name = models.CharField(max_length=20, verbose_name=_("name"))
    tbx_representation = models.CharField(primary_key=True, max_length=25, verbose_name=_("TBX representation"))
    description = models.TextField(blank=True, verbose_name=_("description"))
    allows_administrative_status_reason = models.BooleanField(default=False, verbose_name=_("allows setting administrative status reason"))

    class Meta:
        verbose_name = _("administrative status")
        verbose_name_plural = _("administrative statuses")

    def __unicode__(self):
        return self.name


class AdministrativeStatusReason(models.Model):
    languages = models.ManyToManyField(Language, verbose_name=_("languages"))
    name = models.CharField(max_length=40, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))

    class Meta:
        verbose_name = _("administrative status reason")
        verbose_name_plural = _("administrative status reasons")

    def __unicode__(self):
        return self.name


class ExternalLinkType(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("name"))
    tbx_representation = models.CharField(primary_key=True, max_length=30, verbose_name=_("TBX representation"))
    description = models.TextField(verbose_name=_("description"))

    class Meta:
        verbose_name = _("external link type")
        verbose_name_plural = _("external link types")

    def __unicode__(self):
        return self.name


class Glossary(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    subscribers = models.ManyToManyField(User, null=True, blank=True, verbose_name=_("subscribers"))
    #main_language #TODO this should be the main language of the glossary. This language is used when exporting the glossary and is also the language in which the glossary name and description are written.
    #accepted_languages #TODO this should be a list of languages that can be used in the glossary. If this is finally used should be restricted for translations, definitions, external resources, proposals, ConceptLanguageCommentsThread,... in the Glossary.
    #TODO In the subject_fields field, when trying to remove a concept from the
    # subject_fields of a Glossary make sure before that it is not used as
    # subject field for any of the Glossary concepts.
    #TODO In the subject_fields field, see if is an option using
    # limit_choices_to = {'glossary__exact': self} in order to reduce the
    # options shown in the admin site.
    subject_fields = models.ManyToManyField('Concept', related_name='glossary_subject_fields', null=True, blank=True, verbose_name=_("subject fields"))

    class Meta:
        verbose_name = _("glossary")
        verbose_name_plural = _("glossaries")
        permissions = (
            ('is_terminologist_in_this_glossary', 'Is terminologist in this glossary'),
            ('is_lexicographer_in_this_glossary', 'Is lexicographer in this glossary'),
            ('is_owner_for_this_glossary', 'Is owner for this glossary'),
        )

    def __unicode__(self):
        return self.name

    def assign_terminologist_permissions(self, user):
        assign('is_terminologist_in_this_glossary', user, self)
        # Assign permissions over translations
        assign('terminator.add_translation', user)
        assign('terminator.change_translation', user)
        assign('terminator.delete_translation', user)
        # Assign permissions over definitions
        assign('terminator.add_definition', user)
        assign('terminator.change_definition', user)
        assign('terminator.delete_definition', user)
        # Assign permissions over external resources
        assign('terminator.add_externalresource', user)
        assign('terminator.change_externalresource', user)
        assign('terminator.delete_externalresource', user)
        # Assign permissions over context sentences
        assign('terminator.add_contextsentence', user)
        assign('terminator.change_contextsentence', user)
        assign('terminator.delete_contextsentence', user)
        # Assign permissions over corpus examples
        assign('terminator.add_corpusexample', user)
        assign('terminator.change_corpusexample', user)
        assign('terminator.delete_corpusexample', user)

    def assign_lexicographer_permissions(self, user):
        assign('is_lexicographer_in_this_glossary', user, self)
        # Assign permissions over concepts
        assign('terminator.add_concept', user)
        assign('terminator.change_concept', user)
        assign('terminator.delete_concept', user)
        # Assign permissions over proposals
        assign('terminator.change_proposal', user)
        assign('terminator.delete_proposal', user)

    def assign_owner_permissions(self, user):
        assign('is_owner_for_this_glossary', user, self)
        # Assign permissions over glossaries
        #assign('terminator.add_glossary', user)
        assign('terminator.change_glossary', user)
        assign('terminator.delete_glossary', user)
        # Assign permissions over collaboration requests
        assign('terminator.change_collaborationrequest', user)
        assign('terminator.delete_collaborationrequest', user)


class Concept(models.Model):
    glossary = models.ForeignKey(Glossary, verbose_name=_("glossary"))
    subject_field = models.ForeignKey('self', related_name='concepts_in_subject_field', null=True, blank=True, on_delete=models.PROTECT, verbose_name=_("subject field"))
    broader_concept = models.ForeignKey('self', related_name='narrower_concepts', null=True, blank=True, on_delete=models.PROTECT, verbose_name=_("broader concept"))
    related_concepts = models.ManyToManyField('self', null=True, blank=True, verbose_name=_("related concepts"))

    class Meta:
        verbose_name = _("concept")
        verbose_name_plural = _("concepts")

    def __unicode__(self):
        return unicode(_(u"Concept #%(concept_id)d" % {'concept_id': self.id}))

    def get_list_of_used_languages(self):
        language_set = set()
        for translation in self.translation_set.all():
            language_set.add(translation.language_id)
        for external_resource in self.externalresource_set.all():
            language_set.add(external_resource.language_id)
        for definition in self.definition_set.all():
            language_set.add(definition.language_id)
        used_languages_list = list(language_set)
        used_languages_list.sort()
        return used_languages_list

    def get_english_translation(self):
        english = Language.objects.get(pk="en")
        preferred = AdministrativeStatus.objects.get(pk="preferredTerm-admn-sts")
        english_translation = self.translation_set.filter(language=english, administrative_status=preferred)
        # If there is no english preferred translation return any english
        # translation with no Administrative Status set.
        if len(english_translation):
            english_translation = self.translation_set.filter(language=english, administrative_status=None)
        return english_translation


class ConceptLanguageCommentsThread(models.Model):
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("concept", "language")

    def __unicode__(self):
        return unicode(_(u"%(language)s comment thread for %(concept)s" % {'language': self.language, 'concept': self.concept}))

    @models.permalink
    def get_absolute_url(self):
        return ('terminator_concept_detail_for_language', (), {'pk': unicode(self.concept.pk), 'lang': self.language.pk})


class SummaryMessage(models.Model):
    concept = models.ForeignKey(Concept, verbose_name=_("concept"))
    language = models.ForeignKey(Language, on_delete=models.PROTECT, verbose_name=_("language"))
    text = models.TextField(verbose_name=_("summary message text"))
    is_finalized = models.BooleanField(default=False, verbose_name=_("is finalized"))
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("summary message")
        verbose_name_plural = _("summary messages")
        unique_together = ("concept", "language")

    def __unicode__(self):
        trans_data = {
            'language': self.language,
            'concept': self.concept,
            'text': self.text[:200]
        }
        return unicode(_(u"Summary message for %(language)s and %(concept)s: (%(text)s)" % trans_data))


class Translation(models.Model):
    concept = models.ForeignKey(Concept, verbose_name=_("concept"))
    language = models.ForeignKey(Language, on_delete=models.PROTECT, verbose_name=_("language"))
    translation_text = models.CharField(max_length=100, verbose_name=_("translation text"))
    process_status = models.BooleanField(default=False, verbose_name=_("Is finalized"))
    administrative_status = models.ForeignKey(AdministrativeStatus, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("administrative status"))
    administrative_status_reason = models.ForeignKey(AdministrativeStatusReason, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("administrative status reason"))
    part_of_speech = models.ForeignKey(PartOfSpeech, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("part of speech"))
    grammatical_gender = models.ForeignKey(GrammaticalGender, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("grammatical gender"))
    grammatical_number = models.ForeignKey(GrammaticalNumber, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("grammatical number"))
    note = models.TextField(blank=True)

    class Meta:
        verbose_name = _("translation")
        verbose_name_plural = _("translations")
        ordering = ['concept', 'language']

    def __unicode__(self):
        trans_data = {
            'translation': self.translation_text,
            'iso_code': self.language.iso_code,
            'concept': self.concept
        }
        return unicode(_(u"%(translation)s (%(iso_code)s) for %(concept)s" % trans_data))


class Definition(models.Model):
    concept = models.ForeignKey(Concept, verbose_name=_("concept"))
    language = models.ForeignKey(Language, on_delete=models.PROTECT, verbose_name=_("language"))
    definition_text = models.TextField(verbose_name=_("definition text"))
    is_finalized = models.BooleanField(default=False, verbose_name=_("is finalized"))
    source = models.URLField(blank=True, verbose_name=_("source"))

    class Meta:
        verbose_name = _("definition")
        verbose_name_plural = _("definitions")
        unique_together = ("concept", "language")

    def __unicode__(self):
        trans_data = {
            'language': self.language,
            'concept': self.concept,
            'definition_text': self.definition_text[:200]
        }
        return unicode(_(u"Definition in %(language)s for %(concept)s: (%(definition_text)s)" % trans_data))


class ExternalResource(models.Model):
    concept = models.ForeignKey(Concept, verbose_name=_("concept"))
    language = models.ForeignKey(Language, on_delete=models.PROTECT, verbose_name=_("language"))
    address = models.URLField(verbose_name=_("address"))
    link_type = models.ForeignKey(ExternalLinkType, on_delete=models.PROTECT, verbose_name=_("link type"))
    description = models.TextField(blank=True, verbose_name=_("description"))

    class Meta:
        verbose_name = _("external resource")
        verbose_name_plural = _("external resources")

    def __unicode__(self):
        return unicode(_(u"%(address)s (%(language)s) for %(concept)s" % {'address': self.address, 'language': self.language, 'concept': self.concept}))


class Proposal(models.Model):
    language = models.ForeignKey(Language, on_delete=models.PROTECT, verbose_name=_("language"))
    word = models.CharField(max_length=100, verbose_name=_("word"))
    definition = models.TextField(verbose_name=_("definition"))
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_("user"))
    sent_date = models.DateTimeField(auto_now_add=True, verbose_name=_("sent date"))
    for_glossary = models.ForeignKey(Glossary, on_delete=models.PROTECT, verbose_name=_("for glossary"))

    class Meta:
        verbose_name = _("proposal")
        verbose_name_plural = _("proposals")

    def __unicode__(self):
        return unicode(_(u"%(proposed_word)s (%(language)s)" % {'proposed_word': self.word, 'language': self.language}))


class ContextSentence(models.Model):
    translation = models.ForeignKey(Translation, verbose_name=_("translation"))
    # NOTE: Changed the text field from TextField to Charfield limited to 250
    # chars due to MySQL constraints.
    text = models.CharField(max_length=250, verbose_name=_("text"))
    #source = models.URLField(blank=True, verbose_name=_("source"))#TODO

    class Meta:
        verbose_name = _("context sentence")
        verbose_name_plural = _("context sentences")
        unique_together = ("translation", "text")

    def __unicode__(self):
        trans_data = {
            'sentence': self.text,
            'translation': self.translation
        }
        return unicode(_(u"%(sentence)s for translation %(translation)s" % trans_data))


class CorpusExample(models.Model):
    translation = models.ForeignKey(Translation, verbose_name=_("translation"))
    address = models.URLField(verbose_name=_("address"))
    description = models.TextField(blank=True, verbose_name=_("description"))

    class Meta:
        verbose_name = _("corpus example")
        verbose_name_plural = _("corpus examples")
        unique_together = ("translation", "address")

    def __unicode__(self):
        trans_data = {'address': self.address[:80], 'translation': self.translation}
        return unicode(_(u"%(address)s for translation %(translation)s" % trans_data))


class CollaborationRequest(models.Model):
    COLLABORATION_ROLE_CHOICES = (
        (u'O', _(u'Glossary owner')),
        (u'L', _(u'Lexicographer')),
        (u'T', _(u'Terminologist')),
    )
    collaboration_role = models.CharField(max_length=2, choices=COLLABORATION_ROLE_CHOICES, verbose_name=_("collaboration role"))
    user = models.ForeignKey(User, verbose_name=_("user"))
    sent_date = models.DateTimeField(auto_now_add=True, verbose_name=_("sent date"))
    for_glossary = models.ForeignKey(Glossary, on_delete=models.PROTECT, verbose_name=_("for glossary"))

    class Meta:
        verbose_name = _("collaboration request")
        verbose_name_plural = _("collaboration requests")
        unique_together = ("user", "for_glossary", "collaboration_role")

    def __unicode__(self):
        trans_data = {
            'user': self.user,
            'role': self.get_collaboration_role_display(),
            'glossary': self.for_glossary
        }
        return unicode(_(u"%(user)s requested %(role)s for %(glossary)s" % trans_data))


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("user"))
    is_public = models.BooleanField(default=True, verbose_name=_("is public"))
    preferred_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("preferred language"))

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
