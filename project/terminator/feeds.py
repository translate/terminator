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

from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _


class LatestChangesGenericFeed(Feed):
    link = "/"

    def __init__(self, model):
        self.model = model
        self.title = _(u"Terminator latest %(model_name)s changes" %
                       {'model_name': model._meta.verbose_name_plural})
        self.description = _(u"Updates on %(model_name)s additions, changes "
                             "and deletions to Terminator." %
                             {'model_name': model._meta.verbose_name_plural})
        self.ctype = ContentType.objects.get_for_model(model)

    def items(self):
        return LogEntry.objects.filter(content_type=self.ctype).order_by("-action_time")[:20]

    def item_title(self, item):
        if item.is_addition():
            # TRANSLATORS: this is a verb
            message = _(u"Added ")
        elif item.is_deletion():
            # TRANSLATORS: this is a verb
            message = _(u"Deleted ")
        elif item.is_change():
            # TRANSLATORS: this is a verb
            message = _(u"Changed ")
        message += u"%s " % self.ctype.model
        message += item.object_repr
        return message

    def item_link(self, item):
        return u"/%s/%s/" % (self.model._meta.verbose_name_plural, item.object_id)
        #TODO This points to /translations/19/ for the translation 19 instead
        # of pointing to its concept. In order to fix this perhaps should be
        # added another class, only for handling feeds for translations, that
        # inherits from this class, but that overwrites this particular method,
        # but to be true there is also this problem in the global feed for all
        # the changes done in Terminator. Check if a get_absolute_url() method
        # could be added in Translation or wherever should be in order to get
        # it pointing at the right URL.
        #TODO When internationalizing and localizing the verbose_name_plural
        # for all the affected models it doesn't show correctly the URL, but
        # it shows it localized instead. Perhaps fix this by looking for a way
        # to indicate to use the English language in a local way to Gettext and
        # thus returning the right URLs. Maybe it is a good idea to put this in
        # separate classes since it doesn't work fine for Translation.

    def item_description(self, item):
        if item.is_addition() or item.is_deletion():
            return self.item_title(item)
        return item.change_message

    def item_guid(self, item):
        return u"%d" % item.id


class LatestChangesFeed(Feed):
    title = _("Terminator latest changes")
    link = "/"
    description = _("Updates on latest additions, changes and deletions to "
                    "Terminator.")

    def __init__(self, models):
        self.ctypes = []
        for model in models:
            self.ctypes.append(ContentType.objects.get_for_model(model))

    def items(self):
        return LogEntry.objects.filter(content_type__in=self.ctypes).order_by("-action_time")[:20]

    def item_title(self, item):
        if item.is_addition():
            # TRANSLATORS: this is a verb
            message = _(u"Added ")
        elif item.is_deletion():
            # TRANSLATORS: this is a verb
            message = _(u"Deleted ")
        elif item.is_change():
            # TRANSLATORS: this is a verb
            message = _(u"Changed ")
        message += u"%s " % ContentType.objects.get_for_id(item.content_type_id).model
        message += item.object_repr
        return message

    def item_link(self, item):
        return u"/%s/%s/" % (ContentType.objects.get_for_id(item.content_type_id).model_class()._meta.verbose_name_plural, item.object_id)
        #TODO This points to /translations/19/ for the translation 19 instead
        # of pointing to its concept. See comment in item_link() for
        # LatestChangesGenericFeed class in this file.

    def item_description(self, item):
        if item.is_addition() or item.is_deletion():
            return self.item_title(item)
        return item.change_message

    def item_guid(self, item):
        return u"%d" % item.id
