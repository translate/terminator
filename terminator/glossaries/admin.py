from glossaries.models import *
from django.contrib import admin


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code', 'description')
    ordering = ('iso_code',)

admin.site.register(Language, LanguageAdmin)


admin.site.register(Glossary)


class ConceptAdmin(admin.ModelAdmin):
    filter_horizontal = ('related_concepts',)

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


