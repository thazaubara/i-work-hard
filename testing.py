import sys
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, time, timedelta
from selenium.webdriver.common.keys import Keys

import bmd_credentials as credentials
import sys
import time as t

BMD_USER = credentials.BMD_USER
BMD_PASS = credentials.BMD_PASS
BMD_URL = credentials.BASE_URL

def sleep():
    wait_because_bmd_is_slow = 1
    t.sleep(wait_because_bmd_is_slow)

print(f"Using Python Version: {sys.version}")
print("Selenium Version: " + webdriver.__version__)

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
options.add_argument("--window-size=1300,800")

driver = webdriver.Chrome(options=options)
width = driver.get_window_size().get("width")
height = driver.get_window_size().get("height")
print(f"driver set to {width}x{height}")

# GO TO SITE
base_url = "https://finanz.value-one.com/bmdweb2"
print(f"Loading {BMD_URL}")
driver.get(BMD_URL)

def logout_quitdriver():
    # CLICK USER
    sleep()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "NavBtnCMDUser77-btnInnerEl"))).click()
    # CLICK LOGOOUT
    sleep()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "NavBar68ItemCMDLogout-itemEl"))).click()
    print("Logged out. Quitting Driver.")
    driver.quit()

# FILL CREDENTIALS
try:
    txt_username = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "txtuser-inputEl")))
    txt_username.send_keys(BMD_USER)
    txt_password = driver.find_element(By.ID, "txtpass-inputEl")
    txt_password.send_keys(BMD_PASS)
    print("Credentials filled.")
except Exception as e:
    print("Credential input failed. You lost 1 Life.")
    print(e)

# CLICK THE LOGIN BUTTON
try:
    loginbutton = driver.find_element(By.ID, "loginbutton-btnEl")
    loginbutton.click()
    print("Clicked Login Button")
except Exception as e:
    print("Login Button click failed. You lost 1 Life.")
    print(e)

# CLICK THE LEA BUTTON (Eng: SEA)
try:
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "TileButtonPKG584-btnWrap"))).click()
    print("Clicked LEA Button")
except Exception as e:
    print("LEA Button click failed. You probably lost 1 Life.")
    print(e)
    logout_quitdriver()

# CLICK THE SINGLE RECORDING BUTTON
try:
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "TileButtonCID29166-btnWrap"))).click()
    print("Clicked Single Recording Button")
except Exception as e:
    print("Single Recording Button click failed. You probably lost 1 Life.")
    print(e)
    logout_quitdriver()

# CLICK THE "NEW" BUTTON
try:
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "RibbonButtonExt195CID29597-btnEl"))).click()
    print("Clicked New Button")
except Exception as e:
    print("New Button click failed. You probably lost 1 Life.")
    print(e)
    logout_quitdriver()

# DISMISS THE POPUP IF THERE
# sometime there is a popup with text (Please note that the services from 1. January 2024 have not yet been completed!) after the "New" button is clicked
# check if it is there and close it, if not continue as usual
try:
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "MsgBoxBtn0_2859462034720112_1"))).click()
    print("Found & clicked Infobox Button")
except Exception as e:
    print("No infobox found. Continue as usual.")

# INPUT LEA STUFF
"""
Customer: AttrFieldCmbFieldContainer3488384713005013CID4013623UID378-inputEl
Activity: AttrFieldCmbFieldContainer3488384713005013CID4013321UID379-inputEl
Hours: AttrFieldTimeFieldContainer3488384713005013CID4018896UID382-inputEl
Auto. Hours: AttrBtnF8FieldContainer3488384713005013CID4018896UID382-btnWrap
"""

try:
    # STUPID KEYPRESSES. bc it gets reset to 0:00 after click outside input_field.
    # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "AttrFieldTimeFieldContainer3488384713005013CID4018896UID382-inputEl"))).send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, "10:00")
    # OR: CLICK AUTO TIME BOOKING
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "AttrBtnF8FieldContainer3488384713005013CID4018896UID382-btnWrap"))).click()

    t.sleep(2)  # wait bc apparently input fields get loaded afterwards? XD
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "AttrFieldCmbFieldContainer3488384713005013CID4013623UID378-inputEl"))).send_keys("200127")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "AttrFieldCmbFieldContainer3488384713005013CID4013321UID379-inputEl"))).send_keys("1902")

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "RibbonButtonExt393CID675504-btnEl"))).click()
    print("Input LEA stuff done.")

except Exception as e:
    print("Input LEA stuff failed. You probably lost 1 Life.")
    logout_quitdriver()

print("Done. ")
sleep()
