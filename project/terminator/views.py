# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404, Http404
from django.views.generic import DetailView, ListView
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.contrib.comments.models import Comment
from django.contrib.admin.models import LogEntry, ADDITION
from django.utils.encoding import force_unicode
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from profiles.views import *
from guardian.shortcuts import get_perms
from xml.dom import minidom
from terminator.models import *
from terminator.forms import *



def terminator_profile_create(request):
    extra = {'search_form': SearchForm(), 'next': request.get_full_path()}
    return create_profile(request, extra_context=extra)



def terminator_profile_edit(request):
    extra = {'search_form': SearchForm(), 'next': request.get_full_path()}
    return edit_profile(request, extra_context=extra)



def terminator_profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    user_comments = Comment.objects.filter(user=user).order_by('-submit_date')
    paginator = Paginator(user_comments, 25)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        comments = paginator.page(page)
    except (EmptyPage, InvalidPage):
        comments = paginator.page(paginator.num_pages)
    glossary_list = Glossary.objects.all()
    user_glossaries = []
    for glossary in glossary_list:
        perms = get_perms(user, glossary)
        if u'is_owner_for_this_glossary' in perms:
            user_glossaries.append({'glossary': glossary, 'role': _(u"Owner")})
        elif u'is_lexicographer_in_this_glossary' in perms:
            user_glossaries.append({'glossary': glossary, 'role': _(u"Lexicographer")})
        elif u'is_terminologist_in_this_glossary' in perms:
            user_glossaries.append({'glossary': glossary, 'role': _(u"Terminologist")})
    extra = {'glossaries': user_glossaries, 'comments': comments, 'search_form': SearchForm(), 'next': request.get_full_path()}
    return profile_detail(request, username, extra_context=extra)



def terminator_profile_list(request):
    extra = {'search_form': SearchForm(), 'next': request.get_full_path()}
    return profile_list(request, template_object_name="profile", extra_context=extra)



class TerminatorDetailView(DetailView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TerminatorDetailView, self).get_context_data(**kwargs)
        # Add the breadcrumbs search form to context
        context['search_form'] = SearchForm()
        # Add the request path to correctly render the "log in" link in template
        context['next'] = self.request.get_full_path()
        return context



class TerminatorListView(ListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TerminatorListView, self).get_context_data(**kwargs)
        # Add the breadcrumbs search form to context
        context['search_form'] = SearchForm()
        # Add the request path to correctly render the "log in" link in template
        context['next'] = self.request.get_full_path()
        return context



class ConceptDetailView(TerminatorDetailView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ConceptDetailView, self).get_context_data(**kwargs)
        # Add the comment thread for the given language, if given, to context
        context['available_languages'] = Language.objects.order_by("pk")
        try:
            language = Language.objects.get(pk=self.kwargs.get('lang', None))
        except Language.DoesNotExist:
            pass
        else:
            context['current_language'] = language
            context['comments_thread'], created = ConceptLanguageCommentsThread.objects.get_or_create(concept=context['concept'], language=language)
        return context



