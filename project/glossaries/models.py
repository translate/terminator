# -*- coding: UTF-8 -*-
from django.db import models

class Language(models.Model):
    iso_code = models.CharField(max_length=10, primary_key=True, verbose_name="ISO code")
    name = models.CharField(max_length=50)
    description = models.TextField()
    
    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.iso_code)


class Glossary(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "glossaries"


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
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "administrative statuses"


class PartOfSpeech(models.Model):
    name = models.CharField(max_length=50)
    tbx_representation = models.CharField(max_length=100, verbose_name="TBX representation")
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "parts of speech"


class Translation(models.Model):
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language)
    translation_text = models.CharField(max_length=100)
    process_status = models.BooleanField(blank=False, default=False)
    administrative_status = models.ForeignKey(AdministrativeStatus, null=True, blank=True)
    part_of_speech = models.ForeignKey(PartOfSpeech, null=True, blank=True)
    note = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.translation_text


class Definition(models.Model):
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language)
    definition_text = models.TextField()
    source = models.URLField(blank=True)
    
    def __unicode__(self):
        return self.definition_text[:200]#TODO buscar a maneira de truncar o texto devolto sen usar este método
    
    class Meta:
        unique_together = ("concept", "language")


