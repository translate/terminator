# -*- coding: UTF-8 -*-
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user, assign
from guardian.utils import clean_orphan_obj_perms
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



class GlossaryAdmin(GuardedModelAdmin):
    save_on_top = True
    list_display = ('name', 'description')
    ordering = ('name',)
    search_fields = ['name']
    
    def queryset(self, request):
        qs = super(GlossaryAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return get_objects_for_user(request.user, ['is_owner_for_this_glossary'], qs, False)
    
    def save_model(self, request, obj, form, change):
        super(GlossaryAdmin, self).save_model(request, obj, form, change)
        assign('is_owner_for_this_glossary', request.user, obj)
        #assign('terminator.add_glossary', request.user)
        assign('terminator.change_glossary', request.user)
        assign('terminator.delete_glossary', request.user)
    
    def delete_model(self, request, obj):
        super(GlossaryAdmin, self).delete_model(request, obj)
        clean_orphan_obj_perms() # Remove all orphaned per object permissions after deleting the glossary instance

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
    
    def queryset(self, request):
        qs = super(ConceptAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        inner_qs = get_objects_for_user(request.user, ['is_lexicographer_in_this_glossary'], Glossary, False)
        return qs.filter(glossary__in=inner_qs)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ("subject_field", "broader_concept"):
            inner_qs = get_objects_for_user(request.user, ['is_terminologist_in_this_glossary'], Glossary, False)
            kwargs["queryset"] = Concept.objects.filter(glossary__in=inner_qs)
        if db_field.name == "glossary":
            kwargs["queryset"] = get_objects_for_user(request.user, ['is_terminologist_in_this_glossary'], Glossary, False)
        return super(ConceptAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "related_concepts":
            inner_qs = get_objects_for_user(request.user, ['is_terminologist_in_this_glossary'], Glossary, False)
            kwargs["queryset"] = Concept.objects.filter(glossary__in=inner_qs)
        return super(ConceptAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

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
    
    def queryset(self, request):
        qs = super(TranslationAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        inner_qs = get_objects_for_user(request.user, ['is_terminologist_in_this_glossary'], Glossary, False)
        return qs.filter(concept__glossary__in=inner_qs)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "concept":
            inner_qs = get_objects_for_user(request.user, ['is_terminologist_in_this_glossary'], Glossary, False)
            kwargs["queryset"] = Concept.objects.filter(glossary__in=inner_qs)
        return super(TranslationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Translation, TranslationAdmin)



class DefinitionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('definition_text', 'concept', 'language', 'is_finalized')
    ordering = ('concept',)
    list_filter = ['language', 'concept', 'is_finalized']
    search_fields = ['definition_text']
    
    def queryset(self, request):
        qs = super(DefinitionAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        inner_qs = get_objects_for_user(request.user, ['is_terminologist_in_this_glossary'], Glossary, False)
        return qs.filter(concept__glossary__in=inner_qs)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "concept":
            inner_qs = get_objects_for_user(request.user, ['is_terminologist_in_this_glossary'], Glossary, False)
            kwargs["queryset"] = Concept.objects.filter(glossary__in=inner_qs)
        return super(DefinitionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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
    
    def queryset(self, request):
        qs = super(ProposalAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        inner_qs = get_objects_for_user(request.user, ['is_lexicographer_in_this_glossary'], Glossary, False)
        return qs.filter(for_glossary__in=inner_qs)
    
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
    
    def queryset(self, request):
        qs = super(ExternalResourceAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        inner_qs = get_objects_for_user(request.user, ['is_terminologist_in_this_glossary'], Glossary, False)
        return qs.filter(concept__glossary__in=inner_qs)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "concept":
            inner_qs = get_objects_for_user(request.user, ['is_terminologist_in_this_glossary'], Glossary, False)
            kwargs["queryset"] = Concept.objects.filter(glossary__in=inner_qs)
        return super(ExternalResourceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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
    
    def queryset(self, request):
        qs = super(ContextSentenceAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        inner_qs = get_objects_for_user(request.user, ['is_terminologist_in_this_glossary'], Glossary, False)
        return qs.filter(translation__concept__glossary__in=inner_qs)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "translation":
            inner_qs = get_objects_for_user(request.user, ['is_terminologist_in_this_glossary'], Glossary, False)
            kwargs["queryset"] = Translation.objects.filter(concept__glossary__in=inner_qs)
        return super(ContextSentenceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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
    
    def queryset(self, request):
        qs = super(CollaborationRequestAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        inner_qs = get_objects_for_user(request.user, ['is_owner_for_this_glossary'], Glossary, False)
        return qs.filter(for_glossary__in=inner_qs)
    
    
    def accept_collaboration_requests(self, request, queryset):
        for collaboration_request in queryset:
            collaboration_request.user.is_staff = True # Because we need to ensure this users will can enter the admin site to work
            
            if collaboration_request.collaboration_role in ("T", "L", "O"):
                assign('is_terminologist_in_this_glossary', collaboration_request.user, collaboration_request.for_glossary)
                assign('terminator.add_concept', collaboration_request.user)
                
                assign('terminator.add_translation', collaboration_request.user)
                assign('terminator.change_translation', collaboration_request.user)
                assign('terminator.delete_translation', collaboration_request.user)
                
                assign('terminator.add_definition', collaboration_request.user)
                assign('terminator.change_definition', collaboration_request.user)
                assign('terminator.delete_definition', collaboration_request.user)
                
                assign('terminator.add_externalresource', collaboration_request.user)
                assign('terminator.change_externalresource', collaboration_request.user)
                assign('terminator.delete_externalresource', collaboration_request.user)
                
                assign('terminator.add_contextsentence', collaboration_request.user)
                assign('terminator.change_contextsentence', collaboration_request.user)
                assign('terminator.delete_contextsentence', collaboration_request.user)
                
                assign('terminator.add_corpusexample', collaboration_request.user)
                assign('terminator.change_corpusexample', collaboration_request.user)
                assign('terminator.delete_corpusexample', collaboration_request.user)
            
            if collaboration_request.collaboration_role  in ("L", "O"):
                assign('is_lexicographer_in_this_glossary', collaboration_request.user, collaboration_request.for_glossary)
                assign('terminator.change_concept', collaboration_request.user)
                assign('terminator.delete_concept', collaboration_request.user)
            
            if collaboration_request.collaboration_role == "O":
                assign('is_owner_for_this_glossary', collaboration_request.user, collaboration_request.for_glossary)
                #assign('terminator.add_glossary', collaboration_request.user)
                assign('terminator.change_glossary', collaboration_request.user)
                assign('terminator.delete_glossary', collaboration_request.user)
        rows_deleted = len(queryset)
        queryset.delete()
        if rows_deleted == 1:
            self.message_user(request, "1 collaboration request was successfully accepted.")
        else:
            self.message_user(request, "%s collaboration requests were successfully accepted." % rows_deleted)
    accept_collaboration_requests.short_description = "Accept selected collaboration requests"

admin.site.register(CollaborationRequest, CollaborationRequestAdmin)



