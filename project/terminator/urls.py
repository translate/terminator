# -*- coding: UTF-8 -*-
#
# Copyright 2011, 2013 Leandro Regueiro
#
# This file is part of Terminator.
#
# Terminator is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Terminator is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Terminator. If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import patterns, url
from django.contrib.comments.feeds import LatestCommentFeed

from terminator.feeds import LatestChangesFeed, LatestChangesGenericFeed
from terminator.models import Concept, Glossary, Proposal, Translation
from terminator.views import (ConceptDetailView, GlossaryDetailView,
                              TerminatorDetailView, TerminatorListView,
                              TerminatorTemplateView)
from terminator_comments_app.feeds import CommentThreadFeed


urlpatterns = patterns('terminator.views',
    url(r'^$',
        'terminator_index',
        name='terminator_index'),

    # Glossaries URLs
    url(r'^glossaries/$',
        TerminatorListView.as_view(
            model=Glossary,
            context_object_name="glossary_list",
        ),
        name='terminator_glossary_list'),
    url(r'^glossaries/(?P<pk>\d+)/$',
        GlossaryDetailView.as_view(
            model=Glossary,
        ),
        name='terminator_glossary_detail'),

    # Concepts URLs
    url(r'^concepts/(?P<pk>\d+)/$',
        ConceptDetailView.as_view(
            model=Concept,
        ),
        name='terminator_concept_detail'),
    url(r'^concepts/(?P<pk>\d+)/(?P<lang>\w+)/$',
        ConceptDetailView.as_view(
            model=Concept,
        ),
        name='terminator_concept_detail_for_language'),

    # Proposal URLs
    url(r'^proposals/$',
        TerminatorListView.as_view(
            model=Proposal,
            context_object_name="proposal_list",
        ),
        name='terminator_proposal_list'),
    url(r'^proposals/(?P<pk>\d+)/$',
        TerminatorDetailView.as_view(
            model=Proposal,
        ),
        name='terminator_proposal_detail'),

    # Export URLs
    url(r'^export/$',
        'export',
        name='terminator_export'),

    # Search URLs
    url(r'^search/$',
        'search',
        name='terminator_search'),
    url(r'^advanced_search/$',
        'search',
        name='terminator_advanced_search'),

    # Feed URLs
    url(r'^feeds/glossaries/$',
        LatestChangesGenericFeed(Glossary),
        name='terminator_feed_glossaries'),
    url(r'^feeds/concepts/$',
        LatestChangesGenericFeed(Concept),
        name='terminator_feed_concepts'),
    url(r'^feeds/translations/$',
        LatestChangesGenericFeed(Translation),
        name='terminator_feed_translations'),
    url(r'^feeds/all/$',
        LatestChangesFeed((Glossary, Concept, Translation)),
        name='terminator_feed_all'),
    url(r'^feeds/comments/$',
        LatestCommentFeed(),
        name='terminator_feed_comments'),
    url(r'^feeds/comments/(?P<concept_id>\d+)/(?P<language_id>\w+)/$',
        CommentThreadFeed(),
        name='terminator_feed_commentthread'),

    # Autoterm URLs
    url(r'^autoterm/$',
        TerminatorTemplateView.as_view(
            template_name="autoterm.html"
        ),
        name='terminator_autoterm_index'),
    url(r'^autoterm/(?P<language_code>\w+)/$',
        'autoterm',
        name='terminator_autoterm_query'),

    # TODO URLs
    #url(r'^query/(?P<language_code>\w+)/(?P<word>\w+)/$',
    #    'query_word',
    #     name='terminator_wordquery'),
    #url(r'^concepts/pending/$',
    #    'pending_concepts',
    #    name='terminator_pending_concepts'),
    #url(r'^concepts/pending/(?P<lang>\w+)/$',
    #    'pending_concepts',
    #    name='terminator_pending_concepts_for_language'),
    #url(r'^comments/latest/$',
    #    'latest_comments',
    #    name='terminator_latest_comments'),
    #url(r'^history/$',
    #    'latest_changes',
    #    name='terminator_latest_changes'),

    # Import URLs
    url(r'^import/$',
        'import_view',
        name='terminator_import'),

    # Profile URLs
    url(r'^profiles/create/$',
        'terminator_profile_create',
        name='profiles_create_profile'),
    url(r'^profiles/edit/$',
        'terminator_profile_edit',
        name='profiles_edit_profile'),
    url(r'^profiles/(?P<username>\w+)/$',
        'terminator_profile_detail',
        name='profiles_profile_detail'),
    url(r'^profiles/$',
        'terminator_profile_list',
        name='profiles_profile_list'),

    # Help URLs
    url(r'^help/$',
        TerminatorTemplateView.as_view(
            template_name="help.html"
        ),
        name='terminator_help'),
)
