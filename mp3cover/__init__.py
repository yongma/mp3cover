#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mp3_cover
# __init__.py
# 2017-9-18

__author__ = 'Yong'

import os
import logging
# import magic
from copy import deepcopy

from mutagen import File, MutagenError
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from PIL import Image

from .utils import to_jpeg, mime_type, image_size


log = logging.getLogger(__name__)

FRONT_COVER, BACK_COVER, LEAFLET, MEDIA = range(3, 7)

DESC = {
    FRONT_COVER: 'Front Cover',
    BACK_COVER: 'Back Cover',
    LEAFLET: 'Leaflet',
    MEDIA: 'Media'
}

ROOT_DIR = os.path.dirname(
    os.path.abspath(
        os.path.dirname(__file__)
    )
)


def set_cover(audio_file, cover_file, cover_type=FRONT_COVER):
    """
    Set embedding cover image to mp3 file
    """
    if not os.path.isfile(audio_file):
        log.warning("Invalid audio file path: {}".format(audio_file))
        return False
    if not os.path.isfile(cover_file):
        log.warning("Invalid cover file path: {}".format(cover_file))
        return False
    if cover_type not in range(3, 7):
        log.warning(
            "Invalid cover type: {}, "
            "set to FRONT_COVER by default".format(cover_type)
        )
        cover_type = FRONT_COVER

    audio = MP3(audio_file, ID3=ID3)

    # add ID3 tag if it doesn't exist
    try:
        audio.add_tags()
    except error:
        pass

    audio.tags.add(
        APIC(
            encoding=3,  # 3 is for utf-8
            mime='image/jpeg',  # image/jpeg or image/png
            type=cover_type,  # 3 is for the cover image
            desc=DESC.get(cover_type),
            data=open(cover_file, 'rb').read()
        )
    )
    audio.save()
    return True


def get_cover(audio_file, cover_file=None):
    if not os.path.isfile(audio_file):
        log.warning("Invalid audio file path: {}".format(audio_file))
        return False
    if not cover_file:
        cover_file = 'media.jpg'
    else:
        dir_name = os.path.dirname(cover_file)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
    audio = File(audio_file)  # mutagen can automatically detect format and type of tags
    # log.debug("{}".format(audio.tags))
    artwork = audio.tags['APIC:'].data  # access APIC frame and grab the image
    with open(cover_file, 'wb') as img:
        img.write(artwork)


def cover_info(audio_file):
    if not os.path.isfile(audio_file):
        log.warning("Invalid audio file path: {}".format(audio_file))
        return None
    audio = MP3(audio_file)
    cover_keys = [key for key in audio.tags.keys()
                  if key.startswith('APIC:')]
    if not cover_keys:
        log.warning("No APIC in audio tags")
        return False

    for key in cover_keys:
        cover_type = audio.tags[key].type
        asserted_mime = audio.tags[key].mime
        artwork = audio.tags[key].data
        real_mine = mime_type(artwork)
        width, height = image_size(artwork)

        print "{:<20} {:<30} {}x{}".format(
            DESC.get(cover_type),
            "{}-->{}".format(
                asserted_mime,
                real_mine
            ),
            width, height
        )


def convert_cover(audio_file):
    """
    Just for Netease Cloud Music mp3 files
    """
    if not os.path.isfile(audio_file):
        log.warning("Invalid audio file path: {}".format(audio_file))
        return False
    audio = MP3(audio_file)
    if not audio or not hasattr(audio, "tags") \
            or 'APIC:' not in audio.tags:
        log.debug("Invalid audio or No APIC in audio tags")
        return False
    artwork = audio.tags['APIC:'].data
    # log.debug("Cover type: {}".format(DESC.get(
    #     audio.tags['APIC:'].type
    # )))

    jpeg_artwork = to_jpeg(artwork, resize=320)
    if audio.tags['APIC:'].type != FRONT_COVER:
        audio.tags['APIC:'].type = FRONT_COVER
    audio.tags['APIC:'].data = jpeg_artwork
    audio.tags['APIC:'].mime = 'image/jpeg'
    try:
        audio.save(v2_version=3)
        return True
    except MutagenError:
        log.debug('save fail', exc_info=True)
        return False
    except Exception:
        log.debug('save', exc_info=True)
        return False


def duplicate_front_cover(audio_file):
    """
    Just for Netease Cloud Music mp3 files
    """
    if not os.path.isfile(audio_file):
        log.warning("Invalid audio file path: {}".format(audio_file))
        return False
    audio = MP3(audio_file)
    if 'APIC:' not in audio.tags:
        log.warning("No APIC in audio tags")
        return False
    artwork = audio.tags['APIC:'].data
    asserted_mime = audio.tags['APIC:'].mime
    log.debug("Cover type: {}".format(DESC.get(
        audio.tags['APIC:'].type
    )))
    real_mine = mime_type(artwork)
    jpeg_artwork = to_jpeg(artwork, resize=320)
    if asserted_mime == 'image/jpeg' != real_mine:
        audio.tags['APIC:'].data = jpeg_artwork
    elif asserted_mime != 'image/jpeg':
        audio.tags['APIC:'].data = jpeg_artwork
        audio.tags['APIC:'].mime = 'image/jpeg'
    audio.tags.add(
        APIC(
            encoding=3,  # 3 is for utf-8
            mime='image/jpeg',  # image/jpeg or image/png
            type=FRONT_COVER,  # 3 is for the cover image
            desc=u'Front Cover',
            data=jpeg_artwork
        )
    )
    audio.save(v2_version=3)
    return True


def export_cover(audio_file, dst_dir):
    if not os.path.isfile(audio_file):
        log.warning("Invalid audio file path: {}".format(audio_file))
        return None
    if not os.path.isdir(dst_dir):
        log.warning("Invalid saving directory {}".format(dst_dir))
        return None
    fname, _ = os.path.splitext(
        os.path.basename(audio_file)
    )

    audio = MP3(audio_file)
    cover_keys = [key for key in audio.tags.keys()
                  if key.startswith('APIC:')]
    if not cover_keys:
        log.warning("No APIC in audio tags")
        return False

    for key in cover_keys:
        cover_type = audio.tags[key].type
        asserted_mime = audio.tags[key].mime
        artwork = audio.tags[key].data
        real_mine = mime_type(artwork)

        log.info("{:<20} {:<20} {}".format(
            DESC.get(cover_type),
            asserted_mime,
            real_mine
        ))

        if asserted_mime == 'image/jpeg' != real_mine:
            artwork = to_jpeg(artwork)
        dst_path = os.path.join(
            dst_dir,
            u"{}_{}.jpg".format(
                fname,
                DESC.get(cover_type, '').lower().replace(' ', '_')
            )
        )
        with open(dst_path, 'wb') as f:
            f.write(artwork)