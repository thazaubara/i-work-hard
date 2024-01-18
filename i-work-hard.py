import argparse
import json
import os

import bmd_credentials as credentials
import bmd_automation as bmd

import sys
import time as t

import lea as lea

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, time, timedelta

BMD_USER = credentials.BMD_USER
BMD_PASS = credentials.BMD_PASS
BMD_URL = credentials.BASE_URL


HOMEOFFICE_DAYS = credentials.HOMEOFFICE_DAYS
MY_NAME = credentials.BMD_MY_NAME

action_homeoffice = "homeoffice"
action_normalbuchung = "normalbuchung"
action_going = "logout"
action_check_time = "check_time"

now = datetime.now()
date_now = now.strftime("%d.%m.%Y")
time_now = now.strftime("%H:%M")
day_now = now.strftime("%A")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# just init values, get overridden by argparse.
verbose = False
headless = False



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



def do_bmd_stuff(action, headless):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    options.add_argument("--window-size=1300,800")

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

    # FILL CREDENTIALS
    find_fill_input(driver, "User name", BMD_USER)
    find_fill_input(driver, "Password", BMD_PASS)

    # NAVIGATE TO POST TOUCH
    find_click_button(driver, "Login")
    find_click_button(driver, "Time")
    find_click_button(driver, "Post Touch")

    # GET WORKING TIME TODAY
    sleep()
    day_debit = read_from_info_table(driver, "Day debit")
    # day_debit = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "AttrFieldTextFieldContainer7612734691278121CID4089024UID184-inputEl"))).get_attribute("value")
    # day_so_far = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "AttrFieldTextFieldContainer7612734691278121CID4089025UID185-inputEl"))).get_attribute("value")
    day_so_far = read_from_info_table(driver, "Day so far")
    balance = read_from_info_table(driver, "Balance")


    try:
        hours, minutes = map(int, day_debit.split(':'))
        day_debit_float = hours + minutes / 60.0
        hours, minutes = map(int, day_so_far.split(':'))
        day_so_far_float = hours + minutes / 60.0
    except Exception as e:
        log("Error parsing time. Exiting.")
        sys.exit(1)

    # ACTION DEPENDENT BUTTON CLICKS
    if action == action_homeoffice:
        find_click_button(driver, "Posting type")
        find_click_button(driver, "HOMEOFFICE")
        find_click_button(driver, "Save")
    elif action == action_normalbuchung:
        find_click_button(driver, "Posting type")
        find_click_button(driver, "Normal Booking")
        find_click_button(driver, "Save")
    elif action == action_going:
        find_click_button(driver, "Going")
        find_click_button(driver, "Save")
    elif action == action_check_time:
        log(f"Just checked Time.")
        pass
    else:
        log("Unknown action. Returning.")

    # SIGN OFF
    find_click_button(driver, MY_NAME)
    find_click_button(driver, "Sign off")

    driver.quit()
    return day_debit_float, day_so_far_float

def weekend():
    return now.weekday() in [5, 6]  # is saturday or sunday

def core_time():
    current_time = now.time()
    start_time = time(9, 0)
    end_time = time(20, 0)
    return start_time <= current_time <= end_time

def create_file_if_not_exists():
    if not os.path.exists("logs.txt"):
        with open("logs.txt", "w") as file:
            json.dump([], file)
        log(f"logs.txt did not exist. I created one for you at {os.getcwd()}")
    else:
        if verbose:
            log(f"logs.txt found in {os.getcwd()}")

def file_get_last_entry():
    content = []
    with open("logs.txt", mode='r') as file:
        content = json.load(file)
    if len(content) == 0:
        return None
    return content[-1]

def file_append_entry(entry):
    content = []
    with open("logs.txt", mode='r') as file:
        content = json.load(file)

    with open("logs.txt", "w") as file:
        content.append(entry)
        json.dump(content, file, indent=4)

def file_update_last_entry(entry):
    content = []
    with open("logs.txt", mode='r') as file:
        content = json.load(file)

    with open("logs.txt", "w") as file:
        content[-1] = entry
        json.dump(content, file, indent=4)

def first_entry_today():
    last_entry = file_get_last_entry()

    if last_entry is None:
        return True

    if last_entry["date"] != date_now:
        return True
    else:
        return False

def homeoffice():
    return now.weekday() in HOMEOFFICE_DAYS

def log(message):
    if verbose:
        print(f"I WORK HARD at {date_now} {time_now} -> {message}")

def main():
    global verbose, headless
    parser = argparse.ArgumentParser(description='BMD Buchung')
    parser.add_argument('-v', action='store_true', help='verbose output. print everything.')
    parser.add_argument('-w', action='store_true', default=False, help='run in windowed mode. no headless browser.')
    args = parser.parse_args()
    verbose = args.v
    headless = not args.w

    create_file_if_not_exists()

    if weekend():
        if verbose:
            log('Weekend!')
        return
    if not core_time():
        if verbose:
            log('Not core time!')
        return
    if first_entry_today():
        if homeoffice():
            action = action_homeoffice
        else:
            action = action_normalbuchung
        day_debit, day_so_far = do_bmd_stuff(action, headless=headless)

        result_time = now + timedelta(hours=day_debit)
        day_ends = result_time.strftime('%H:%M')

        log(f"Started {action} at {time_now}, ending at {day_ends}")
        if day_debit == 0.0:
            new_entry = {"date": date_now, "day": day_now, "action": "cancel booking", "start": time_now, "end": day_ends, "finished": "yes"}
        else:
            new_entry = {"date": date_now, "day": day_now, "action": action, "start": time_now, "end": day_ends, "finished": "no"}
        file_append_entry(new_entry)

    elif not first_entry_today():
        # print("not first entry today")
        last_entry = file_get_last_entry()
        if last_entry["finished"] == "yes":
            if verbose:
                log("Day is finished. Nothing to do.")
            return

        string_time = last_entry['end']
        parsed_time = datetime.strptime(string_time, "%H:%M").time()
        end_datetime = datetime.combine(now.date(), parsed_time)

        if now < end_datetime:
            time_difference = end_datetime - now
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes = remainder // 60
            time_left_string = f"{hours:02}:{minutes:02}"
            if verbose:
                log(f"Do more work. Can go home in {time_left_string}")
        else:
            log(f"Feierabend!")
            do_bmd_stuff(action_going, headless=headless)
            last_entry["finished"] = "yes"
            last_entry["logout_time"] = time_now
            file_update_last_entry(last_entry)

            log(f"Starting LEA")
            lea.perform_lea()


if __name__ == '__main__':
    # main()
    # bmd.verbose = True
    # bmd.headless = False
    bmd.start_bmd(url=credentials.BASE_URL, user=credentials.BMD_USER, password=credentials.BMD_PASS)
    bmd.perform_single_day_lea()
    # bmd.book_normalbuchung()
    bmd.sign_off()
    pass
