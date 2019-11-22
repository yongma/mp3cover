#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mp3_cover
# mp3_cover
# 2017-9-18

__author__ = 'Yong'

import sys
import os
import logging

rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

log_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(log_formatter)
rootLogger.addHandler(consoleHandler)


ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)
if sys.stdout.encoding == "cp936":
    DEFAULT_ENCODING = 'gb18030'
else:
    DEFAULT_ENCODING = 'utf-8'


def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


def dup_dir(dir_path):
    from mp3cover import duplicate_front_cover
    for fn in os.listdir(u'{}'.format(dir_path)):
        if not fn.lower().endswith(".mp3"):
            continue
        mp3 = os.path.join(dir_path, fn)
        print u"-->{}".format(fn)
        duplicate_front_cover(mp3)


def cov_dir(dir_path):
    from mp3cover import convert_cover
    result = {'succ': 0, 'fail': 0, 'title': 0}
    for i, fn in enumerate(os.listdir(u'{}'.format(dir_path))):
        if not fn.lower().endswith(".mp3"):
            continue
        # print u"-->{0:{1}<64}".format(fn, u" ").encode(DEFAULT_ENCODING),
        result['title'] += 1
        print "-->{:<72}".format(fn.encode(DEFAULT_ENCODING)),
        mp3 = os.path.join(dir_path, fn)
        ret = convert_cover(mp3)
        if ret is True:
            result['succ'] += 1
            print "ok"
        else:
            result['fail'] += 1
            print "fail"
    return result


def export_covers(audio_path, cover_path):
    from mp3cover import export_cover
    if not cover_path:
        os.makedirs(cover_path)
    for fn in os.listdir(u'{}'.format(audio_path)):
        mp3 = os.path.join(audio_path, fn)
        print fn
        export_cover(mp3, cover_path)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        print u"-目录：{}".format(cur_dir).encode(DEFAULT_ENCODING)
        result = cov_dir(cur_dir)
        print "\r\n"
        print u"共处理{}个mp3，其中成功{}个，失败{}个".format(
            result.get('title') or 0,
            result.get('succ') or 0,
            result.get('fail') or 0
        ).encode(DEFAULT_ENCODING)
        print "\r\n"
        kw = raw_input(u"输入任意字符退出: ".encode(DEFAULT_ENCODING))
        if kw:
            sys.exit(0)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "test":
        rootLogger.setLevel(logging.DEBUG)
        test()

    elif cmd == "dup":
        dir_path = sys.argv[2]
        if os.path.isdir(dir_path):
            dup_dir(dir_path)
        else:
            logging.warning("Invalid path: {}".format(dir_path))
    elif cmd == "cov":
        dir_path = sys.argv[2]
        if os.path.isdir(dir_path):
            print u"目录：{}".format(dir_path).encode(DEFAULT_ENCODING)
            result = cov_dir(dir_path)
            print u"共处理{}个mp3，其中成功{}个，失败{}个".format(
                result.get('succ') or 0 + result.get('fail') or 0,
                result.get('succ') or 0,
                result.get('fail') or 0
            ).encode(DEFAULT_ENCODING)
            kw = raw_input(u"输入任意字符退出: ".encode(DEFAULT_ENCODING))
            if kw:
                sys.exit(0)
        else:
            print u"无效目录：{}".format(dir_path).encode(DEFAULT_ENCODING)
            logging.warning("Invalid path: {}".format(dir_path))
    elif cmd == "export":
        audio_path = sys.argv[2]
        cover_path = sys.argv[3]
        if os.path.isdir(audio_path):
            export_covers(audio_path, cover_path)
        else:
            logging.warning(
                "Invalid path: {}".format(audio_path)
            )
    else:
        print "Usage: python mp3_cover.py {PATH_TO_MP3_DIR}"