class GlossaryDetailView(TerminatorDetailView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    @transaction.commit_manually
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GlossaryDetailView, self).get_context_data(**kwargs)
        # Add the collaboration request form to context and treat it if form data is received
        if self.request.method == 'POST':
            if 'collaboration_role' in self.request.POST:
                collaboration_form = CollaborationRequestForm(self.request.POST)
                if collaboration_form.is_valid():
                    collaboration_request = collaboration_form.save(commit=False)
                    collaboration_request.user = self.request.user
                    collaboration_request.for_glossary = self.object
                    try:
                        collaboration_request.save()
                    except IntegrityError:
                        transaction.rollback()
                        error_message = _("You already sent a similar request for this glossary!")
                        context['collaboration_request_error_message'] = error_message
                        #TODO consider updating the request DateTimeField to now and then save
                    else:
                        transaction.commit()
                        message = _("You will receive a message when the glossary owners have considerated your request.")
                        context['collaboration_request_message'] = message
                        collaboration_form = CollaborationRequestForm()
                # Always provide a blank subscription form after managing a collaboration request form
                subscribe_form = SubscribeForm()
            elif 'subscribe_to_this_glossary' in self.request.POST:
                subscribe_form = SubscribeForm(self.request.POST)
                if subscribe_form.is_valid():
                    self.object.subscribers.add(self.request.user)
                    transaction.commit()
                    context['subscribe_message'] = _("You have subscribed to get email notifications when a comment is saved or modified.")
                    subscribe_form = SubscribeForm()
                # Always provide a blank collaboration request form after managing a subscription form
                collaboration_form = CollaborationRequestForm()
        else:
            collaboration_form = CollaborationRequestForm()
            subscribe_form = SubscribeForm()
        context['subscribe_form'] = subscribe_form
        context['collaboration_request_form'] = collaboration_form
        # Get the collaborators list and their roles
        user_list = User.objects.all()
        collaborators = []
        for user in user_list:
            perms = get_perms(user, self.object)
            if u'is_owner_for_this_glossary' in perms:
                collaborators.append({'user': user, 'role': _(u"Owner")})
            elif u'is_lexicographer_in_this_glossary' in perms:
                collaborators.append({'user': user, 'role': _(u"Lexicographer")})
            elif u'is_terminologist_in_this_glossary' in perms:
                collaborators.append({'user': user, 'role': _(u"Terminologist")})
        transaction.commit()
        context['collaborators'] = collaborators
        return context



@csrf_protect
def terminator_index(request):
    new_proposal_message = ""
    if request.method == 'POST':
        proposal_form = ProposalForm(request.POST)
        if proposal_form.is_valid():
            new_proposal = proposal_form.save(commit=False)
            new_proposal.user = request.user
            new_proposal.save()
            # Log the addition using LogEntry from admin contrib app
            LogEntry.objects.log_action(
                user_id         = request.user.pk,
                content_type_id = ContentType.objects.get_for_model(new_proposal).pk,
                object_id       = new_proposal.pk,
                object_repr     = force_unicode(new_proposal),
                action_flag     = ADDITION
            )
            new_proposal_message = _("Thank you for sending a new proposal. You may send more!")
            proposal_form = ProposalForm()
    else:
        proposal_form = ProposalForm()
    search_form = SearchForm()
    context = {'search_form': search_form, 'proposal_form': proposal_form, 'new_proposal_message': new_proposal_message}
    context['next'] = request.get_full_path()
    context['glossary_list'] = get_list_or_404(Glossary)
    context['latest_proposals'] = Proposal.objects.order_by("-id")[:8]
    context['latest_comments'] = Comment.objects.order_by("-id")[:8]
    glossary_ctype = ContentType.objects.get_for_model(Glossary)
    context['latest_glossary_changes'] = LogEntry.objects.filter(content_type=glossary_ctype).order_by("-action_time")[:8]
    concept_ctype = ContentType.objects.get_for_model(Concept)
    context['latest_concept_changes'] = LogEntry.objects.filter(content_type=concept_ctype).order_by("-action_time")[:8]
    translation_ctype = ContentType.objects.get_for_model(Translation)
    latest_translation_changes = LogEntry.objects.filter(content_type=translation_ctype).order_by("-action_time")[:8]
    translation_changes = []
    for logentry in latest_translation_changes:
        translation_concept_id = logentry.object_repr.split("for Concept #")[1]
        translation_changes.append({"data": logentry, "translation_concept_id": translation_concept_id})
    context['latest_translation_changes'] = translation_changes
    return render_to_response('index.html', context, context_instance=RequestContext(request))



