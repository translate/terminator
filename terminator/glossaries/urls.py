from django.conf.urls.defaults import patterns

urlpatterns = patterns('glossaries.views',
    (r'^$', 'terminator_index'),
)

