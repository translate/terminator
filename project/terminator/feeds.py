# -*- coding: UTF-8 -*-
from django.contrib.syndication.views import Feed
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType


class LatestChangesFeed(Feed):
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
        message += u"%s " % self.model._meta.verbose_name
        message += item.object_repr
        return message
    
    def item_link(self, item):
        return u"/%s/%s/" % (self.model._meta.verbose_name_plural, item.object_id)

    def item_description(self, item):
        if item.is_addition() or item.is_deletion():
            return self.item_title(item)
        return item.change_message
    
    def item_guid(self, item):
        return u"%d" % item.id



