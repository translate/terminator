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

from django.conf.urls import url
from django.contrib.auth.models import User
from django_comments.feeds import LatestCommentFeed

from terminator import feeds
from terminator import views
from terminator.models import Concept, Glossary, Proposal, Translation
from terminator_comments_app.feeds import CommentThreadFeed


urlpatterns = [
    url(r'^$',
        views.terminator_index,
        name='terminator_index'),

    # Glossaries URLs
    url(r'^glossaries/$',
        views.TerminatorListView.as_view(
            model=Glossary,
            context_object_name="glossary_list",
        ),
        name='terminator_glossary_list'),
    url(r'^glossaries/(?P<pk>\d+)/$',
        views.GlossaryDetailView.as_view(
            model=Glossary,
        ),
        name='terminator_glossary_detail'),

    # Concepts URLs
    url(r'^concepts/(?P<pk>\d+)/$',
        views.ConceptDetailView.as_view(
            model=Concept,
        ),
        name='terminator_concept_detail'),
    url(r'^concepts/(?P<pk>\d+)/(?P<lang>\w+)/$',
        views.ConceptDetailView.as_view(
            model=Concept,
        ),
        name='terminator_concept_detail_for_language'),

    # Proposal URLs
    url(r'^proposals/$',
        views.TerminatorListView.as_view(
            model=Proposal,
            context_object_name="proposal_list",
        ),
        name='terminator_proposal_list'),
    url(r'^proposals/(?P<pk>\d+)/$',
        views.TerminatorDetailView.as_view(
            model=Proposal,
        ),
        name='terminator_proposal_detail'),

    # Export URLs
    url(r'^export/$',
        views.export,
        name='terminator_export'),

    # Search URLs
    url(r'^search/$',
        views.search,
        name='terminator_search'),
    url(r'^advanced_search/$',
        views.search,
        name='terminator_advanced_search'),

    # Feed URLs
    url(r'^feeds/glossaries/$',
        feeds.LatestChangesGenericFeed(Glossary),
        name='terminator_feed_glossaries'),
    url(r'^feeds/concepts/$',
        feeds.LatestChangesGenericFeed(Concept),
        name='terminator_feed_concepts'),
    url(r'^feeds/translations/$',
        feeds.LatestChangesGenericFeed(Translation),
        name='terminator_feed_translations'),
    url(r'^feeds/all/$',
        feeds.LatestChangesFeed((Glossary, Concept, Translation)),
        name='terminator_feed_all'),
    url(r'^feeds/comments/$',
        LatestCommentFeed(),
        name='terminator_feed_comments'),
    url(r'^feeds/comments/(?P<concept_id>\d+)/(?P<language_id>\w+)/$',
        CommentThreadFeed(),
        name='terminator_feed_commentthread'),

    # Autoterm URLs
    url(r'^autoterm/$',
        views.TerminatorTemplateView.as_view(
            template_name="autoterm.html"
        ),
        name='terminator_autoterm_index'),
    url(r'^autoterm/(?P<language_code>\w+)/$',
        views.autoterm,
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
        views.import_view,
        name='terminator_import'),

    # Profile URLs
    url(r'^profiles/(?P<username>\w+)/$',
        views.terminator_profile_detail,
        name='profiles_profile_detail'),
    url(r'^profiles/$',
        views.ProfileListView.as_view(
            model=User,
            context_object_name="user_list",
            template_name="profiles/profile_list.html"
        ),
        name='profiles_profile_list'),

    # Help URLs
    url(r'^help/$',
        views.TerminatorTemplateView.as_view(
            template_name="help.html"
        ),
        name='terminator_help'),
]
