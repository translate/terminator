from django.conf.urls.defaults import patterns
from django.views.generic import ListView
from glossaries.models import Glossary, Concept

urlpatterns = patterns('glossaries.views',
    (r'^$', 'terminator_index'),
    (r'^glossaries/$', ListView.as_view(
        model=Glossary,
        context_object_name="glossary_list",
    )),
    (r'^glossaries/(?P<glossary_id>\d+)/$', 'glossary_detail'),
    (r'^concepts/$', ListView.as_view(
        model=Concept,
        context_object_name="concept_list",
    )),
)

