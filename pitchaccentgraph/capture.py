# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aqt import mw
from aqt.qt import *
from aqt.webview import AnkiWebView
from io import BytesIO
from .support.PIL import Image, ImageChops


def convert(image):
  buf = QBuffer()
  buf.open(QBuffer.ReadWrite)
  image.save(buf, "png")
  return Image.open(BytesIO(str(buf.data())))


def trim(image):
  bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
  diff = ImageChops.difference(image, bg)
  diff = ImageChops.add(diff, diff, 2.0, -100)
  bbox = diff.getbbox()
  if bbox:
      return image.crop(bbox)
  else:
      return image


def generate(expression, cb=None):
  web = AnkiWebView()

  def save_image():
    page = web.page()
    page.setViewportSize(page.mainFrame().contentsSize())

    image = QImage(page.viewportSize(), QImage.Format_ARGB32)
    painter = QPainter(image)
    page.mainFrame().render(painter)
    painter.end()

    if cb:
      cb(trim(convert(image)))


  def print_page():
    web.loadFinished.disconnect()

    dom = web.page().mainFrame()
    dom.evaluateJavaScript('document.getElementById("PhrasingPublishIndexForm").target = ""')
    dom.evaluateJavaScript('document.querySelector(\'#PhrasingPublishIndexForm input[type="submit"]\').click()')

    web.loadFinished.connect(lambda: QTimer.singleShot(100, lambda: save_image()))


  def submit_text():
    web.loadFinished.disconnect()

    dom = web.page().mainFrame()
    dom.evaluateJavaScript('document.getElementById("PhrasingText").value = "%s"' % expression)
    dom.evaluateJavaScript('document.getElementById("PhrasingIndexForm").submit()')

    web.loadFinished.connect(print_page)


  web.load(QUrl("http://www.gavo.t.u-tokyo.ac.jp/ojad/phrasing/index"))
  web.loadFinished.connect(submit_text)