def export_glossaries_to_TBX(glossaries, desired_languages=[], export_all_definitions=False, export_admitted=False, export_not_recommended=False, export_all_translations=False):
    # Get the data
    if not glossaries:
        raise Http404
    elif len(glossaries) == 1:
        glossary_data = glossaries[0]
    else:
        glossary_description = _("TBX file created by exporting the following glossaries: ")
        glossaries_names_list = []
        for gloss in glossaries:
            glossaries_names_list.append(gloss.name)
        glossary_description += ", ".join(glossaries_names_list)
        glossary_data = {"name": _("Terminator TBX exported glossary"), "description": glossary_description}
    data = {'glossary': glossary_data, 'concepts': []}
    
    preferred = AdministrativeStatus.objects.get(name="Preferred")
    admitted = AdministrativeStatus.objects.get(name="Admitted")
    not_recommended = AdministrativeStatus.objects.get(name="Not recommended")
    
    concept_list = Concept.objects.filter(glossary__in=glossaries).order_by("glossary", "id")
    for concept in concept_list:
        concept_data = {'concept': concept, 'languages': []}
        
        if desired_languages:
            concept_translations = concept.translation_set.filter(language__in=desired_languages)
            concept_external_resources = concept.externalresource_set.filter(language__in=desired_languages).order_by("language")
            concept_definitions = concept.definition_set.filter(language__in=desired_languages)
        else:
            concept_translations = concept.translation_set.all()
            concept_external_resources = concept.externalresource_set.order_by("language")
            concept_definitions = concept.definition_set.all()
        
        if not export_all_translations:
            if export_not_recommended:
                concept_translations = concept_translations.filter(Q(administrative_status=preferred) | Q(administrative_status=admitted) | Q(administrative_status=not_recommended))
            elif export_admitted:
                concept_translations = concept_translations.filter(Q(administrative_status=preferred) | Q(administrative_status=admitted))
            else:
                concept_translations = concept_translations.filter(administrative_status=preferred)
        concept_translations = concept_translations.order_by("language")
        
        if not export_all_definitions:
            concept_definitions = concept_definitions.filter(is_finalized=True)
        concept_definitions = concept_definitions.order_by("language")
        
        # Get the list of used languages in the filtered translations, external resources and definitions
        language_set = set()
        for translation in concept_translations:
            language_set.add(translation.language_id)
        for definition in concept_definitions:
            language_set.add(definition.language_id)
        for external_resource in concept_external_resources:
            language_set.add(external_resource.language_id)
        used_languages_list = list(language_set)
        used_languages_list.sort()
        
        trans_index = 0
        res_index = 0
        def_index = 0
        for language_code in used_languages_list:
            language = Language.objects.get(pk=language_code)
            
            lang_translations = []
            while trans_index < len(concept_translations) and concept_translations[trans_index].language == language:
                lang_translations.append(concept_translations[trans_index])
                trans_index += 1
            
            lang_definition = None
            if def_index < len(concept_definitions) and concept_definitions[def_index].language == language:
                lang_definition = concept_definitions[def_index]
                def_index += 1
            
            lang_resources = []
            while res_index < len(concept_external_resources) and concept_external_resources[res_index].language == language:
                lang_resources.append(concept_external_resources[res_index])
                res_index += 1
            
            lang_data = {'iso_code': language_code, 'translations': lang_translations, 'externalresources': lang_resources, 'definition': lang_definition}
            concept_data['languages'].append(lang_data)
        
        # Only append concept data if at least has information for a language
        if concept_data['languages']:
            data['concepts'].append(concept_data)
    
    # Create the HttpResponse object with the appropriate header.
    response = HttpResponse(mimetype='application/x-tbx')
    if len(glossaries) == 1:
        response['Content-Disposition'] = 'attachment; filename=' + glossaries[0].name + '.tbx'
    else:
        response['Content-Disposition'] = 'attachment; filename=terminator_several_exported_glossaries.tbx'
    
    # Create the response
    t = loader.get_template('export.tbx')
    c = Context({'data': data})
    response.write(t.render(c))
    return response



def autoterm(request, language_code):#TODO facer que sexa capaz de exportar para calquera parella de idioma, e non só para inglés e outro idioma
    language = get_object_or_404(Language, pk=language_code)
    english = get_object_or_404(Language, pk="en")
    glossaries = list(Glossary.objects.all())
    if not glossaries:
        raise Http404
    return export_glossaries_to_TBX(glossaries, [language, english])



