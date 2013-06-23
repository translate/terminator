# -*- coding: UTF-8 -*-
#
# Copyright 2011, 2013 Leandro Regueiro
#
# This file is part of Terminator.
#
# Terminator is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Terminator is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Terminator. If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy, ungettext, ugettext as _

from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user
from guardian.utils import clean_orphan_obj_perms

from terminator.forms import (TerminatorConceptAdminForm,
                              TerminatorGlossaryAdminForm,
                              TerminatorTranslationAdminForm)
from terminator.models import *


class PartOfSpeechForLanguageInline(admin.TabularInline):
    model = PartOfSpeechForLanguage
    extra = 1


class AdministrativeStatusReasonForLanguageInline(admin.TabularInline):
    model = AdministrativeStatusReason.languages.through
    extra = 1
    verbose_name = _("Administrative status reason for language")
    verbose_name_plural = _("Administrative status reasons for language")


class LanguageAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'iso_code', 'description')
    ordering = ('iso_code',)
    search_fields = ['name', 'iso_code']
    filter_horizontal = ('grammatical_genders', 'grammatical_numbers')
    inlines = (PartOfSpeechForLanguageInline,
               AdministrativeStatusReasonForLanguageInline)


admin.site.register(Language, LanguageAdmin)


class PartOfSpeechAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'tbx_representation', 'description')
    ordering = ('name',)
    inlines = (PartOfSpeechForLanguageInline,)


admin.site.register(PartOfSpeech, PartOfSpeechAdmin)


class AdministrativeStatusReasonAdmin(admin.ModelAdmin):
    save_on_top = True
    filter_horizontal = ('languages',)


admin.site.register(AdministrativeStatusReason,
                    AdministrativeStatusReasonAdmin)


