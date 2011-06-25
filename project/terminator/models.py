# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User


class PartOfSpeech(models.Model):
    name = models.CharField(max_length=50)
    tbx_representation = models.CharField(max_length=100, verbose_name="TBX representation")
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "parts of speech"
    
    def __unicode__(self):
        return self.name


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


class PartOfSpeechForLanguage(models.Model):
    language = models.ForeignKey(Language)
    part_of_speech = models.ForeignKey(PartOfSpeech)
    allows_grammatical_gender = models.BooleanField(blank=False, default=False)
    allows_grammatical_number = models.BooleanField(blank=False, default=False)
    
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
    
    def __unicode__(self):
        return self.name


class Concept(models.Model):
    id = models.AutoField(primary_key=True) 
    glossary = models.ForeignKey(Glossary)
    subject_field = models.ForeignKey('self', related_name='concepts_in_subject_field', null=True, blank=True)
    broader_concept = models.ForeignKey('self', related_name='narrower_concepts', null=True, blank=True)
    related_concepts = models.ManyToManyField('self', null=True, blank=True)
    
    def __unicode__(self):
        return u'Concept #%s' % (unicode(self.id))


class AdministrativeStatus(models.Model):
    name = models.CharField(max_length=20)
    tbx_representation = models.CharField(max_length=25, verbose_name="TBX representation", primary_key=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "administrative statuses"
    
    def __unicode__(self):
        return self.name


class Translation(models.Model):
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language)
    translation_text = models.CharField(max_length=100)
    process_status = models.BooleanField(blank=False, default=False)
    administrative_status = models.ForeignKey(AdministrativeStatus, null=True, blank=True)
    part_of_speech = models.ForeignKey(PartOfSpeech, null=True, blank=True)
    grammatical_gender = models.ForeignKey(GrammaticalGender, null=True, blank=True)
    grammatical_number = models.ForeignKey(GrammaticalNumber, null=True, blank=True)
    note = models.TextField(blank=True)
    
    def __unicode__(self):
        return u'%s (%s) for %s' % (self.translation_text, self.language, self.concept)


class Definition(models.Model):
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language)
    definition_text = models.TextField()
    source = models.URLField(blank=True)
    
    class Meta:
        unique_together = ("concept", "language")
    
    def __unicode__(self):
        return u'Definition in %s for %s: %s' % (self.language, self.concept, self.definition_text[:200])


class Proposal(models.Model):
    language = models.ForeignKey(Language)
    word = models.CharField(max_length=100)
    definition = models.TextField()
    user = models.ForeignKey(User)
    sent_date = models.DateTimeField()
    
    def __unicode__(self):
        return u'%s (%s)' % (self.word, self.language)


class ExternalLinkType(models.Model):
    name = models.CharField(max_length=50)
    tbx_representation = models.CharField(max_length=30, verbose_name="TBX representation")
    description = models.TextField()
    
    def __unicode__(self):
        return u'%s' % self.name


class ExternalResource(models.Model):
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language)
    address = models.URLField()
    link_type = models.ForeignKey(ExternalLinkType)
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


