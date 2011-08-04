# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import patterns
from django.contrib.auth.views import login, logout
from django.contrib.comments.feeds import LatestCommentFeed
from terminator.views import TerminatorListView, TerminatorDetailView, GlossaryDetailView
from terminator.feeds import LatestChangesGenericFeed, LatestChangesFeed
from terminator.models import Glossary, Concept, Proposal, Translation

urlpatterns = patterns('terminator.views',
    (r'^$', 'terminator_index'),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout, {'template_name': 'registration/logout.html'}),
    (r'^glossaries/$', TerminatorListView.as_view(
        model=Glossary,
        context_object_name="glossary_list",
    )),
    (r'^glossaries/(?P<pk>\d+)/$', GlossaryDetailView.as_view(
        model=Glossary,
    )),
    (r'^concepts/(?P<pk>\d+)/$', TerminatorDetailView.as_view(
        model=Concept,
    )),
    (r'^proposals/$', TerminatorListView.as_view(
        model=Proposal,
        context_object_name="proposal_list",
    )),
    (r'^proposals/(?P<pk>\d+)/$', TerminatorDetailView.as_view(
        model=Proposal,
    )),
    (r'^export/$', 'export'),
    (r'^search/$', 'search'),
    (r'^advanced_search/$', 'advanced_search'),
    (r'^feeds/glossaries/$', LatestChangesGenericFeed(Glossary)),
    (r'^feeds/concepts/$', LatestChangesGenericFeed(Concept)),
    (r'^feeds/translations/$', LatestChangesGenericFeed(Translation)),
    (r'^feeds/all/$', LatestChangesFeed((Glossary, Concept, Translation))),
    (r'^feeds/comments/$', LatestCommentFeed()),
)

