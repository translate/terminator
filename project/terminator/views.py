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



def advanced_search(request):#TODO definir clase de vista xenérica para englobar as funcións de busca simple e avanzada?
    if request.method == 'GET' and 'search_string' in request.GET:
        search_form = AdvancedSearchForm(request.GET)
        if search_form.is_valid():
            search_results = []
            try:
                queryset = Translation.objects.all()
                if search_form.cleaned_data['also_show_partial_matches']:
                    queryset = queryset.filter(translation_text__icontains=search_form.cleaned_data['search_string'])
                else:
                    queryset = queryset.filter(translation_text__iexact=search_form.cleaned_data['search_string'])
                
                if search_form.cleaned_data['filter_by_glossary']:
                    queryset = queryset.filter(concept__glossary=search_form.cleaned_data['filter_by_glossary'])
                
                if search_form.cleaned_data['filter_by_language']:
                    queryset = queryset.filter(language=search_form.cleaned_data['filter_by_language'])
                
                if search_form.cleaned_data['filter_by_part_of_speech']:
                    queryset = queryset.filter(part_of_speech=search_form.cleaned_data['filter_by_part_of_speech'])
                
                if search_form.cleaned_data['filter_by_administrative_status']:
                    queryset = queryset.filter(administrative_status=search_form.cleaned_data['filter_by_administrative_status'])
                
                
                
                #translation_list = get_list_or_404(Translation, translation_text__iexact=search_form.cleaned_data['search_string'])
                translation_list = list(queryset.all())
                if not translation_list:#TODO investigar como conseguir recuperar usando get_list_or_404 #TODO investigar se convén ter resultados separados en exactos e parciais como en glósima (non é mala idea pero pode que requira cambiar o template de resultados e seguro que hai que modificar o contexto proporcionado e o template de advanced_search. E haberá que asegurarse de se hai que meter cambios en base_search.html)
                    raise Http404
                
                
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
    return render_to_response('advanced_search.html', context)



