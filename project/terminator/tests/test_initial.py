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

from django.test import TestCase

from terminator.models import *


class LanguageTest(TestCase):

    def setUp(self):
        """
        Setting up environment to execute the tests.
        """
        self.verb = PartOfSpeech.objects.get(pk=1)
        self.noun = PartOfSpeech.objects.get(pk=2)
        self.feminine = GrammaticalGender.objects.get(pk=1)
        self.masculine = GrammaticalGender.objects.get(pk=2)
        self.singular = GrammaticalNumber.objects.get(pk=1)
        self.plural = GrammaticalNumber.objects.get(pk=2)
        self.english = Language.objects.get(pk="en")
        self.chinese = Language.objects.get(pk="zh")
        self.castelanismo = AdministrativeStatusReason.objects.get(pk=1)
        self.galicism = AdministrativeStatusReason.objects.get(pk=4)

    def test_language_allows_part_of_speech(self):
        """
        Tests that returns: True for an allowed PartOfSpeech
                            False for one that doesn't
                            False for a non PartOfSpeech object
        """
        self.assertTrue(self.english.allows_part_of_speech(self.verb))
        self.assertFalse(self.english.allows_part_of_speech(self.noun))
        self.assertFalse(self.english.allows_part_of_speech(self.masculine))

    def test_language_allows_grammatical_gender(self):
        """
        Tests that returns: True for an allowed GrammaticalGender
                            False for one that doesn't
                            False for a non GrammaticalGender object
        """
        self.assertTrue(self.english.allows_grammatical_gender(self.feminine))
        self.assertFalse(self.english.allows_grammatical_gender(self.masculine))
        self.assertFalse(self.english.allows_grammatical_gender(self.noun))

    def test_language_allows_grammatical_number(self):
        """
        Tests that returns: True for an allowed GrammaticalNumber
                            False for one that doesn't
                            False for a non GrammaticalNumber object
        """
        self.assertTrue(self.chinese.allows_grammatical_number(self.singular))
        self.assertFalse(self.chinese.allows_grammatical_number(self.plural))
        self.assertFalse(self.chinese.allows_grammatical_number(self.noun))

    def test_language_allows_administrative_status_reason(self):
        """
        Tests that returns: True for an allowed AdministrativeStatusReason
                            False for one that doesn't
                            False for a non AdministrativeStatusReason object
        """
        self.assertTrue(self.english.allows_administrative_status_reason(self.galicism))
        self.assertFalse(self.english.allows_administrative_status_reason(self.castelanismo))
        self.assertFalse(self.english.allows_administrative_status_reason(self.noun))


class PartOfSpeechTest(TestCase):

    def setUp(self):
        """
        Setting up environment to execute the tests.
        """
        self.verb = PartOfSpeech.objects.get(pk=1)
        self.noun = PartOfSpeech.objects.get(pk=2)
        self.chinese = Language.objects.get(pk="zh")
        self.galician = Language.objects.get(pk="gl")

    def test_part_of_speech_allows_grammatical_gender_for_language(self):
        """
        Tests that returns: True for an existing Language/PartOfSpeech relationshiop allowing GrammaticalGender
                            False for an existing Language/PartOfSpeech relationship that doesn't allows GrammaticalGender
                            False for an unexisting Language/PartOfSpeech relationship
                            False for a non-Language/PartOfSpeech relationship
        """
        self.assertTrue(self.noun.allows_grammatical_gender_for_language(self.galician))
        self.assertFalse(self.verb.allows_grammatical_gender_for_language(self.galician))
        self.assertFalse(self.verb.allows_grammatical_gender_for_language(self.chinese))
        self.assertFalse(self.verb.allows_grammatical_gender_for_language(self.noun))

    def test_part_of_speech_allows_grammatical_number_for_language(self):
        """
        Tests that returns: True for an existing Language/PartOfSpeech relationshiop allowing GrammaticalNumber
                            False for an existing Language/PartOfSpeech relationship that doesn't allows GrammaticalNumber
                            False for an unexisting Language/PartOfSpeech relationship
                            False for a non-Language/PartOfSpeech relationship
        """
        self.assertTrue(self.noun.allows_grammatical_number_for_language(self.galician))
        self.assertFalse(self.verb.allows_grammatical_number_for_language(self.galician))
        self.assertFalse(self.verb.allows_grammatical_number_for_language(self.chinese))
        self.assertFalse(self.verb.allows_grammatical_number_for_language(self.noun))


class AdministrativeStatusTest(TestCase):

    def setUp(self):
        """
        Setting up environment to execute the tests.
        """
        self.admitted = AdministrativeStatus.objects.get(pk="admittedTerm-admn-sts")
        self.not_recommended = AdministrativeStatus.objects.get(pk="deprecatedTerm-admn-sts")

    def test_part_of_speech_allows_grammatical_gender_for_language(self):
        """
        Tests that returns: True for an AdministrativeStatus allowing the setting of an AdministrativeStatusReason
                            False for an AdministrativeStatus that doesn't allows the setting of an AdministrativeStatusReason
        """
        self.assertTrue(self.not_recommended.allows_administrative_status_reason)
        self.assertFalse(self.admitted.allows_administrative_status_reason)
