from glossaries.models import *
from django.contrib import admin

admin.site.register(Language)
admin.site.register(Glossary)
admin.site.register(Concept)

class TranslationAdmin(admin.ModelAdmin):
    fields = ['concept', 'language', 'translation_text', 'process_status']
    list_display = ('translation_text', 'language', 'concept')
    ordering = ('concept',)
    list_filter = ['language', 'concept']
    search_fields = ['translation_text']

admin.site.register(Translation, TranslationAdmin)


class DefinitionAdmin(admin.ModelAdmin):
    list_display = ('definition_text', 'concept', 'language')

admin.site.register(Definition, DefinitionAdmin)