@csrf_protect
def export(request):
    #exporting_message = ""#TODO show export confirmation message
    if request.method == 'GET' and 'from_glossaries' in request.GET:
        export_form = ExportForm(request.GET)
    elif request.method == 'POST' and 'from_glossaries' in request.POST:
        export_form = ExportForm(request.POST)
        if export_form.is_valid():
            glossaries = export_form.cleaned_data['from_glossaries']
            desired_languages = export_form.cleaned_data['for_languages']
            export_all_definitions = export_form.cleaned_data['export_not_finalized_definitions']
            export_not_recommended = export_form.cleaned_data['export_not_recommended_translations']
            export_admitted = export_form.cleaned_data['export_admitted_translations']
            export_all_translations = export_form.cleaned_data['export_not_finalized_translations']
            #exporting_message = "Exported succesfully."#TODO show export confirmation message
            return export_glossaries_to_TBX(glossaries, desired_languages, export_all_definitions, export_admitted, export_not_recommended, export_all_translations)
    else:
        export_form = ExportForm()
    search_form = SearchForm()
    context = {'search_form': search_form, 'export_form': export_form}
    context['next'] = request.get_full_path()
    #context['exporting_message'] = exporting_message#TODO show export confirmation message
    return render_to_response('export.html', context, context_instance=RequestContext(request))



