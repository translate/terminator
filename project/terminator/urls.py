from django.conf.urls.defaults import patterns
from django.views.generic import ListView
from terminator.models import Glossary

urlpatterns = patterns('terminator.views',
    (r'^$', 'terminator_index'),
    (r'^glossaries/$', ListView.as_view(
        model=Glossary,
        context_object_name="glossary_list",
    )),
    (r'^glossaries/(?P<glossary_id>\d+)/$', 'glossary_detail'),
    (r'^concepts/(?P<concept_id>\d+)/$', 'concept_detail'),
)

