from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.test import TestCase
from django.core.urlresolvers import reverse
# later Django versions:
#from django.utils import reverse

from terminator_comments_app.forms import *
from terminator_comments_app.models import *

from terminator.models import *


CT = ContentType.objects.get_for_model


class TestComments(TestCase):

    fixtures = ['test_data']

    def test_model(self):
        user = User.objects.create_user(username="test", email="test@test.com", password="test")
        comment = TerminatorComment.objects.create(
            content_type=CT(Translation),
            object_pk="1",
            user=user,
            site=Site.objects.get_current(),
        )
        comment.save()

    def getValidData(self, obj, data):
        # Based on django-contrib-comments/__init__.py
        f = TerminatorCommentForm(obj)
        data.update(f.initial)
        return obj, data

    def test_form(self):
        translation = Translation.objects.get(pk=1)
        form = TerminatorCommentForm(
                *self.getValidData(translation, {
                    "name": "Name",
                    "email": "asdf@example.com",
                    "url": "",
                    "comment": "asdf",
        }))
        self.assertEquals(form.is_valid(), True, str(form))
        form.get_comment_model()
        form.get_comment_create_data()

    def test_feed(self):
        response = self.client.get(reverse("terminator_feed_comments"))
        self.assertEquals(response.status_code, 200)
        response = self.client.get(reverse("terminator_feed_commentthread", kwargs={
            "concept_id": 1,
            "language_id": 'en'
        }))
        self.assertEquals(response.status_code, 404)

        concept = Concept.objects.get(pk=1)
        language = Language.objects.get(pk='en')
        thread = ConceptLanguageCommentsThread.objects.create(concept=concept, language=language)
        response = self.client.get(reverse("terminator_feed_commentthread", kwargs={
            "concept_id": 1,
            "language_id": 'en'
        }))
        self.assertEquals(response.status_code, 200)