@transaction.commit_manually
def import_uploaded_file(uploaded_file, imported_glossary):
    #FIXME this function is too slow with a file with just 100 termEntry, so disable autocommit and use @transaction.commit_manually in order to commit just after the creation of concepts, translations and at the function end
    #FIXME split this function in several shortest functions
    #FIXME validate the uploaded file in order to check that it is a valid TBX file, or even a text file.
    tbx_file = minidom.parse(uploaded_file)
    
    def getText(nodelist):
        rc = u""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc += node.data
        return rc.strip()
    
    #FIXME add the title and description from the TBX file to the glossary object description and then save it
    #glossary_name = getText(tbx_file.getElementsByTagName(u"title")[0].childNodes)
    #glossary_description = getText(tbx_file.getElementsByTagName(u"p")[0].childNodes)
    
    # Get now the link types list in order to avoid retrieving it tenths of times inside the loop
    external_link_types = dict((linktype.pk, linktype) for linktype in ExternalLinkType.objects.all())
    available_link_types = external_link_types.keys()
    
    concept_pool = {}
    try:
        for concept_tag in tbx_file.getElementsByTagName(u"termEntry"):
            concept_id = concept_tag.getAttribute(u"id")
            if not concept_id:
                raise Exception
            concept_object = Concept(glossary=imported_glossary)
            concept_object.save()
            concept_pool_entry = {"object": concept_object}
            
            # Get the subject field and broader concept for the current termEntry
            for descrip_tag in concept_tag.getElementsByTagName(u"descrip"):# Be careful because it returns all the descrip tags, even from langSet or lower levels
                if descrip_tag.getAttribute("type") == "subjectField":
                    # Only accept subjectFields that are inside a descripGrp with a ref tag pointing to a concept
                    if descrip_tag.parentNode != concept_tag:
                        ref_tags = descrip_tag.parentNode.getElementsByTagName(u"ref")
                        if ref_tags:
                            concept_pool_entry["subject"] = ref_tags[0].getAttribute(u"target")
                if descrip_tag.getAttribute(u"type") == u"broaderConceptGeneric":
                    broader = descrip_tag.getAttribute(u"target")
                    if broader:
                        concept_pool_entry["broader"] = broader
            
            # Get the related concepts info for the current termEntry
            concept_pool_entry["related"] = []
            for ref_tag in concept_tag.getElementsByTagName(u"ref"):
                if ref_tag.getAttribute(u"type") == u"crossReference":
                    # The subject_field may be inside a descripGrp with a ref tag
                    if ref_tag.parentNode == concept_tag:
                        related_key = ref_tag.getAttribute(u"target")
                        if related_key:
                            concept_pool_entry["related"].append(related_key)
            # If the termEntry has no related concepts remove the key related from concept_pool_entry
            if not concept_pool_entry["related"]:
                concept_pool_entry.pop("related")
            
            # Save all the concept relations for setting them when the TBX file is fully readed
            concept_pool[concept_id] = concept_pool_entry
            
            for language_tag in concept_tag.getElementsByTagName(u"langSet"):
                xml_lang = language_tag.getAttribute(u"xml:lang")
                if not xml_lang:
                    raise Exception
                # The next line may raise Language.DoesNotExist
                language_object = Language.objects.get(pk=xml_lang)
                
                # Get the definition for each language
                for descrip_tag in language_tag.getElementsByTagName(u"descrip"):# Be careful because it returns all the descrip tags, and not all are definitions
                    descrip_type = descrip_tag.getAttribute(u"type")
                    if descrip_type == u"definition":
                        definition_text = getText(descrip_tag.childNodes)
                        if definition_text:
                            definition_object = Definition(concept=concept_object, language=language_object, definition_text=definition_text, is_finalized=True)
                            # If the definition is inside a descripGrp tag, it may have a source
                            if descrip_tag.parentNode != language_tag:
                                definition_source_list = descrip_tag.parentNode.getElementsByTagName(u"xref")
                                if definition_source_list:
                                    definition_object.source = definition_source_list[0].getAttribute(u"target")
                            definition_object.save()
                        # Each langSet should have at most one definition, so stop looping
                        break
                 
                # Get the external resources for each language
                for xref_tag in language_tag.getElementsByTagName(u"xref"):# Be careful since it returns all the xref tags and not all refer to ExternalResources
                    resource_type = xref_tag.getAttribute(u"type")
                    if resource_type in available_link_types:
                        resource_target = xref_tag.getAttribute(u"target")
                        resource_description = getText(xref_tag.childNodes)
                        if resource_target and resource_description:
                            # The next line NEVER should raise ExternalLinkType.DoesNotExist
                            resource_link_type = external_link_types[resource_type]
                            external_resource_object = ExternalResource(concept=concept_object, language=language_object, address=resource_target, link_type=resource_link_type, description=resource_description)
                            external_resource_object.save()
                
                # Get the translations and related data for each language
                for translation_tag in language_tag.getElementsByTagName(u"tig"):#FIXME this should work for ntig tags too
                    term_tags = translation_tag.getElementsByTagName(u"term")
                    if term_tags:# Only proceed if exists a term tag
                        translation_text = getText(term_tags[0].childNodes)# Only work with the first term tag
                        translation_object = Translation(concept=concept_object, language=language_object, translation_text=translation_text)
                        #translation_object.save()#FIXME This saving seems to be unnecessary since it is saved later again
                        
                        for termnote_tag in translation_tag.getElementsByTagName(u"termNote"):
                            termnote_type = termnote_tag.getAttribute(u"type")
                            #FIXME: the parts of speech, grammatical genders, grammatical numbers, administrative statuses and administrative status reasons specified in the TBX file may not exist in the Terminator database, so the import process will fail. Maybe it should create those missing entities, but it may fill the database with duplicates.
                            #FIXME: the parts of speech, grammatical genders, grammatical numbers, administrative statuses and administrative status reasons can only be used for certain languages, and the actual importing code doesn't respect these constraints.
                            if termnote_type == u"partOfSpeech":
                                # The next line may raise PartOfSpeech.DoesNotExist
                                part_of_speech_object = PartOfSpeech.objects.get(tbx_representation__iexact=getText(termnote_tag.childNodes))
                                translation_object.part_of_speech = part_of_speech_object
                            elif termnote_type == u"grammaticalGender":
                                # The next line may raise GrammaticalGender.DoesNotExist
                                grammatical_gender_object = GrammaticalGender.objects.get(tbx_representation__iexact=getText(termnote_tag.childNodes))
                                translation_object.grammatical_gender = grammatical_gender_object
                            elif termnote_type == u"grammaticalNumber":
                                # The next line may raise GrammaticalNumber.DoesNotExist
                                grammatical_number_object = GrammaticalNumber.objects.get(tbx_representation__iexact=getText(termnote_tag.childNodes))
                                translation_object.grammatical_number = grammatical_number_object
                            if termnote_type == u"processStatus":
                                if getText(termnote_tag.childNodes) == u"finalized":
                                    translation_object.process_status = True
                            if termnote_type == u"administrativeStatus":
                                # The next line may raise AdministrativeStatus.DoesNotExist
                                administrative_status_object = AdministrativeStatus.objects.get(tbx_representation__iexact=getText(termnote_tag.childNodes))
                                translation_object.administrative_status = administrative_status_object
                                # If the administrative status is inside a termGrp tag it may have an administrative status reason
                                if administrative_status_object.allows_administrative_status_reason and termnote_tag.parentNode != translation_tag:
                                    reason_tag_list = termnote_tag.parentNode.getElementsByTagName(u"note")
                                    if reason_tag_list:
                                        try:
                                            # The next line may raise AdministrativeStatusReason.DoesNotExist
                                            reason_object = AdministrativeStatusReason.objects.get(name__iexact=getText(reason_tag_list[0].childNodes))
                                        except Exception:
                                            pass
                                        else:
                                            translation_object.administrative_status_reason = reason_object
                        
                        for note_tag in translation_tag.getElementsByTagName(u"note"):
                            # Ensure that this note tag is not at lower levels inside the translation tag
                            if note_tag.parentNode == translation_tag:
                                note_text = getText(note_tag.childNodes)
                                if note_text:
                                    translation_object.note = note_text
                                # Each translation should have at most one translation note, so stop looping
                                break
                        
                        # Remove the assigned grammatical gender or number for the translation if doesn't has a part of speech
                        if (translation_object.grammatical_gender or translation_object.grammatical_number) and not translation_object.part_of_speech:
                            translation_object.grammatical_gender = None
                            translation_object.grammatical_number = None
                        
                        # Save the translation because the next tags can create objects that will refer to the translation object and thus it should have an id
                        translation_object.save()
                        
                        # Get the context phrase for the current translation
                        for descrip_tag in translation_tag.getElementsByTagName(u"descrip"):
                            descrip_type = descrip_tag.getAttribute(u"type")
                            if descrip_type == u"context":
                                phrase_object = ContextSentence(translation=translation_object, text=getText(descrip_tag.childNodes))
                                phrase_object.save()
                        
                        # Get the corpus examples for the current translation
                        for xref_tag in translation_tag.getElementsByTagName(u"xref"):
                            xref_type = xref_tag.getAttribute(u"type")
                            if xref_type == u"corpusTrace":
                                xref_target = xref_tag.getAttribute(u"target")
                                xref_description = getText(xref_tag.childNodes)
                                if xref_target and xref_description:
                                    corpus_example_object = CorpusExample(translation=translation_object, address=xref_target, description=xref_description)
                                    corpus_example_object.save()
        
        # Once the file has been completely parsed is time to add the concept relationships and save the concepts. This is done this way since some termEntry refer to termEntries that hasn't being parsed yet
        try:
            for concept_key in concept_pool.keys():
                if concept_pool[concept_key].has_key("subject"):
                    concept_pool[concept_key]["object"].subject_field = concept_pool[concept_pool[concept_key]["subject"]]["object"]
                if concept_pool[concept_key].has_key("broader"):
                    concept_pool[concept_key]["object"].broader_concept = concept_pool[concept_pool[concept_key]["broader"]]["object"]
                if concept_pool[concept_key].has_key("related"):
                    for related_key in concept_pool[concept_key]["related"]:
                        concept_pool[concept_key]["object"].related_concepts.add(concept_pool[related_key]["object"])
                concept_pool[concept_key]["object"].save()
        except:
            # In case of failure during the concept relationships assignment the subject_field and broader_concept must be set to None in order to delete all the glossary data because this two fields have on_delete=models.PROTECT
            for concept_key in concept_pool.keys():
                concept_pool[concept_key]["object"].subject_field = None
                concept_pool[concept_key]["object"].broader_concept = None
                #concept_pool[concept_key]["object"].related_concepts.clear()# Unnecessary. But keep this because in the future may be necessary.
                concept_pool[concept_key]["object"].save()
            raise Exception
    except:
        # Some exception was raised while extracting the data from the uploaded file
        transaction.rollback()
        raise Exception
    else:
        transaction.commit()



