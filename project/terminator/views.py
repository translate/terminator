# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404, Http404
from django.views.generic import DetailView, ListView
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from terminator.models import Glossary, Translation, Definition
from terminator.forms import *


class TerminatorDetailView(DetailView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TerminatorDetailView, self).get_context_data(**kwargs)
        # Add the breadcrumbs search form to context
        context['search_form'] = SearchForm()
        return context



class TerminatorListView(ListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TerminatorListView, self).get_context_data(**kwargs)
        # Add the breadcrumbs search form to context
        context['search_form'] = SearchForm()
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
    glossary_list = get_list_or_404(Glossary)
    search_form = SearchForm()
    context_dictionary = {'glossary_list': glossary_list, 'search_form': search_form, 'proposal_form': proposal_form, 'new_proposal_message': new_proposal_message}
    return render_to_response('index.html', context_dictionary, context_instance=RequestContext(request))



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
    return render_to_response('search.html', context)



