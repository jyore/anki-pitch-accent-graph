# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import platform
import struct
import sys
import uuid
import warnings

from PIL import Image, ImageChops
from selenium import webdriver



__all__ = ['trim', 'random_filename', 'get_driver']


# NOTE: Technically, the phantomjs browser that is being used is being
# deprecated by selenium. We, however, still are running it to avoid
# making people install specific drivers. This statement will "wat"
# the deprecation warnings, hiding it from the end-user
warnings.filterwarnings("ignore", category=UserWarning)



def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        return im


def random_filename():
    return "pitchaccent-%s.png" % uuid.uuid4().hex


def get_driver():
    system = platform.system()

    if system == 'Darwin':
        path = "drivers/osx/phantomjs"
    elif system == 'Linux':
        if struct.calcsize('P') * 8 == 64:
            path = "drivers/linux_x86_64/phantomjs"
        else:
            path = "drivers/linux_i686/phantomjs"
    else:
        path = "drivers/win/phantomjs.exe"

    sys.path.append(os.path.join(os.path.dirname(__file__), path))

    driver = webdriver.PhantomJS(executable_path=os.path.join(os.path.dirname(__file__), path))
    driver.set_window_size(1920,1080)
    return driver
