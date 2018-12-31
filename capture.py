# -*- coding: utf-8 -*-

import time

from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select  

from .util import trim, get_driver, random_filename


# Errors will bubble up to be hanled closer to the UI
def capture(reference, expression):

    driver = get_driver()
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

    time.sleep(0.1)

    driver.execute_script("$('.ds_t, input, select, font').hide()")
    
    png = driver.get_screenshot_as_png()
    im = trim(Image.open(BytesIO(png)))
    fn = random_filename() 
    im.save(fn)

    driver.quit()

    return {
        'ref': reference, 
        'fn':  fn,
    }