@csrf_protect
def import_view(request):
    context = {}
    if request.method == 'POST':
        import_form = ImportForm(request.POST, request.FILES)
        if import_form.is_valid():
            glossary = import_form.save()
            try:
                import_uploaded_file(request.FILES['imported_file'], glossary)
            except:
                glossary.delete()
                import_error_message = _("The uploaded file is not a valid TBX file.")
                context['import_error_message'] = import_error_message
            else:
                # Assign the owner permissions to the file sender
                glossary.assign_terminologist_permissions(request.user)
                glossary.assign_lexicographer_permissions(request.user)
                glossary.assign_owner_permissions(request.user)
                import_message = _("TBX file succesfully imported. Thank you!")
                context['import_message'] = import_message
                import_form = ImportForm()
    else:
        import_form = ImportForm()
    context['import_form'] = import_form
    context['search_form'] = SearchForm()
    context['next'] = request.get_full_path()
    return render_to_response('import.html', context, context_instance=RequestContext(request))



def search(request):
    if request.method == 'GET' and 'search_string' in request.GET:
        if "advanced" in request.path:
            search_form = AdvancedSearchForm(request.GET)
        else:
            search_form = SearchForm(request.GET)
        if search_form.is_valid():
            search_results = []
            try:
                if "advanced" in request.path:
                    queryset = Translation.objects.all()
                    if search_form.cleaned_data['filter_by_glossary']:
                        queryset = queryset.filter(concept__glossary=search_form.cleaned_data['filter_by_glossary'])
                    if search_form.cleaned_data['filter_by_language']:
                        queryset = queryset.filter(language=search_form.cleaned_data['filter_by_language'])
                    #TODO add filter by process status
                    if search_form.cleaned_data['filter_by_part_of_speech']:
                        queryset = queryset.filter(part_of_speech=search_form.cleaned_data['filter_by_part_of_speech'])
                    if search_form.cleaned_data['filter_by_administrative_status']:
                        queryset = queryset.filter(administrative_status=search_form.cleaned_data['filter_by_administrative_status'])
                    
                    if search_form.cleaned_data['also_show_partial_matches']:
                        translation_list = get_list_or_404(queryset, translation_text__icontains=search_form.cleaned_data['search_string'])
                    else:
                        translation_list = get_list_or_404(queryset, translation_text__iexact=search_form.cleaned_data['search_string'])
                else:
                    translation_list = get_list_or_404(Translation, translation_text__iexact=search_form.cleaned_data['search_string'])
                
                previous_concept = None
                for trans in translation_list:
                    try:
                        definition = get_object_or_404(Definition, concept=trans.concept, language=trans.language)
                    except Http404:
                        definition = None
                    if not previous_concept is trans.concept.pk:
                        is_first = True
                        previous_concept = trans.concept.pk
                        try:
                            other_translations = get_list_or_404(Translation.objects.exclude(id=trans.pk), concept=trans.concept)[:7]
                        except Http404:
                            other_translations = None
                    else:
                        other_translations = None
                        is_first = False
                    search_results.append({"translation": trans, "definition": definition, "other_translations": other_translations, "is_first": is_first})
            except Http404:
                pass
        else:
            search_results = None
    else:
        if "advanced" in request.path:
            search_form = AdvancedSearchForm()
        else:
            search_form = SearchForm()
        search_results = None
    context = {'search_form': search_form, 'search_results': search_results}
    context['next'] = request.get_full_path()
    template_name = 'search.html'
    if "advanced" in request.path:
        template_name = 'advanced_search.html'
    return render_to_response(template_name, context, context_instance=RequestContext(request))



