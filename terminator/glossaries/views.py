from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from glossaries.models import Glossary, Concept


def terminator_index(request):
    glossary_list = get_list_or_404(Glossary)
    return render_to_response('index.html', {'glossary_list': glossary_list})


def glossary_detail(request, glossary_id):
    glossary = get_object_or_404(Glossary, pk=glossary_id)
    return render_to_response('glossaries/glossary_details.html', {'glossary': glossary})


def concept_detail(request, concept_id):
    concept = get_object_or_404(Concept, pk=concept_id)
    return render_to_response('glossaries/concept_details.html', {'concept': concept})


