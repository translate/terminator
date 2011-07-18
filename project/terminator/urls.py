# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import patterns
from django.contrib.auth.views import login
from terminator.views import TerminatorListView, TerminatorDetailView
from terminator.models import Glossary, Concept, Proposal

urlpatterns = patterns('terminator.views',
    (r'^$', 'terminator_index'),
    (r'^accounts/login/$', login),
    (r'^glossaries/$', TerminatorListView.as_view(
        model=Glossary,
        context_object_name="glossary_list",
    )),
    (r'^glossaries/(?P<pk>\d+)/$', TerminatorDetailView.as_view(
        model=Glossary,
    )),
    (r'^concepts/(?P<pk>\d+)/$', TerminatorDetailView.as_view(
        model=Concept,
    )),
    (r'^proposals/$', TerminatorListView.as_view(
        model=Proposal,
        context_object_name="proposal_list",
    )),
    (r'^search/$', 'search'),
    (r'^advanced_search/$', 'advanced_search'),
)

