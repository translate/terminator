# -*- coding: UTF-8 -*-
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.contrib.comments.feeds import LatestCommentFeed
from django.conf import settings
from terminator.models import ConceptLanguageCommentsThread
from terminator_comments_app import get_model


class LatestChangesGenericFeed(Feed):
    link = "/"
    
    def __init__(self, model):
        self.model = model
        self.title = "Terminator latest %s changes" % model._meta.verbose_name_plural
        self.description = "Updates on %s additions, changes and deletions to Terminator." % model._meta.verbose_name_plural
        self.ctype = ContentType.objects.get_for_model(model)

    def items(self):
        return LogEntry.objects.filter(content_type=self.ctype).order_by("-action_time")[:20]

    def item_title(self, item):
        if item.is_addition():
            message = u"Added "
        elif item.is_deletion():
            message = u"Deleted "
        elif item.is_change():
            message = u"Changed "
        message += u"%s " % self.ctype.model
        message += item.object_repr
        return message
    
    def item_link(self, item):
        return u"/%s/%s/" % (self.model._meta.verbose_name_plural, item.object_id)#FIXME isto apunta a /translations/19/ para a tradu 19 en vez de ao seu concepto

    def item_description(self, item):
        if item.is_addition() or item.is_deletion():
            return self.item_title(item)
        return item.change_message
    
    def item_guid(self, item):
        return u"%d" % item.id



class LatestChangesFeed(Feed):
    title = "Terminator latest changes"
    link = "/"
    description = "Updates on latest additions, changes and deletions to Terminator."
    
    def __init__(self, models):
        self.ctypes = []
        for model in models:
            self.ctypes.append(ContentType.objects.get_for_model(model))

    def items(self):
        return LogEntry.objects.filter(content_type__in=self.ctypes).order_by("-action_time")[:20]

    def item_title(self, item):
        if item.is_addition():
            message = u"Added "
        elif item.is_deletion():
            message = u"Deleted "
        elif item.is_change():
            message = u"Changed "
        message += u"%s " % ContentType.objects.get_for_id(item.content_type_id).model
        message += item.object_repr
        return message
    
    def item_link(self, item):
        return u"/%s/%s/" % (ContentType.objects.get_for_id(item.content_type_id).model_class()._meta.verbose_name_plural, item.object_id)#FIXME isto apunta a /translations/19/ para a tradu 19 en vez de ao seu concepto

    def item_description(self, item):
        if item.is_addition() or item.is_deletion():
            return self.item_title(item)
        return item.change_message
    
    def item_guid(self, item):
        return u"%d" % item.id



class CommentThreadFeed(LatestCommentFeed):
    """Feed of latest comments on a given concept comment thread."""
    
    def get_object(self, request, concept_id, language_id):
        return get_object_or_404(ConceptLanguageCommentsThread, concept=concept_id, language=language_id)
    
    def items(self, obj):
        qs = get_model().objects.filter(
            site__pk = settings.SITE_ID,
            is_public = True,
            is_removed = False,
            object_pk = obj.pk,
            content_type = ContentType.objects.get_for_model(obj.__class__)
        )
        if getattr(settings, 'COMMENTS_BANNED_USERS_GROUP', None):
            where = ['user_id NOT IN (SELECT user_id FROM auth_user_groups WHERE group_id = %s)']
            params = [settings.COMMENTS_BANNED_USERS_GROUP]
            qs = qs.extra(where=where, params=params)
        return qs.order_by('-submit_date')[:40]



