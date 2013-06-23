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

from django.contrib import admin
from django.contrib.comments.admin import CommentsAdmin
from django.utils.translation import ugettext_lazy as _

from terminator_comments_app.models import TerminatorComment


class TerminatorCommentAdmin(CommentsAdmin):
    fieldsets = (
        (_('Content'),
           {'fields': ('user', 'mail_me', 'comment')}
        ),
        (_('Metadata'), {
            'classes': ('collapse',),
            'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')
            }
        ),
        (_('Other data'), {
            'classes': ('collapse',),
            'fields': ('content_type', 'object_pk', 'site')
            }
        ),
     )
    list_display = ('user', 'comment_thread', 'ip_address', 'submit_date', 'mail_me', 'is_public', 'is_removed')
    list_filter = ('submit_date', 'mail_me', 'site', 'is_public', 'is_removed')

    def get_actions(self, request):
        actions = super(TerminatorCommentAdmin, self).get_actions(request)
        actions.pop('flag_comments')
        actions.pop('approve_comments')
        actions.pop('remove_comments')
        return actions


admin.site.register(TerminatorComment, TerminatorCommentAdmin)
