from django.shortcuts import render_to_response, get_object_or_404
from glossaries.models import Glossary


def terminator_index(request):
    return render_to_response('index.html')


def glossary_detail(request, glossary_id):
    glossary = get_object_or_404(Glossary, pk=glossary_id)
    return render_to_response('glossaries/glossary_details.html', {'glossary': glossary})


