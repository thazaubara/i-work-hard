import bmd_credentials as credentials
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timezone
import mysql.connector as mariadb
from mysql.connector import Error

BMD_USER = credentials.BMD_USER
BMD_PASS = credentials.BMD_PASS
BMD_URL = credentials.BASE_URL
HEADLESS = False

def STOPHERE():
    seconds = 120
    print(f"STOPPING HERE FOR {seconds} seconds")
    time.sleep(seconds)

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
options.add_argument("--window-size=1300,800")

if HEADLESS:
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

    STOPHERE()

    """
    # FILL CREDENTIALS
    txt_username = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#txtuser-inputEl")))
    txt_username.send_keys(BMD_USER)
    txt_password = driver.find_element(By.CSS_SELECTOR, "#txtpass-inputEl")
    txt_password.send_keys(BMD_PASS)

    loginbutton = driver.find_element(By.CSS_SELECTOR, "#loginbutton-btnInnerEl")
    loginbutton.click()

    # TIME BUTTON
    time_menu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#TileButtonPKG564-btnWrap")))
    time_menu.click()

    # POST TOUCH BUTTON
    touch_menu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#TileButtonCID31513-btnWrap")))
    touch_menu.click()

    STOPHERE()

    # COMING BUTTON
    coming_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#ButtonFrameBtn158-btnIconEl")))
    touch_menu.click()
    """


except Exception as e:
    driver.quit()
    print(e)
    print("Unexpected error:", sys.exc_info()[0])


# Message: unexpected alert open: {Alert text : The max. number of 5 zulässigen Datenbankverbindungen pro Benutzer wurde überschritten!} (Session info: chrome=115.0.5790.114)

