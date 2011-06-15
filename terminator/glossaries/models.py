from django.db import models

class Language(models.Model):
    iso_code = models.CharField(max_length=10, primary_key=True)
    description = models.TextField()

class Glossary(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

class Concept(models.Model):
    glossary = models.ForeignKey(Glossary)
    subject_field = models.ForeignKey('self', related_name='concepts_in_subject_field')
    broader_concept = models.ForeignKey('self', related_name='narrower_concepts')
    related_concepts = models.ManyToManyField('self')


class Translation(models.Model):
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language)
    translation_text = models.CharField(max_length=100)
    process_status = models.BooleanField(blank=False, default=False)
    #administrative_status = models.ForeignKey(Administrative_status)
    #part_of_speech = models.ForeignKey(Part_of_speech)

class Definition(models.Model):
    concept = models.ForeignKey(Concept)
    language = models.ForeignKey(Language)
    definition_text = models.TextField()
