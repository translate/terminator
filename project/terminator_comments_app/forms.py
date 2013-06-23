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

from django import forms
from django.contrib.comments.forms import CommentForm
from django.utils.translation import ugettext_lazy as _

from terminator_comments_app.models import TerminatorComment


class TerminatorCommentForm(CommentForm):
    name = forms.CharField(max_length=50, widget=forms.HiddenInput)
    email = forms.EmailField(widget=forms.HiddenInput)
    url = forms.URLField(required=False, widget=forms.HiddenInput)
    mail_me = forms.BooleanField(label=_("Mail me when a new reply is posted"),
                                 initial=True, required=False)

    def get_comment_model(self):
        return TerminatorComment

    def get_comment_create_data(self):
        data = super(TerminatorCommentForm, self).get_comment_create_data()
        data['mail_me'] = self.cleaned_data['mail_me']
        return data
