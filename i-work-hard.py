import bmd_credentials as credentials
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timezone, timedelta
import mysql.connector as mariadb
from mysql.connector import Error

BMD_USER = credentials.BMD_USER
BMD_PASS = credentials.BMD_PASS
BMD_URL = credentials.BASE_URL
HEADLESS = False

def STOPHERE(text=""):
    pressed = input(f"STOPPING HERE -> {text}")

def BREAKPOINT(text=""):
    print(f"Breakpoint: {text}")

def TOFILE(name, text):
    f = open(name, "a")
    f.write(text)
    f.close()

def SCREENSHOT(driver, name):
    driver.save_screenshot(name)

homeoffice = "homeoffice"
normalbuchung = "normalbuchung"
logout = "logout"
check_time = "check_time"

def do_bmd_stuff(action, headless=True):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    options.add_argument("--window-size=1300,800")

    if headless:
        options.add_argument("--start-maximized")
        options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    width = driver.get_window_size().get("width")
    height = driver.get_window_size().get("height")
    print(f"driver set to {width}x{height}")

    # GO TO SITE
    base_url = "https://finanz.value-one.com/bmdweb2"
    print(f"Loading {BMD_URL}")
    driver.get(BMD_URL)

    try:
        # FILL CREDENTIALS
        #txt_username = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "txtuser - inputEl")))
        txt_username = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "txtuser-inputEl")))
        txt_username.send_keys(BMD_USER)
        txt_password = driver.find_element(By.ID, "txtpass-inputEl")
        txt_password.send_keys(BMD_PASS)

        # CLICK THE LOGIN BUTTON
        loginbutton = driver.find_element(By.ID, "loginbutton-btnEl")
        loginbutton.click()

        # CLICK THE TIME BUTTON#
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "TileButtonPKG564-btnWrap"))).click()

        # CLICK THE POST TOUCH BUTTON
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "TileButtonCID31513-btnWrap"))).click()

        # GET WORKING TIME TODAY
        day_debit = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "AttrFieldTextFieldContainer7612734691278121CID4089024UID184-inputEl"))).get_attribute("value")
        day_so_far = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "AttrFieldTextFieldContainer7612734691278121CID4089025UID185-inputEl"))).get_attribute("value")

        day_debit_float = 0.0
        day_so_far_float = 0.0

        try:
            hours, minutes = map(int, day_debit.split(':'))
            day_debit_float = hours + minutes / 60.0
            hours, minutes = map(int, day_so_far.split(':'))
            day_so_far_float = hours + minutes / 60.0
        except:
            print("Error parsing time. Exiting.")
            sys.exit(1)

        if action == homeoffice:
            # CLICK POSTING TYPE
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ButtonFrameBtn162-btnEl"))).click()
            # CLICK "HOMEOFFICE"
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ButtonFrameBtn287-btnEl"))).click()
            # CLICK SAVE BUTTON
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ButtonFrameBtn179-btnEl"))).click()
            print("Homeoffice booked.")
        elif action == normalbuchung:
            # CLICK POSTING TYPE
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ButtonFrameBtn162-btnEl"))).click()
            # CLICK "NORMAL BOOKING"
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ButtonFrameBtn281-btnEl"))).click()
            # CLICK SAVE BUTTON
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ButtonFrameBtn179-btnEl"))).click()
            print("Normal booking booked.")
        elif action == logout:
            # CLICK GOING
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ButtonFrameBtn159-btnEl"))).click()
            # CLICK SAVE BUTTON
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ButtonFrameBtn179-btnEl"))).click()
            print("Logged out.")
        elif action == check_time:
            print(f"Just checked Time.")
            pass
        else:
            print("Unknown action. Returning.")

        # TODO Logout. bc -> The max. number of 5 zulässigen Datenbankverbindungen pro Benutzer wurde überschritten!
        driver.quit()
        return day_debit_float, day_so_far_float

    except Exception as e:
        print("Error in Script. Exiting.")
        print(e)
        sys.exit(1)

day_debit, day_sofar = do_bmd_stuff(homeoffice, headless=False)
print(f"Day debit: {day_debit}, day so far: {day_sofar}")

