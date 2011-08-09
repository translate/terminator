# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.comments.models import Comment
from django.core.mail import send_mail

class TerminatorComment(Comment):
    mail_me = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        super(TerminatorComment, self).save(*args, **kwargs)
        # Now send an email to all other users that commented in the current thread
        thread_comments = TerminatorComment.objects.filter(content_type=self.content_type, object_pk=self.object_pk).exclude(user=self.user)
        
        emails_to_notify_set = set()
        for comment in thread_comments:
            if comment.user.email and comment.mail_me and not comment.user.email in emails_to_notify_set:
                emails_to_notify_set.add(comment.user.email)
        
        #TODO notificar a todos os outros usuarios subscritos tamén para recibir novas deste glosario
        
        if emails_to_notify_set:
            thread = self.content_type.get_object_for_this_type(pk=self.object_pk)
            mail_subject = "[Terminator] New message in %s thread for concept #%s" % (thread.language.name, thread.concept.pk)
            send_mail(mail_subject, self.comment, 'donotreply@donotreply.com', list(emails_to_notify_set), fail_silently=False)
        
