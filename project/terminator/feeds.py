# -*- coding: UTF-8 -*-
#
# Copyright 2011 Leandro Regueiro
#
# This file is part of Terminator.
# 
# Terminator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Terminator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Terminator.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.syndication.views import Feed
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class LatestChangesGenericFeed(Feed):
    link = "/"
    
    def __init__(self, model):
        self.model = model
        self.title = _(u"Terminator latest %(model_name)s changes" % {'model_name': model._meta.verbose_name_plural})
        self.description = _(u"Updates on %(model_name)s additions, changes and deletions to Terminator." % {'model_name': model._meta.verbose_name_plural})
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
        return u"/%s/%s/" % (self.model._meta.verbose_name_plural, item.object_id)#FIXME isto apunta a /translations/19/ para a tradu 19 en vez de ao seu concepto. Para resolvelo creo que habería que poñer outra clase á parte para as traducións, que herde desta, pero que redefina este método en particular, pero aínda así queda o problema do fío global para todos os cambios. Mirar se se pode poñer un método get_absolute_url en translation ou onde raio toque para que apunta ao enderezo correcto#FIXME ao internacionalizar e localizar o verbose_name_plural de todos os modelo afectados non mostra correctamente a ligazón, senón que a mostra localizada, quizais solucionar buscando a forma de indicar o idioma inglés de forma local e así devolver as ligazóns correctamente. Quizais sexa boa idea separar en diferentes clases dado que non se axeita ben para Translation
    
    def item_description(self, item):
        if item.is_addition() or item.is_deletion():
            return self.item_title(item)
        return item.change_message
    
    def item_guid(self, item):
        return u"%d" % item.id



class LatestChangesFeed(Feed):
    title = _("Terminator latest changes")
    link = "/"
    description = _("Updates on latest additions, changes and deletions to Terminator.")
    
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
        return u"/%s/%s/" % (ContentType.objects.get_for_id(item.content_type_id).model_class()._meta.verbose_name_plural, item.object_id)#FIXME isto apunta a /translations/19/ para a tradu 19 en vez de ao seu concepto
    
    def item_description(self, item):
        if item.is_addition() or item.is_deletion():
            return self.item_title(item)
        return item.change_message
    
    def item_guid(self, item):
        return u"%d" % item.id