class GlossaryAdmin(GuardedModelAdmin):
    save_on_top = True
    form = TerminatorGlossaryAdminForm
    filter_horizontal = ('subscribers','subject_fields',)
    list_display = ('name', 'description')
    ordering = ('name',)
    search_fields = ['name']

    def queryset(self, request):
        qs = super(GlossaryAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return get_objects_for_user(request.user,
                                    ['is_owner_for_this_glossary'], qs, False)

    def save_model(self, request, obj, form, change):
        super(GlossaryAdmin, self).save_model(request, obj, form, change)

        if not change:
            obj.assign_terminologist_permissions(request.user)
            obj.assign_lexicographer_permissions(request.user)
            obj.assign_owner_permissions(request.user)

    def delete_model(self, request, obj):
        super(GlossaryAdmin, self).delete_model(request, obj)
        # Remove all orphaned per object permissions after deleting the
        # glossary instance.
        clean_orphan_obj_perms()


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
        inner_qs = get_objects_for_user(request.user,
                                        ['is_lexicographer_in_this_glossary'],
                                        Glossary, False)
        return qs.filter(glossary__in=inner_qs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ("subject_field", "broader_concept"):
            inner_qs = get_objects_for_user(request.user, ['is_lexicographer_in_this_glossary'], Glossary, False)
            kwargs["queryset"] = Concept.objects.filter(glossary__in=inner_qs)
        if db_field.name == "glossary":
            kwargs["queryset"] = get_objects_for_user(request.user, ['is_lexicographer_in_this_glossary'], Glossary, False)
        return super(ConceptAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "related_concepts":
            inner_qs = get_objects_for_user(request.user, ['is_lexicographer_in_this_glossary'], Glossary, False)
            kwargs["queryset"] = Concept.objects.filter(glossary__in=inner_qs)
        return super(ConceptAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Concept, ConceptAdmin)


class SummaryMessageAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('text', 'concept', 'language', 'is_finalized')
    ordering = ('concept',)
    list_filter = ['language', 'concept', 'is_finalized']
    search_fields = ['text']

    def queryset(self, request):
        qs = super(SummaryMessageAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        inner_qs = get_objects_for_user(request.user,
                                        ['is_lexicographer_in_this_glossary'],
                                        Glossary, False)
        return qs.filter(concept__glossary__in=inner_qs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "concept":
            inner_qs = get_objects_for_user(request.user, ['is_lexicographer_in_this_glossary'], Glossary, False)
            kwargs["queryset"] = Concept.objects.filter(glossary__in=inner_qs)
        return super(SummaryMessageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(SummaryMessage, SummaryMessageAdmin)


class ContextSentenceInline(admin.TabularInline):
    model = ContextSentence
    extra = 1


class CorpusExampleInline(admin.TabularInline):
    model = CorpusExample
    extra = 1


class TranslationAdmin(admin.ModelAdmin):
    save_on_top = True
    form = TerminatorTranslationAdminForm
    fields = [
        'concept', 'language', 'translation_text', 'part_of_speech',
        'grammatical_gender', 'grammatical_number', 'process_status',
        'administrative_status', 'administrative_status_reason', 'note'
    ]
    list_display = ('translation_text', 'language', 'concept', 'part_of_speech', 'administrative_status', 'process_status',)
    ordering = ('concept',)
    list_filter = [
        'language', 'concept', 'process_status', 'administrative_status',
        'part_of_speech'
    ]
    search_fields = ['translation_text']
    inlines = [ContextSentenceInline, CorpusExampleInline]

    def queryset(self, request):
        qs = super(TranslationAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        inner_qs = get_objects_for_user(request.user,
                                        ['is_terminologist_in_this_glossary'],
                                        Glossary, False)
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
        inner_qs = get_objects_for_user(request.user,
                                        ['is_terminologist_in_this_glossary'],
                                        Glossary, False)
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
        inner_qs = get_objects_for_user(request.user,
                                        ['is_lexicographer_in_this_glossary'],
                                        Glossary, False)
        return qs.filter(for_glossary__in=inner_qs)

    def convert_proposals(self, request, queryset):
        for proposal in queryset:
            concept = Concept(glossary=proposal.for_glossary)
            concept.save()
            translation = Translation(concept=concept,
                                      language=proposal.language,
                                      translation_text=proposal.word)
            translation.save()
            definition = Definition(concept=concept,
                                    language=proposal.language,
                                    definition_text=proposal.definition)
            definition.save()
            obj_display = force_unicode(proposal)
            self.log_deletion(request, proposal, obj_display)
            #TODO maybe notify by email the users that sent the proposals
        rows_deleted = len(queryset)
        queryset.delete()
        self.message_user(request, ungettext('%(count)d proposal was '
                                             'successfully converted to '
                                             'translations and definitions in '
                                             'a new concept.',
                                             '%(count)d proposals were '
                                             'successfully converted to '
                                             'translations and definitions in '
                                             'a new concept.', rows_deleted) %
                                             {'count': rows_deleted})
    convert_proposals.short_description = _("Convert selected proposals to "
                                            "Translations and Definitions in "
                                            "a new concept")

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
        inner_qs = get_objects_for_user(request.user,
                                        ['is_terminologist_in_this_glossary'],
                                        Glossary, False)
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
        inner_qs = get_objects_for_user(request.user,
                                        ['is_terminologist_in_this_glossary'],
                                        Glossary, False)
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

    def queryset(self, request):
        qs = super(CorpusExampleAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        inner_qs = get_objects_for_user(request.user,
                                        ['is_terminologist_in_this_glossary'],
                                        Glossary, False)
        return qs.filter(translation__concept__glossary__in=inner_qs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "translation":
            inner_qs = get_objects_for_user(request.user, ['is_terminologist_in_this_glossary'], Glossary, False)
            kwargs["queryset"] = Translation.objects.filter(concept__glossary__in=inner_qs)
        return super(CorpusExampleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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
        inner_qs = get_objects_for_user(request.user,
                                        ['is_owner_for_this_glossary'],
                                        Glossary, False)
        return qs.filter(for_glossary__in=inner_qs)

    #TODO replace the delete admin action with a wrapper around the default one
    # in order to send an email to all the collaboration request users telling
    # them that their requests were not approved.

    def delete_model(self, request, obj):
        # Send email messages only if allowed in the settings
        if settings.SEND_NOTIFICATION_EMAILS:
            mail_subject = _('[Terminator] collaboration request rejected')
            mail_body_data = {
                'role': obj.get_collaboration_role_display(),
                'glossary': obj.for_glossary
            }
            full_mail_text = (_('Your collaboration request as \"%(role)s\" '
                               'for glossary \"%(glossary)s\" was rejected by '
                               'the glossary owners.') % mail_body_data)
            send_mail(mail_subject, full_mail_text,
                      'donotreply@donotreply.com', [obj.user.email],
                      fail_silently=False)
        super(CollaborationRequestAdmin, self).delete_model(request, obj)

    def accept_collaboration_requests(self, request, queryset):
        for collaboration_request in queryset:
            collaboration_request.user.is_staff = True # Because we need to ensure this users will can enter the admin site to work
            mail_message = ""

            if collaboration_request.collaboration_role in ("T", "L", "O"):
                mail_message += _("Now you can manage translations, "
                                  "definitions, external resources, context "
                                  "sentences and corpus examples inside this "
                                  "glossary.")
                collaboration_request.for_glossary.assign_terminologist_permissions(collaboration_request.user)

            if collaboration_request.collaboration_role  in ("L", "O"):
                mail_message += _("\n\nAlso you can manage concepts and "
                                  "concept proposals for this glossary.")
                collaboration_request.for_glossary.assign_lexicographer_permissions(collaboration_request.user)

            if collaboration_request.collaboration_role == "O":
                mail_message += _("\n\nAs glossary owner you can modify or "
                                  "delete the glossary and manage its "
                                  "collaboration requests as well.")
                collaboration_request.for_glossary.assign_owner_permissions(collaboration_request.user)

            # Send email messages only if allowed in the settings
            if settings.SEND_NOTIFICATION_EMAILS:
                mail_subject = _("[Terminator] collaboration request accepted")
                mail_body_data = {
                    'role': collaboration_request.get_collaboration_role_display(),
                    'glossary': collaboration_request.for_glossary
                }
                mail_text = (_("Your collaboration request as \"%(role)s\" "
                               "for glossary \"%(glossary)s\" was accepted.") %
                             mail_body_data)
                full_mail_text = mail_text + mail_message
                send_mail(mail_subject, full_mail_text,
                          'donotreply@donotreply.com',
                          [collaboration_request.user.email],
                          fail_silently=False)
            obj_display = force_unicode(collaboration_request)
            self.log_deletion(request, collaboration_request, obj_display)
        rows_deleted = len(queryset)
        queryset.delete()
        # Translators: This message appears after executing the action in admin
        self.message_user(request, ungettext("%(count)d collaboration request "
                                             "was successfully accepted.",
                                             "%(count)d collaboration "
                                             "requests were successfully "
                                             "accepted.", rows_deleted) %
                                             {'count': rows_deleted})
    accept_collaboration_requests.short_description = _("Accept selected %(verbose_name_plural)s")

admin.site.register(CollaborationRequest, CollaborationRequestAdmin)



