
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.keys import Keys

import bmd_credentials as credentials
import sys
import time as t

BMD_USER = credentials.BMD_USER
BMD_PASS = credentials.BMD_PASS
BMD_URL = credentials.BASE_URL

MY_NAME = credentials.BMD_MY_NAME

now = datetime.now()
date_now = now.strftime("%d.%m.%Y")
time_now = now.strftime("%H:%M")
day_now = now.strftime("%A")

verbose = True
headless = True

def sleep(time=1):
    t.sleep(time)

def log(message):
    if verbose:
        print(f"I WORK HARD at {date_now} {time_now} -> {message}")


def init(verbose=True, headless=False):
    print(f"Using Python Version: {sys.version}")
    print("Selenium Version: " + webdriver.__version__)

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    options.add_argument("--window-size=1300,1000")

    if headless:
        options.add_argument("--start-maximized")
        options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    width = driver.get_window_size().get("width")
    height = driver.get_window_size().get("height")
    log(f"driver set to {width}x{height}")

    # GO TO SITE
    log(f"Loading {BMD_URL}")
    driver.get(BMD_URL)
    return driver


def find_click_button(driver, button_text):
    """
    this only works on span elements
    tires to find a span element with given text and attempts to click it
    it it fails, it tries to signn off
    remember: you only have 5 login requets per timeframe
    """

    sleep()  # because BMD is f*cking slow

    try:
        # (By.XPATH, "//input[@placeholder='User Name']")
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(),'{button_text}')]")))
        element.click()
        log(f"Clicked element with text '{button_text}'")
        return
    except Exception as e:
        log(f"Could not find element with text '{button_text}'")

    try:
        log("TRYING EMERGENCY EXIT to not lose a login request")
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(),'{MY_NAME}')]")))
        element.click()
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(),'Sign off')]")))
        element.click()
        log("Emergency exit (Sign off) successful.")
    except Exception as e:
        log("Emergency exit (Sign off) failed. You probably lost 1 login request")

def find_fill_input(driver, placeholder_text, text_to_fill):
    """
    this only works on input elements
    tires to find a input element with given placeholder text and attempts to fill it with text_to_fill
    it it fails, it tries to signn off
    remember: you only have 5 login requets per timeframe
    :param driver:
    :param placeholder_text:
    :param text_to_fill:
    :return:
    """

    sleep()  # because BMD is f*cking slow
    try:
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//input[@placeholder='{placeholder_text}']")))
        element.send_keys(text_to_fill)
        log(f"Filled input with placeholder '{placeholder_text}'")  # do not print password, only log that is has been filled.
        return
    except Exception as e:
        log(f"Could not find input with placeholder '{placeholder_text}'")

    try:
        log("TRYING EMERGENCY EXIT to not lose a login request")
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(),'{MY_NAME}')]")))
        element.click()
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(),'Sign off')]")))
        element.click()
        log("Emergency exit (Sign off) successful.")
    except Exception as e:
        log("Emergency exit (Sign off) failed. You probably lost 1 login request")

def find_dismiss_popup(driver):
    try:
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(@id, 'MsgBoxBtn') and text()='OK']"))).click()
        log("Found & clicked Infobox Button")
    except Exception as e:
        log("No infobox found. Continue as usual.")

def logout_quitdriver(driver):
    print("performing logout action.")
    # CLICK USER
    sleep()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "NavBtnCMDUser77-btnInnerEl"))).click()
    # CLICK LOGOOUT
    sleep()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "NavBar68ItemCMDLogout-itemEl"))).click()
    print("Logged out. Quitting Driver.")
    driver.quit()
    sleep()
    sys.exit(0)

def input_lea_stuff(driver, projekt_nr, tatigkeit_nr, time=None):
    sleep(3)
    # CLICK THE NEW BUTTON
    find_click_button(driver, "New")

    # DISMISS THE POPUP IF THERE
    # sometime there is a popup with text (Please note that the services from 1. January 2024 have not yet been completed!) after the "New" button is clicked
    # check if it is there and close it, if not continue as usual
    find_dismiss_popup(driver)

    sleep()
    # display STATS
    overall = driver.find_element(By.XPATH, f"//label[contains(text(), 'Overall')]//../label[2]").text
    remaining = driver.find_element(By.XPATH, f"//label[contains(text(), 'Overall')]//../label[4]").text
    log(f"Overall: {overall}, Remaining: {remaining}")

    def convert_time_to_decimal(time_str):
        hours, minutes = map(int, time_str.split(":"))
        decimal_time = hours + minutes / 60.0
        return decimal_time

    # INPUT LEA STUFF
    try:
        # input project number
        sleep()
        txt_project_number = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, f"//input[contains(@name, 'MCA_LEI_ORG_PROJEKTNR')]")))
        txt_project_number.send_keys(projekt_nr + Keys.ENTER)

        # input tätigkeit number
        sleep()
        txt_tatigkeit = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//input[contains(@name, 'MCA_LEI_ARL_ARTIKELNR')]")))
        txt_tatigkeit.send_keys(tatigkeit_nr, Keys.TAB, Keys.TAB)  # tab so that time field is in view and rendered

        # input time
        sleep()
        if time is None:
            # click three buttons - lifehack
            three_points = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//input[contains(@name, 'MCU_LEI_STUNDEN_EINGABE')]//../../div[contains(@class, 'pictos')]")))
            three_points.click()
            log("Clicked three points button")
        else:
            if convert_time_to_decimal(time) > convert_time_to_decimal(remaining):
                log(f"ERROR: You tried to input more time than remaining. {time} > {remaining}")
                sleep()
                find_click_button(driver, "Cancel")
                sleep(3)
                return
            txt_time = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//input[contains(@name, 'MCU_LEI_STUNDEN_EINGABE')]")))
            txt_time.send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, time)

        # click save button, give time to check if everything is ok
        sleep()
        find_click_button(driver, "Save")
        sleep()

        if time is None:
            print(f"LEA entry [Restzeit] for Projekt {projekt_nr} and Tätigkeit {tatigkeit_nr} saved.")
        else:
            print(f"LEA entry [{time}] for Projekt {projekt_nr} and Tätigkeit {tatigkeit_nr} saved.")

    except Exception as e:
        print(e)

def perform_lea(verbose=True, headless=False):
    driver = init(verbose, headless)
    # FILL CREDENTIALS
    find_fill_input(driver, "User name", BMD_USER)
    find_fill_input(driver, "Password", BMD_PASS)
    find_click_button(driver, "Login")

    # CLICK THE LEA BUTTON (Eng: SEB)
    find_click_button(driver, "SEB")
    find_click_button(driver, "Daily service entry")

    input_lea_stuff(driver, "2127099", "1902", "3:00")
    input_lea_stuff(driver, "2130000", "1902")

    sleep()

    print("Done. ")
    logout_quitdriver(driver)

if __name__ == "__main__":
    verbose = True
    headless = False
    perform_lea()
