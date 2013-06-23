# -*- coding: UTF-8 -*-
#
# Copyright 2012, 2013 Leandro Regueiro
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

from django.conf import settings
from django.contrib.comments.feeds import LatestCommentFeed
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from terminator.models import ConceptLanguageCommentsThread
from terminator_comments_app import get_model


class CommentThreadFeed(LatestCommentFeed):
    """Feed of latest comments on a given concept comment thread."""

    def get_object(self, request, concept_id, language_id):
        return get_object_or_404(ConceptLanguageCommentsThread,
                                 concept=concept_id, language=language_id)

    def items(self, obj):
        qs = get_model().objects.filter(
            site__pk = settings.SITE_ID,
            is_public = True,
            is_removed = False,
            object_pk = obj.pk,
            content_type = ContentType.objects.get_for_model(obj.__class__)
        )
        if getattr(settings, 'COMMENTS_BANNED_USERS_GROUP', None):
            inner_qs = User.objects.filter(groups__pk=settings.COMMENTS_BANNED_USERS_GROUP)
            qs = qs.filter(~Q(user__in=inner_qs))
        return qs.order_by('-submit_date')[:40]
