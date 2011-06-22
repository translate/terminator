from django.shortcuts import render_to_response, get_list_or_404
from terminator.models import Glossary, Concept


def terminator_index(request):
    glossary_list = get_list_or_404(Glossary)
    return render_to_response('index.html', {'glossary_list': glossary_list})


