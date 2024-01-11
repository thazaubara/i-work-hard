import sys

from httpcore import TimeoutException
from selenium import webdriver
from selenium import webdriver
from selenium.common import UnexpectedAlertPresentException
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
    print("performing logout action.")
    # CLICK USER
    sleep()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "NavBtnCMDUser77-btnInnerEl"))).click()
    # CLICK LOGOOUT
    sleep()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "NavBar68ItemCMDLogout-itemEl"))).click()
    print("Logged out. Quitting Driver.")
    driver.quit()
    sys.exit(0)

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
except TimeoutException as e:
    print("You lose. Max Retries reached.")
    print(e.msg)
    print(e)
    logout_quitdriver()
except Exception as e:
    print("Login Button click failed. You lost 1 Life.")
    print(e)

# CLICK THE LEA BUTTON (Eng: SEB)
try:
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "TileButtonPKG584-btnWrap"))).click()
    print("Clicked LEA Button")
except Exception as e:
    print("LEA Button click failed. You probably lost 1 Life.")
    print(e)
    logout_quitdriver()

# CLICK THE DAILY SERVICE ENTRY BUTTON
try:
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "TileButtonCID30577-btnWrap"))).click()
    print("Clicked daily Button")
except Exception as e:
    print("Daily Button click failed. You probably lost 1 Life.")
    print(e)
    logout_quitdriver()

# CLICK THE NEW BUTTON

sleep()

try:
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "RibbonButtonExt214CID29597-btnEl"))).click()
    print("Clicked new Button")
except Exception as e:
    print("New Button click failed. You probably lost 1 Life.")
    print(e)
    logout_quitdriver()

# DISMISS THE POPUP IF THERE
# sometime there is a popup with text (Please note that the services from 1. January 2024 have not yet been completed!) after the "New" button is clicked
# check if it is there and close it, if not continue as usual
try:
    WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, "MsgBoxBtn0_2859462034720112_1-btnWrap"))).click()
    print("Found & clicked Infobox Button")
except Exception as e:
    print("No infobox found. Continue as usual.")

def input_lea_stuff(projekt_nr, tatigkeit_nr, time=None):
    sleep()
    # INPUT LEA STUFF
    try:
        # input project number
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "AttrFieldTextFieldContainer3488384713005001CID4018874UID189-inputEl"))).send_keys(projekt_nr)
        # AttrFieldTextFieldContainer3488384713005001CID4004645UID190
        # input customer number
        # filled automatically from bmd :D

        # input tätigkeit number
        txt_tatigkeit = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "AttrFieldTextFieldContainer3488384713005001CID4013321UID193-inputEl")))
        txt_tatigkeit.send_keys(tatigkeit_nr, Keys.TAB)

        if time is None:
            # click three buttons - lifehack
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "AttrFieldTimeFieldContainer3488384713005001CID4018896UID195-trigger-f8"))).click()
        else:
            txt_time = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "AttrFieldTimeFieldContainer3488384713005001CID4018896UID195-inputEl")))
            txt_time.send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, time)

        # click save button, give time to check if everything is ok
        sleep()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "button-1085-btnEl"))).click()
        sleep()

        if time is None:
            print(f"LEA entry [Restzeit] for Projekt {projekt_nr} and Tätigkeit {tatigkeit_nr} saved.")
        else:
            print(f"LEA entry [{time}] for Projekt {projekt_nr} and Tätigkeit {tatigkeit_nr} saved.")

    except Exception as e:
        print(e)

input_lea_stuff("2127099", "1902", "3:00")
input_lea_stuff("2130000", "1902")


sleep()

print("Done. ")
logout_quitdriver()
