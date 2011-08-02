# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404, Http404
from django.views.generic import DetailView, ListView
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.db import IntegrityError, transaction
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from terminator.models import Glossary, Translation, Definition
from terminator.forms import *


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
            form = CollaborationRequestForm(self.request.POST)
            if form.is_valid():
                collaboration_request = form.save(commit=False)
                collaboration_request.user = self.request.user
                collaboration_request.for_glossary = self.object
                try:
                    collaboration_request.save()
                except IntegrityError:
                    transaction.rollback()
                    error_message = "You already sent a similar request for this glossary!"
                    context['collaboration_request_error_message'] = error_message
                    #TODO consider updating the request DateTimeField to now and then save
                else:
                    transaction.commit()
                    message = "You will receive a message when the glossary owners have considerated your request."
                    context['collaboration_request_message'] = message
                    form = CollaborationRequestForm()
        else:
            form = CollaborationRequestForm()
        context['collaboration_request_form'] = form
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
            new_proposal_message = "Thank you for sending a new proposal. You may send more!"
            proposal_form = ProposalForm()
    else:
        proposal_form = ProposalForm()
    search_form = SearchForm()
    context = {'search_form': search_form, 'proposal_form': proposal_form, 'new_proposal_message': new_proposal_message}
    context['next'] = request.get_full_path()
    context['glossary_list'] = get_list_or_404(Glossary)
    context['latest_proposals'] = Proposal.objects.order_by("-id")[:8]
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
    #context['latest_comment_changes'] = #TODO engadir últimos comentarios
    return render_to_response('index.html', context, context_instance=RequestContext(request))



def search(request):
    if request.method == 'GET' and 'search_string' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            search_results = []
            try:
                translation_list = get_list_or_404(Translation, translation_text__iexact=search_form.cleaned_data['search_string'])
                previous_concept = None
                for trans in translation_list:
                    try:
                        definition = get_object_or_404(Definition, concept=trans.concept, language=trans.language)
                    except Http404:
                        definition = None
                    if not previous_concept is trans.concept.id:
                        is_first = True
                        previous_concept = trans.concept.id
                        try:
                            other_translations = get_list_or_404(Translation.objects.exclude(id=trans.id), concept=trans.concept)[:7]
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
        search_form = SearchForm()
        search_results = None
    context = {'search_form': search_form, 'search_results': search_results}
    context['next'] = request.get_full_path()
    return render_to_response('search.html', context, context_instance=RequestContext(request))



def advanced_search(request):
    if request.method == 'GET' and 'search_string' in request.GET:
        search_form = AdvancedSearchForm(request.GET)
        if search_form.is_valid():
            search_results = []
            try:
                queryset = Translation.objects.all()
                if search_form.cleaned_data['filter_by_glossary']:
                    queryset = queryset.filter(concept__glossary=search_form.cleaned_data['filter_by_glossary'])
                if search_form.cleaned_data['filter_by_language']:
                    queryset = queryset.filter(language=search_form.cleaned_data['filter_by_language'])
                if search_form.cleaned_data['filter_by_part_of_speech']:
                    queryset = queryset.filter(part_of_speech=search_form.cleaned_data['filter_by_part_of_speech'])
                if search_form.cleaned_data['filter_by_administrative_status']:
                    queryset = queryset.filter(administrative_status=search_form.cleaned_data['filter_by_administrative_status'])
                
                if search_form.cleaned_data['also_show_partial_matches']:
                    translation_list = get_list_or_404(queryset, translation_text__icontains=search_form.cleaned_data['search_string'])
                else:
                    translation_list = get_list_or_404(queryset, translation_text__iexact=search_form.cleaned_data['search_string'])
                
                previous_concept = None
                for trans in translation_list:
                    try:
                        definition = get_object_or_404(Definition, concept=trans.concept, language=trans.language)
                    except Http404:
                        definition = None
                    if not previous_concept is trans.concept.id:
                        is_first = True
                        previous_concept = trans.concept.id
                        try:
                            other_translations = get_list_or_404(Translation.objects.exclude(id=trans.id), concept=trans.concept)[:7]
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
        search_form = AdvancedSearchForm()
        search_results = None
    context = {'search_form': search_form, 'search_results': search_results}
    context['next'] = request.get_full_path()
    return render_to_response('advanced_search.html', context, context_instance=RequestContext(request))



