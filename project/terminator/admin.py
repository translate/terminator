# -*- coding: UTF-8 -*-
from terminator.models import *
from django.contrib import admin


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code', 'description')
    ordering = ('iso_code',)
    search_fields = ['name', 'iso_code']

admin.site.register(Language, LanguageAdmin)



class PartOfSpeechForLanguageAdmin(admin.ModelAdmin):
    list_display = ('language', 'part_of_speech', 'allows_grammatical_gender', 'allows_grammatical_number')
    ordering = ('language', 'part_of_speech')
    list_filter = ['language', 'part_of_speech']

admin.site.register(PartOfSpeechForLanguage, PartOfSpeechForLanguageAdmin)



class GlossaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ('name',)
    search_fields = ['name']

admin.site.register(Glossary, GlossaryAdmin)



class DefinitionInline(admin.TabularInline):
    model = Definition
    extra = 1

class ConceptAdmin(admin.ModelAdmin):
    filter_horizontal = ('related_concepts',)
    inlines = [DefinitionInline]
    list_display = ('id', 'glossary', 'subject_field', 'broader_concept')
    ordering = ('id',)

admin.site.register(Concept, ConceptAdmin)



class ContextSentenceInline(admin.TabularInline):
    model = ContextSentence
    extra = 1
    
class CorpusExampleInline(admin.TabularInline):
    model = CorpusExample
    extra = 1

class TranslationAdmin(admin.ModelAdmin):
    fields = ['concept', 'language', 'translation_text', 'part_of_speech', 'grammatical_gender', 'grammatical_number', 'process_status', 'administrative_status', 'note']
    list_display = ('translation_text', 'language', 'concept', 'part_of_speech', 'administrative_status')
    ordering = ('concept',)
    list_filter = ['language', 'concept', 'process_status', 'administrative_status', 'part_of_speech']
    search_fields = ['translation_text']
    inlines = [ContextSentenceInline, CorpusExampleInline]

admin.site.register(Translation, TranslationAdmin)



class DefinitionAdmin(admin.ModelAdmin):
    list_display = ('definition_text', 'concept', 'language')
    ordering = ('concept',)
    list_filter = ['language', 'concept']
    search_fields = ['definition_text']

admin.site.register(Definition, DefinitionAdmin)



class PartOfSpeechAdmin(admin.ModelAdmin):
    list_display = ('name', 'tbx_representation', 'description')
    ordering = ('name',)

admin.site.register(PartOfSpeech, PartOfSpeechAdmin)



class AdministrativeStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'tbx_representation', 'description')
    ordering = ('name',)

admin.site.register(AdministrativeStatus, AdministrativeStatusAdmin)



class ProposalAdmin(admin.ModelAdmin):
    list_display = ('word', 'language', 'definition', 'sent_date')
    ordering = ('sent_date',)
    list_filter = ['language', 'sent_date', 'user']
    search_fields = ['word', 'definition']

admin.site.register(Proposal, ProposalAdmin)



class ExternalResourceAdmin(admin.ModelAdmin):
    list_display = ('address', 'concept', 'language', 'link_type', 'description')
    ordering = ('concept',)
    list_filter = ['language', 'concept', 'link_type']
    search_fields = ['description', 'address']

admin.site.register(ExternalResource, ExternalResourceAdmin)



class GrammaticalGenderAdmin(admin.ModelAdmin):
    list_display = ('name', 'tbx_representation', 'description')
    ordering = ('name',)

admin.site.register(GrammaticalGender, GrammaticalGenderAdmin)



class GrammaticalNumberAdmin(admin.ModelAdmin):
    list_display = ('name', 'tbx_representation', 'description')
    ordering = ('name',)

admin.site.register(GrammaticalNumber, GrammaticalNumberAdmin)



class ExternalLinkTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'tbx_representation', 'description')
    ordering = ('name',)

admin.site.register(ExternalLinkType, ExternalLinkTypeAdmin)



class ContextSentenceAdmin(admin.ModelAdmin):
    list_display = ('text', 'translation')
    ordering = ('translation',)
    list_filter = ['translation']

admin.site.register(ContextSentence, ContextSentenceAdmin)



class CorpusExampleAdmin(admin.ModelAdmin):
    list_display = ('translation', 'address', 'description')
    ordering = ('translation',)
    list_filter = ['translation']

admin.site.register(CorpusExample, CorpusExampleAdmin)



