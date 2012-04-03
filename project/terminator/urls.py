# -*- coding: UTF-8 -*-
#
# Copyright 2011 Leandro Regueiro
#
# This file is part of Terminator.
# 
# Terminator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Terminator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Terminator.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import patterns, url
from django.contrib.comments.feeds import LatestCommentFeed
from django.views.generic import TemplateView
from terminator.views import TerminatorListView, TerminatorDetailView, GlossaryDetailView, ConceptDetailView
from terminator.feeds import LatestChangesGenericFeed, LatestChangesFeed, CommentThreadFeed
from terminator.models import Glossary, Concept, Proposal, Translation

urlpatterns = patterns('terminator.views',
    url(r'^$', 'terminator_index'),
    url(r'^glossaries/$', TerminatorListView.as_view(
        model=Glossary,
        context_object_name="glossary_list",
    )),
    url(r'^glossaries/(?P<pk>\d+)/$', GlossaryDetailView.as_view(
        model=Glossary,
    )),
    url(r'^concepts/(?P<pk>\d+)/$', ConceptDetailView.as_view(
        model=Concept,
    )),
    url(r'^concepts/(?P<pk>\d+)/(?P<lang>\w+)/$', ConceptDetailView.as_view(
        model=Concept,
    )),
    url(r'^proposals/$', TerminatorListView.as_view(
        model=Proposal,
        context_object_name="proposal_list",
    )),
    url(r'^proposals/(?P<pk>\d+)/$', TerminatorDetailView.as_view(
        model=Proposal,
    )),
    url(r'^export/$', 'export'),
    url(r'^search/$', 'search'),
    url(r'^advanced_search/$', 'search'),
    url(r'^feeds/glossaries/$', LatestChangesGenericFeed(Glossary)),
    url(r'^feeds/concepts/$', LatestChangesGenericFeed(Concept)),
    url(r'^feeds/translations/$', LatestChangesGenericFeed(Translation)),
    url(r'^feeds/all/$', LatestChangesFeed((Glossary, Concept, Translation))),
    url(r'^feeds/comments/$', LatestCommentFeed()),
    url(r'^feeds/comments/(?P<concept_id>\d+)/(?P<language_id>\w+)/$', CommentThreadFeed()),
    url(r'^autoterm/$', TemplateView.as_view(template_name="autoterm.html")),
    url(r'^autoterm/(?P<language_code>\w+)/$', 'autoterm'),
    #url(r'^query/(?P<language_code>\w+)/(?P<word>\w+)/$', 'query_word'),#TODO
    url(r'^import/$', 'import_view'),
    url(r'^profiles/create/$', 'terminator_profile_create', name='profiles_create_profile'),
    url(r'^profiles/edit/$', 'terminator_profile_edit', name='profiles_edit_profile'),
    url(r'^profiles/(?P<username>\w+)/$', 'terminator_profile_detail', name='profiles_profile_detail'),
    url(r'^profiles/$', 'terminator_profile_list', name='profiles_profile_list'),
    url(r'^help/$', TemplateView.as_view(template_name="help.html")),
)

