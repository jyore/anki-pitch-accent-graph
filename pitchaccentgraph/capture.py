# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aqt.qt import QObject, pyqtSlot, pyqtSignal
from io import BytesIO
from PIL import Image, ImageChops
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select  

from .util import trim, get_driver, random_filename


__all__ = ['CaptureWorker']

class CaptureWorker(QObject):
  finished = pyqtSignal()
  dataReady = pyqtSignal(str)

  @pyqtSlot(list)
  def processB(self, expressions):
    driver = get_driver()

    try:

      for expression in expressions:
        driver.get("http://www.gavo.t.u-tokyo.ac.jp/ojad/eng/phrasing/index")

        WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.ID, 'PhrasingIndexForm'))
        )

        form = driver.find_element_by_id("PhrasingIndexForm")
        text = driver.find_element_by_id("PhrasingText")
        text.send_keys(expression)
        form.submit()


        WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.ID, 'PhrasingPublishIndexForm'))
        )
    
        printform = driver.find_element_by_id('PhrasingPublishIndexForm')
        driver.execute_script('document.getElementById("PhrasingPublishIndexForm").target = ""')
        printform.submit()
    
    
        WebDriverWait(driver, 10).until(
          EC.title_contains('Printable Screen')
        )

        import time
        time.sleep(0.2)
    
        png = driver.get_screenshot_as_png()
        im = trim(Image.open(BytesIO(png)))
        fn = random_filename() 
        im.save(fn)
        self.dataReady.emit(fn)
    
    finally:
      driver.quit()
      self.finished.emit()

