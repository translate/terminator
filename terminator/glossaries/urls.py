from django.conf.urls.defaults import patterns
from django.views.generic import ListView
from glossaries.models import Glossary

urlpatterns = patterns('glossaries.views',
    (r'^$', 'terminator_index'),
    (r'^glossaries/$', ListView.as_view(
        model=Glossary,
        context_object_name="glossary_list",
    )),
)

