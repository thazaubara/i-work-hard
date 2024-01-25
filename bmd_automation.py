import sys
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# global vars
verbose = True
headless = False
driver = webdriver.Chrome  # gets set in init. do not change here. This is only here for type definition.
base_url = None  # gets set in init. do not change here

"""
   __ ________   ___  _______  ____
  / // / __/ /  / _ \/ __/ _ \/ __/
 / _  / _// /__/ ___/ _// , _/\ \  
/_//_/___/____/_/  /___/_/|_/___/  
Stuff that has nothing to do with selenium per se.
"""

def log(message):
    if verbose:
        now = datetime.now()
        date_now = now.strftime("%d.%m.%Y")
        time_now = now.strftime("%H:%M")
        print(f"I WORK HARD at {date_now} {time_now} -> {message}")

def sleep(seconds=1):
    time.sleep(seconds)


"""
   ___  ___________________  _  ______
  / _ |/ ___/_  __/  _/ __ \/ |/ / __/
 / __ / /__  / / _/ // /_/ /    /\ \  
/_/ |_\___/ /_/ /___/\____/_/|_/___/  
Stuff that abstracts selenium stuff like:
- driver init
- find and fill input
- find and click button
- read a specific table format
- close a secific popup
"""

def init_driver():
    global verbose, headless, driver

    sys_version = sys.version.split('\n')[0]
    log(f"Using Python Version: {sys_version}")
    log("Selenium Version: " + webdriver.__version__)

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    options.add_argument("--window-size=1300,1000")

    if headless:
        options.add_argument("--start-maximized")
        options.add_argument("--headless")

    log(f"Loading Chrome Driver. Headless={headless}, Verbose={verbose}")
    driver = webdriver.Chrome(options=options)
    width = driver.get_window_size().get("width")
    height = driver.get_window_size().get("height")
    log(f"Driver set to {width}x{height}")

def find_fill_input(placeholder_text, text_to_fill):
    """
    this only works on input elements
    tires to find a input element with given placeholder text and attempts to fill it with text_to_fill
    it it fails, it tries to signn off
    remember: you only have 5 login requets per timeframe
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
        emergency_signoff()

def find_click_button(button_text, emergency=True):
    """
    this only works on span elements
    tires to find a span element with given text and attempts to click it
    it it fails, it tries to signn off
    remember: you only have 5 login requets per timeframe
    """
    sleep()  # because BMD is f*cking slow
    try:
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(),'{button_text}')]")))
        element.click()
        log(f"Clicked element with text '{button_text}'")
        return
    except Exception as e:
        log(f"Could not find element with text '{button_text}'")
        if emergency:
            emergency_signoff()

def read_from_info_table(label_text):
    """
    Very specific function. reads the info table on the bootom of the page containing Day debit, week debit, etc ...
    This is a very dumb html layout from BMD, which results in a very dumb xpath query.
    finds the element with the given text. from there, go to the third parent (the div), and then down to find the input field. you can then get the value from there.

    for debugging:
    element = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(),'Month debit')]/../../..//input"))).get_attribute("value").strip()

    :param driver:
    :return:
    """
    try:
        element = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(),'{label_text}')]/../../..//input")))
        value = element.get_attribute("value").strip()
        log(f"Label {label_text}: {value}")  # do not print password, only log that is has been filled.
        return value
    except Exception as e:
        log(f"Could not find values for label '{label_text}'")
        emergency_signoff()

def navigate_to_url(url):
    log(f"Loading {url}")
    driver.get(url)

def navigate_to_home():
    global driver
    """
    Goes to the home page of BMD
    """
    sleep()  # because BMD is f*cking slow
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//a[@id='NavBarBtnMain']"))).click()
        log(f"Home Sweet Home.")
        return
    except Exception as e:
        log(f"Click Home Failed. But why?.")
        sleep(10)

    driver.quit()
    log("Quitting driver")

def emergency_signoff():
    log("EMERGENCY SIGNOFF")
    sleep(60)
    sign_off()

def find_dismiss_popup():
    try:
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(@id, 'MsgBoxBtn') and text()='OK']"))).click()
        log("Found & clicked Infobox Button")
    except Exception as e:
        log("No infobox found. Continue as usual.")


def input_lea_stuff(projekt_nr, tatigkeit_nr, time=None):
    sleep(3)
    # CLICK THE NEW BUTTON
    # if done a second time, new btn is greyed out and line is already there to fill, so no emergency.
    find_click_button("New", emergency=False)

    # DISMISS THE POPUP IF THERE
    # sometime there is a popup with text (Please note that the services from 1. January 2024 have not yet been completed!) after the "New" button is clicked
    # check if it is there and close it, if not continue as usual
    find_dismiss_popup()

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
                find_click_button("Cancel")
                sleep(3)
                return
            txt_time = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//input[contains(@name, 'MCU_LEI_STUNDEN_EINGABE')]")))
            txt_time.send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, time)

        # click save button, give time to check if everything is ok
        sleep()
        find_click_button("Save")
        sleep()

        if time is None:
            log(f"LEA entry [Restzeit] for Projekt {projekt_nr} and Tätigkeit {tatigkeit_nr} saved.")
        else:
            log(f"LEA entry [{time}] for Projekt {projekt_nr} and Tätigkeit {tatigkeit_nr} saved.")

    except Exception as e:
        log(e)

"""
   __ _____________ __  __   _____   ________ 
  / // /  _/ ___/ // / / /  / __/ | / / __/ / 
 / _  // // (_ / _  / / /__/ _/ | |/ / _// /__
