# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.comments.models import Comment
from django.core.mail import send_mail

class TerminatorComment(Comment):
    mail_me = models.BooleanField(default=True)
    
    def comment_thread(self):
        return self.content_type.get_object_for_this_type(pk=self.object_pk)
    
    def save(self, *args, **kwargs):
        # First of all test if object is in database
        try:
            object_in_bd = TerminatorComment.objects.get(pk=self.pk)
        except TerminatorComment.DoesNotExist:
            changed_or_new = "New"
        else:
            changed_or_new = "Changed"
        
        # Call the super implementation
        super(TerminatorComment, self).save(*args, **kwargs)
        
        # Get the set of emails from all other users that commented in the current thread and want to keep updated
        thread_comments = TerminatorComment.objects.filter(content_type=self.content_type, object_pk=self.object_pk).exclude(user=self.user)
        emails_to_notify_set = set()
        for comment in thread_comments:
            if comment.user.email and comment.mail_me and not comment.user.email in emails_to_notify_set:
                emails_to_notify_set.add(comment.user.email)
        
        # Get the set of emails from users that subscribed to glossary updates
        for subscriber in self.comment_thread().concept.glossary.subscribers.exclude(pk=self.user.pk):
            emails_to_notify_set.add(subscriber.email)
        
        # Now send an email to all other users that commented in the current thread or have subscribed to the glossary
        if emails_to_notify_set:
            thread = self.comment_thread()
            mail_subject = "[Terminator] %s message in %s thread for concept #%s" % (changed_or_new, thread.language.name, thread.concept.pk)
            send_mail(mail_subject, self.comment, 'donotreply@donotreply.com', list(emails_to_notify_set), fail_silently=False)



