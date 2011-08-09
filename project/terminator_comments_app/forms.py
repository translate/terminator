# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import ungettext, ugettext_lazy as _
from django.contrib.comments.forms import CommentForm
from terminator_comments_app.models import TerminatorComment

class TerminatorCommentForm(CommentForm):
    name = forms.CharField(max_length=50, widget=forms.HiddenInput)
    email = forms.EmailField(widget=forms.HiddenInput)
    url = forms.URLField(required=False, widget=forms.HiddenInput)
    mail_me = forms.BooleanField(label=_("Mail me when a new reply is posted"), initial=True, required=False)

    def get_comment_model(self):
        return TerminatorComment
    
    def get_comment_create_data(self):
        data = super(TerminatorCommentForm, self).get_comment_create_data()
        data['mail_me'] = self.cleaned_data['mail_me']
        return data
