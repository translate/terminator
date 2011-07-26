# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class PartOfSpeech(models.Model):
    name = models.CharField(max_length=50)
    tbx_representation = models.CharField(max_length=100, verbose_name="TBX representation")
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "parts of speech"
    
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
    name = models.CharField(max_length=50)
    tbx_representation = models.CharField(max_length=100, verbose_name="TBX representation")
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name


class GrammaticalNumber(models.Model):
    name = models.CharField(max_length=50)
    tbx_representation = models.CharField(max_length=100, verbose_name="TBX representation")
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name


class Language(models.Model):
    iso_code = models.CharField(max_length=10, primary_key=True, verbose_name="ISO code")
    name = models.CharField(max_length=50)
    description = models.TextField()
    parts_of_speech = models.ManyToManyField(PartOfSpeech, through='PartOfSpeechForLanguage')
    grammatical_genders = models.ManyToManyField(GrammaticalGender)
    grammatical_numbers = models.ManyToManyField(GrammaticalNumber)
    
    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.iso_code)
    
    def allows_part_of_speech(self, part_of_speech):
        return part_of_speech in self.parts_of_speech.all()
    
    def allows_grammatical_gender(self, grammatical_gender):
        return grammatical_gender in self.grammatical_genders.all()
    
    def allows_grammatical_number(self, grammatical_number):
        return grammatical_number in self.grammatical_numbers.all()
    
    def allows_administrative_status_reason(self, administrative_status_reason):
        return administrative_status_reason in self.administrativestatusreason_set.all()


class PartOfSpeechForLanguage(models.Model):
    language = models.ForeignKey(Language)
    part_of_speech = models.ForeignKey(PartOfSpeech)
    allows_grammatical_gender = models.BooleanField(default=False)
    allows_grammatical_number = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "parts of speech for languages"
        unique_together = ("language", "part_of_speech")
    
    def __unicode__(self):
        return u'%s (%s)' % (self.part_of_speech, self.language)


class Glossary(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = "glossaries"
        permissions = (
            ('is_terminologist_in_this_glossary', 'Is terminologist in this glossary'),
            ('is_lexicographer_in_this_glossary', 'Is lexicographer in this glossary'),
            ('is_owner_for_this_glossary', 'Is owner for this glossary'),
        )
    
    def __unicode__(self):
        return self.name


class Concept(models.Model):
    glossary = models.ForeignKey(Glossary)
    subject_field = models.ForeignKey('self', related_name='concepts_in_subject_field', null=True, blank=True, on_delete=models.PROTECT)
    broader_concept = models.ForeignKey('self', related_name='narrower_concepts', null=True, blank=True, on_delete=models.PROTECT)
    related_concepts = models.ManyToManyField('self', null=True, blank=True)
    
    def __unicode__(self):
        return u'Concept #%s' % (unicode(self.id))


class AdministrativeStatus(models.Model):
    name = models.CharField(max_length=20)
    tbx_representation = models.CharField(max_length=25, verbose_name="TBX representation", primary_key=True)
    description = models.TextField(blank=True)
    allows_administrative_status_reason = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "administrative statuses"
    
    def __unicode__(self):
        return self.name
    
    def allows_setting_administrative_status_reason(self):
        return self.allows_administrative_status_reason


class AdministrativeStatusReason(models.Model):
    languages = models.ManyToManyField(Language)
    name = models.CharField(max_length=40)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = "administrative status reasons"
    
    def __unicode__(self):
        return self.name


class Translation(models.Model):
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    translation_text = models.CharField(max_length=100)
    process_status = models.BooleanField(verbose_name="Is finalized", default=False)
    administrative_status = models.ForeignKey(AdministrativeStatus, null=True, blank=True, on_delete=models.SET_NULL)
    administrative_status_reason = models.ForeignKey(AdministrativeStatusReason, null=True, blank=True, on_delete=models.SET_NULL)
    part_of_speech = models.ForeignKey(PartOfSpeech, null=True, blank=True, on_delete=models.SET_NULL)
    grammatical_gender = models.ForeignKey(GrammaticalGender, null=True, blank=True, on_delete=models.SET_NULL)
    grammatical_number = models.ForeignKey(GrammaticalNumber, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.TextField(blank=True)
    
    class Meta:
        ordering = ['concept']
    
    def __unicode__(self):
        return u'%s (%s) for %s' % (self.translation_text, self.language.iso_code, self.concept)


class Definition(models.Model):
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    definition_text = models.TextField()
    is_finalized = models.BooleanField(default=False)
    source = models.URLField(blank=True)
    
    class Meta:
        unique_together = ("concept", "language")
    
    def __unicode__(self):
        return u'Definition in %s for %s: %s' % (self.language, self.concept, self.definition_text[:200])


class Proposal(models.Model):
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    word = models.CharField(max_length=100)
    definition = models.TextField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    sent_date = models.DateTimeField(auto_now_add=True)
    for_glossary = models.ForeignKey(Glossary, on_delete=models.PROTECT)
    
    def __unicode__(self):
        return u'%s (%s)' % (self.word, self.language)


class ExternalLinkType(models.Model):
    name = models.CharField(max_length=50)
    tbx_representation = models.CharField(max_length=30, verbose_name="TBX representation", primary_key=True)
    description = models.TextField()
    
    def __unicode__(self):
        return u'%s' % self.name


class ExternalResource(models.Model):
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    address = models.URLField()
    link_type = models.ForeignKey(ExternalLinkType, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return u'%s (%s) for %s' % (self.address, self.language, self.concept)


class ContextSentence(models.Model):
    translation = models.ForeignKey(Translation)
    text = models.TextField()
    
    class Meta:
        unique_together = ("translation", "text")
    
    def __unicode__(self):
        return u'%s for %s' % (self.text, self.translation)


class CorpusExample(models.Model):
    translation = models.ForeignKey(Translation)
    address = models.URLField()
    description = models.TextField(blank=True)
    
    class Meta:
        unique_together = ("translation", "address")
    
    def __unicode__(self):
        return u'%s for %s' % (self.address, self.translation)


class CollaborationRequest(models.Model):
    COLLABORATION_ROLE_CHOICES = (
        (u'O', u'Glossary owner'),
        (u'L', u'Lexicographer'),
        (u'T', u'Terminologist'),
    )
    collaboration_role = models.CharField(max_length=2, choices=COLLABORATION_ROLE_CHOICES)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    sent_date = models.DateTimeField(auto_now_add=True)
    for_glossary = models.ForeignKey(Glossary, on_delete=models.PROTECT)
    
    class Meta:
        unique_together = ("user", "for_glossary", "collaboration_role")
    
    def __unicode__(self):
        return u'%s requested %s for %s' % (self.user, self.collaboration_role, self.for_glossary)


