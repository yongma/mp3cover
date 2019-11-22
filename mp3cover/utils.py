#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mp3_cover
# utils
# 2017-9-18

__author__ = 'Yong'

import os
import logging
import json
import cStringIO
import magic

from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

from PIL import Image

_current_dir = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.normpath(os.path.join(_current_dir, ".."))

log = logging.getLogger(__name__)
logging.getLogger('PIL').setLevel(logging.WARNING)


def utf8_string(text):
    if not text:
        return None
    elif isinstance(text, unicode):
        return text.encode('utf-8')
    else:
        return text


def to_json(v, pretty=True):
    """
    Convert object to json string, with encoding exception handling.
    @:param v: object to be converted
    @:return : json string
    """
    value = None
    if pretty is True:
        indent = 4
    else:
        indent = None
    try:
        value = json.dumps(v, indent=indent)
    except:
        try:
            value = json.dumps(v, ensure_ascii=False, indent=indent)
        except:
            log.error('json dumps', exc_info=True)
    return value


def mime_type(artwork):
    magic_file = os.path.join(
        ROOT_DIR, 'bin', 'magic.mgc'
    )
    mf = magic.Magic(
        magic_file=magic_file,
        mime=True,
        uncompress=True
    )
    return mf.from_buffer(artwork)


def to_jpeg(png_data, resize=0):
    if not png_data:
        log.warning("No data to convert")
        return None
    im = Image.open(cStringIO.StringIO(png_data))
    if not im.mode == 'RGB':
        im = im.convert('RGB')
    if resize > 0:
        new_size = resize, resize
        im.thumbnail(new_size, Image.ANTIALIAS)
    fake_file = cStringIO.StringIO()
    im.save(fake_file, "jpeg")
    return fake_file.getvalue()


def image_size(image_data):
    if not image_data:
        log.warning("No data to convert")
        return None
    with Image.open(cStringIO.StringIO(image_data)) as im:
        return im.size


def file_info(audio_file):
    if not os.path.isfile(audio_file):
        log.warning("Invalid audio file path: {}".format(audio_file))
        return False
    audio = MP3(audio_file)
    log.info('-------PPRINT--------')
    audio.pprint()
    log.info('-------INFO--------')
    info = vars(audio.info)
    log.info("\n{}".format(to_json(info)))

    log.info('--------ID3---------')
    aid3 = ID3(audio_file)
    log.info('ID3 version: {}'.format(aid3.version))

    log.info('-------File--------')
    f = File(audio_file)
    for k, v in f.items():
        if k.startswith("APIC:") or k.startswith("COMM:"):
            continue
        log.debug("[{}]:{}".format(k, v))

    log.info('-------APIC--------')
    apic = f.tags.get("APIC:")
    info = dict()
    for k, v in vars(apic).items():
        k = utf8_string(k)
        if k == 'data':
            continue
        v = utf8_string(v)
        info[k] = v
    log.info("\n{}".format(to_json(info)))


def gbk_string(text):
    if not text:
        return ""
    if isinstance(text, unicode):
        return text.encode('gb2312')
    else:
        return text.decode().encode('gb2312')
