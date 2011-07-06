# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, get_list_or_404, Http404
from terminator.models import Glossary, Translation, Definition
from terminator.forms import *


def terminator_index(request):
    glossary_list = get_list_or_404(Glossary)
    search_form = SearchForm()
    return render_to_response('index.html', {'glossary_list': glossary_list, 'search_form': search_form})


def search(request):
    if request.method == 'GET':
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            search_results = []
            try:
                translation_list = get_list_or_404(Translation, translation_text__iexact=search_form.cleaned_data['search_string'])
                previous_concept = None
                for trans in translation_list:
                    try:
                        definition = get_list_or_404(Definition, concept=trans.concept, language=trans.language)[0]
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
    return render_to_response('search.html', {'search_form': search_form, 'search_results': search_results})


