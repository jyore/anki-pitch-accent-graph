# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import aqt

#XXX: TEMP
def dummy(obj):
  from .capture import generate
  generate("あそこに立ってる人、もしかして部長!?", result)


#XXX: TEMP
def result(image):
  import uuid

  fn = "%s.png" % uuid.uuid4()
  image.save(fn) 
  aqt.utils.showInfo(fn)



def add_to_note(menu):
  #TODO: Get current note being edited
  #TODO: Is current card different than new card?
  pass

def bulk_add(browser):
  #TODO: Config for bulk run?
  notes = browser.selectedNotes()

def configure(mw):
  #TODO: Configuration ideas?
  pass
