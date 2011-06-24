# -*- coding: UTF-8 -*-
from terminator.models import *
from django.contrib import admin


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code', 'description')
    ordering = ('iso_code',)
    search_fields = ['name', 'iso_code']

admin.site.register(Language, LanguageAdmin)



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

admin.site.register(Concept, ConceptAdmin)


class TranslationAdmin(admin.ModelAdmin):
    fields = ['concept', 'language', 'translation_text', 'part_of_speech', 'process_status', 'administrative_status', 'note']
    list_display = ('translation_text', 'language', 'concept', 'part_of_speech', 'administrative_status')
    ordering = ('concept',)
    list_filter = ['language', 'concept', 'process_status']
    search_fields = ['translation_text']

admin.site.register(Translation, TranslationAdmin)


class DefinitionAdmin(admin.ModelAdmin):
    list_display = ('definition_text', 'concept', 'language')

admin.site.register(Definition, DefinitionAdmin)


class PartOfSpeechAdmin(admin.ModelAdmin):
    list_display = ('name', 'tbx_representation', 'description')

admin.site.register(PartOfSpeech, PartOfSpeechAdmin)


class AdministrativeStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'tbx_representation', 'description')

admin.site.register(AdministrativeStatus, AdministrativeStatusAdmin)


class ProposalAdmin(admin.ModelAdmin):
    list_display = ('language', 'word', 'definition')

admin.site.register(Proposal, ProposalAdmin)


class ExternalResourceAdmin(admin.ModelAdmin):
    list_display = ('address', 'concept', 'language', 'link_type', 'description')

admin.site.register(ExternalResource, ExternalResourceAdmin)


class GrammaticalGenderAdmin(admin.ModelAdmin):
    list_display = ('name', 'tbx_representation', 'description')

admin.site.register(GrammaticalGender, GrammaticalGenderAdmin)


class GrammaticalNumberAdmin(admin.ModelAdmin):
    list_display = ('name', 'tbx_representation', 'description')

admin.site.register(GrammaticalNumber, GrammaticalNumberAdmin)


