# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from ndic.search import search


class NdicTestCase(TestCase):

    def test_search_korean_word(self):
        test_search_korean_word = "사과"
        test_corresponding_english_word = "(과일) apple"
        self.assertEqual(
            search(test_search_korean_word),
            test_corresponding_english_word,
        )

    def test_search_english_word(self):
        test_search_english_word = "apple"
        test_corresponding_korean_word = "사과"
        self.assertEqual(
            search(test_search_english_word),
            test_corresponding_korean_word,
        )

    def test_search_nonexistent_korean_word(self):
        test_nonexistent_korean_word = "아갸야라"
        self.assertFalse(
            search(test_nonexistent_korean_word),
        )

    def test_search_nonexistent_english_word(self):
        test_nonexistent_english_word = "asfasdfasdf"
        self.assertFalse(
            search(test_nonexistent_english_word),
        )
