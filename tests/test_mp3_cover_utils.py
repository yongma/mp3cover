#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mp3_cover
# test_mp3_cover_utils
# 2017-9-18

__author__ = 'Yong'

import os
import logging
import unittest
from mp3cover.utils import ROOT_DIR, file_info
from mp3cover import duplicate_front_cover, cover_info

SAMPLE = os.path.join(ROOT_DIR,
                      'data', 'mp3', 'test3.mp3')
COVER = os.path.join(ROOT_DIR,
                     'data', 'cover', 'test.jpg')
MEDIA_DIR = "D:\Transfer\exp"

log = logging.getLogger(__name__)


class Mp3CoverTestCase(unittest.TestCase):
    def setUp(self):
        print '\n'
        pass

    def tearDown(self):
        pass

    def ntest_file_info(self):
        for i in range(1, 4):
            mp3 = os.path.join(
                ROOT_DIR, 'data', 'mp3',
                'test{}.mp3'.format(i)
            )
            log.debug("[{}]".format(mp3))
            file_info(mp3)
    #
    # def test_export_cover(self):
    #     if os.path.isfile(COVER):
    #         os.remove(COVER)
    #     export_cover(SAMPLE, COVER)
    #     self.assertTrue(os.path.isfile(COVER))
    #
    # def test_set_cover(self):
    #     new_cover = os.path.join(
    #         ROOT_DIR, 'data', 'cover', 'front.jpg'
    #     )
    #     self.assertTrue(os.path.isfile(new_cover))
    #     set_front_cover(SAMPLE, new_cover)
    #     file_info(SAMPLE)
    #

    def ntest_netease_transfer(self):
        sample2 = os.path.join(
            ROOT_DIR, 'data', 'mp3', 'test3.mp3'
        )
        self.assertTrue(os.path.isfile(sample2))
        duplicate_front_cover(sample2)

    # def test_cover_info(self):
    #     for fn in os.listdir(u'{}'.format(MEDIA_DIR)):
    #         mp3 = os.path.join(MEDIA_DIR, fn)
    #         print u'{:<30}'.format(fn)
    #         cover_info(mp3)