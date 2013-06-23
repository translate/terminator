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

from django.conf import settings
from django.contrib.comments.models import Comment
from django.core.mail import send_mail, EmailMessage
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TerminatorComment(Comment):
    mail_me = models.BooleanField(default=True)

    def comment_thread(self):
        return self.content_type.get_object_for_this_type(pk=self.object_pk)
    comment_thread.short_description = _('comment thread')

    def save(self, *args, **kwargs):
        # First of all test if object is in the database.
        try:
            object_in_bd = TerminatorComment.objects.get(pk=self.pk)
        except TerminatorComment.DoesNotExist:
            changed_or_new = _("New")
        else:
            changed_or_new = _("Changed")

        # Call the super implementation.
        super(TerminatorComment, self).save(*args, **kwargs)

        # Send email messages only if allowed in the settings.
        if settings.SEND_NOTIFICATION_EMAILS:
            # Get the set of emails from all other users that commented in the
            # current thread and want to keep updated.
            thread_comments = TerminatorComment.objects.filter(content_type=self.content_type, object_pk=self.object_pk).exclude(user=self.user)
            emails_to_notify_set = set()
            for comment in thread_comments:
                if comment.user.email and comment.mail_me:
                    emails_to_notify_set.add(comment.user.email)

            # Get the set of emails from users that subscribed to glossary
            # updates.
            for subscriber in self.comment_thread().concept.glossary.subscribers.exclude(pk=self.user.pk):
                emails_to_notify_set.add(subscriber.email)

            #TODO Add the language mailing list address to emails_to_notify_set

            # Now send an email to all other users that commented in the
            # current thread or have subscribed to the glossary.
            if emails_to_notify_set:
                thread = self.comment_thread()
                subject_data = {
                    'changed_or_new': changed_or_new,
                    'language': thread.language.name,
                    'concept': thread.concept.pk
                }
                mail_subject = _('[Terminator] %(changed_or_new)s message in '
                                 '%(language)s thread for concept '
                                 '#%(concept)s') % subject_data
                email = EmailMessage(mail_subject, self.comment,
                                     'donotreply@donotreply.com',
                                     bcc=list(emails_to_notify_set))
                email.send(fail_silently=False)
                #TODO the two lines of code above try to send the message using
                # only BCC field in order to avoid all the recipients to see
                # the email addresses of the other recipients. If it fails
                # comment the two lines above and uncomment the following one
                # that send the email message without using the BCC field.
                #send_mail(mail_subject, self.comment,
                #          'donotreply@donotreply.com',
                #          list(emails_to_notify_set), fail_silently=False)
