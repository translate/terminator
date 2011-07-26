# -*- coding: UTF-8 -*-
from django.contrib import admin
from terminator.models import *
from terminator.forms import TerminatorTranslationAdminForm, TerminatorConceptAdminForm


class PartOfSpeechForLanguageInline(admin.TabularInline):
    model = PartOfSpeechForLanguage
    extra = 1

class AdministrativeStatusReasonForLanguageInline(admin.TabularInline):
    model = AdministrativeStatusReason.languages.through
    extra = 1

class LanguageAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'iso_code', 'description')
    ordering = ('iso_code',)
    search_fields = ['name', 'iso_code']
    filter_horizontal = ('grammatical_genders', 'grammatical_numbers')
    inlines = (PartOfSpeechForLanguageInline, AdministrativeStatusReasonForLanguageInline)

admin.site.register(Language, LanguageAdmin)



class PartOfSpeechAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'tbx_representation', 'description')
    ordering = ('name',)
    inlines = (PartOfSpeechForLanguageInline,)

admin.site.register(PartOfSpeech, PartOfSpeechAdmin)



class AdministrativeStatusReasonAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = (AdministrativeStatusReasonForLanguageInline,)
    exclude = ('languages',)

admin.site.register(AdministrativeStatusReason, AdministrativeStatusReasonAdmin)



class GlossaryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'description')
    ordering = ('name',)
    search_fields = ['name']

admin.site.register(Glossary, GlossaryAdmin)



class DefinitionInline(admin.TabularInline):
    model = Definition
    extra = 1

class ConceptAdmin(admin.ModelAdmin):
    save_on_top = True
    form = TerminatorConceptAdminForm
    filter_horizontal = ('related_concepts',)
    list_display = ('id', 'glossary', 'subject_field', 'broader_concept')
    ordering = ('id',)
    list_filter = ['glossary']
    inlines = [DefinitionInline]

admin.site.register(Concept, ConceptAdmin)



class ContextSentenceInline(admin.TabularInline):
    model = ContextSentence
    extra = 1
    
class CorpusExampleInline(admin.TabularInline):
    model = CorpusExample
    extra = 1

class TranslationAdmin(admin.ModelAdmin):
    save_on_top = True
    form = TerminatorTranslationAdminForm
    fields = ['concept', 'language', 'translation_text', 'part_of_speech', 'grammatical_gender', 'grammatical_number', 'process_status', 'administrative_status', 'administrative_status_reason', 'note']
    list_display = ('translation_text', 'language', 'concept', 'part_of_speech', 'administrative_status')
    ordering = ('concept',)
    list_filter = ['language', 'concept', 'process_status', 'administrative_status', 'part_of_speech']
    search_fields = ['translation_text']
    inlines = [ContextSentenceInline, CorpusExampleInline]

admin.site.register(Translation, TranslationAdmin)



class DefinitionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('definition_text', 'concept', 'language', 'is_finalized')
    ordering = ('concept',)
    list_filter = ['language', 'concept', 'is_finalized']
    search_fields = ['definition_text']

admin.site.register(Definition, DefinitionAdmin)



class AdministrativeStatusAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'tbx_representation', 'allows_administrative_status_reason', 'description')
    ordering = ('name',)

admin.site.register(AdministrativeStatus, AdministrativeStatusAdmin)



class ProposalAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('word', 'language', 'definition', 'sent_date', 'for_glossary')
    ordering = ('sent_date',)
    list_filter = ['language', 'for_glossary', 'sent_date', 'user']
    search_fields = ['word', 'definition']
    actions = ['convert_proposals']
    
    def convert_proposals(self, request, queryset):
        for proposal in queryset:
            concept = Concept(glossary=proposal.for_glossary)
            concept.save()
            translation = Translation(concept=concept,language=proposal.language, translation_text=proposal.word)
            translation.save()
            definition = Definition(concept=concept, language=proposal.language, definition_text=proposal.definition)
            definition.save()
        rows_deleted = len(queryset)
        queryset.delete()
        if rows_deleted == 1:
            self.message_user(request, "1 proposal was successfully converted to translations and definitions in a new concept.")
        else:
            self.message_user(request, "%s proposals were successfully converted to translations and definitions in a new concept." % rows_deleted)
    convert_proposals.short_description = "Convert selected proposals to Translations and Definitions in a new concept"

admin.site.register(Proposal, ProposalAdmin)



class ExternalResourceAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('address', 'concept', 'language', 'link_type', 'description')
    ordering = ('concept',)
    list_filter = ['language', 'concept', 'link_type']
    search_fields = ['description', 'address']

admin.site.register(ExternalResource, ExternalResourceAdmin)



class GrammaticalGenderAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'tbx_representation', 'description')
    ordering = ('name',)

admin.site.register(GrammaticalGender, GrammaticalGenderAdmin)



class GrammaticalNumberAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'tbx_representation', 'description')
    ordering = ('name',)

admin.site.register(GrammaticalNumber, GrammaticalNumberAdmin)



class ExternalLinkTypeAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'tbx_representation', 'description')
    ordering = ('name',)

admin.site.register(ExternalLinkType, ExternalLinkTypeAdmin)



class ContextSentenceAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('text', 'translation')
    ordering = ('translation',)
    list_filter = ['translation']

admin.site.register(ContextSentence, ContextSentenceAdmin)



class CorpusExampleAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('translation', 'address', 'description')
    ordering = ('translation',)
    list_filter = ['translation']

admin.site.register(CorpusExample, CorpusExampleAdmin)



class CollaborationRequestAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('for_glossary', 'user', 'collaboration_role', 'sent_date')
    ordering = ('sent_date',)
    list_filter = ['collaboration_role', 'for_glossary', 'sent_date', 'user']
    actions = ['accept_collaboration_requests']

admin.site.register(CollaborationRequest, CollaborationRequestAdmin)