/_//_/___/\___/_//_/ /____/___/ |___/___/____/
Stuff that uses action to perfom specific tasks.
These are built from the basic functions above.
Prefereably use this in your main code.
These are things like:
    - perform LEA entry
    - book homeoffice
    - start bmd
"""

def start_bmd(url, user, password):
    """
    Starts the BMD site and login process
    """
    global base_url
    init_driver()
    base_url = url
    navigate_to_url(base_url)
    find_fill_input("User name", user)
    find_fill_input("Password", password)
    find_click_button("Login")

def book_homeoffice():
    global driver
    """
    Books homeoffice
    """
    navigate_to_home()
    find_click_button("Time")
    find_click_button("Post Touch")
    sleep()
    day_debit = read_from_info_table("Day debit")
    day_so_far = read_from_info_table("Day so far")
    balance = read_from_info_table("Balance")

    try:
        hours, minutes = map(int, day_debit.split(':'))
        day_debit_float = hours + minutes / 60.0
        hours, minutes = map(int, day_so_far.split(':'))
        day_so_far_float = hours + minutes / 60.0
    except Exception as e:
        log("Error parsing time. Exiting.")
        emergency_signoff()

    find_click_button("Posting type")
    find_click_button("HOMEOFFICE")
    find_click_button("Save")

    return day_debit_float, day_so_far_float

def book_normalbuchung():
    global driver
    """
    Books homeoffice
    """
    navigate_to_home()
    find_click_button("Time")
    find_click_button("Post Touch")
    sleep()
    day_debit = read_from_info_table("Day debit")
    day_so_far = read_from_info_table("Day so far")
    balance = read_from_info_table("Balance")

    try:
        hours, minutes = map(int, day_debit.split(':'))
        day_debit_float = hours + minutes / 60.0
        hours, minutes = map(int, day_so_far.split(':'))
        day_so_far_float = hours + minutes / 60.0
    except Exception as e:
        log("Error parsing time. Exiting.")
        emergency_signoff()

    find_click_button("Posting type")
    find_click_button("Normal Booking")
    find_click_button("Save")

    return day_debit_float, day_so_far_float

def book_going():
    global driver
    """
    Books homeoffice
    """
    navigate_to_home()
    find_click_button("Time")
    find_click_button("Post Touch")
    sleep()
    day_debit = read_from_info_table("Day debit")
    day_so_far = read_from_info_table("Day so far")
    balance = read_from_info_table("Balance")

    try:
        hours, minutes = map(int, day_debit.split(':'))
        day_debit_float = hours + minutes / 60.0
        hours, minutes = map(int, day_so_far.split(':'))
        day_so_far_float = hours + minutes / 60.0
    except Exception as e:
        log("Error parsing time. Exiting.")
        emergency_signoff()

    find_click_button("Going")
    find_click_button("Save")

    return day_debit_float, day_so_far_float

def perform_daily_lea():
    navigate_to_home()
    find_click_button("SEB")
    find_click_button("Daily service entry")
    input_lea_stuff("2127099", "1902", "3:00")
    input_lea_stuff("2130000", "1902")

def sign_off():
    global driver
    """
    Signs off from BMD
    """
    sleep()  # because BMD is f*cking slow
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//a[@title='Current user']"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(text(),'Sign off')]"))).click()
        log(f"Signed off.")
        return
    except Exception as e:
        log(f"Sign off failed. Do something.")
        sleep(10)

    driver.quit()
    log("Quitting driver")

def perform_weekly_lea(projects):
    log(f"Performing weekly LEA with: {projects}")
    #navigate_to_home()
    #find_click_button("SEB")
    #find_click_button("Weekly service entry")

def convert_to_lea_projects(projects):
    """
    Converts the time to LEA format.
    """

    print(projects)

    lea_projects = []

    # projekt, tätigkeit, time
    for project in projects:
        print(project)
        print(projects[project])
        #lea_projects.append({"project": projects[project], "activity": project["activity"], "time": project["time"]})
