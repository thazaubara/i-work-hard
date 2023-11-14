import json
import os

import bmd_credentials as credentials
import sys


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, time, timedelta

BMD_USER = credentials.BMD_USER
BMD_PASS = credentials.BMD_PASS
BMD_URL = credentials.BASE_URL

action_homeoffice = "homeoffice"
action_normalbuchung = "normalbuchung"
action_logout = "logout"
action_check_time = "check_time"

now = datetime.now()
date_now = now.strftime("%d.%m.%Y")
time_now = now.strftime("%H:%M")
day_now = now.strftime("%A")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
        print("Login Successful.")

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
        elif action == action_normalbuchung:
            # CLICK POSTING TYPE
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ButtonFrameBtn162-btnEl"))).click()
            # CLICK "NORMAL BOOKING"
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ButtonFrameBtn281-btnEl"))).click()
            # CLICK SAVE BUTTON
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ButtonFrameBtn179-btnEl"))).click()
            print("Normal booking booked.")
        elif action == action_logout:
            # CLICK GOING
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ButtonFrameBtn159-btnEl"))).click()
            # CLICK SAVE BUTTON
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ButtonFrameBtn179-btnEl"))).click()
            print("Logged out.")
        elif action == action_check_time:
            print(f"Just checked Time.")
            pass
        else:
            print("Unknown action. Returning.")

        # TODO Logout. bc -> The max. number of 5 zulässigen Datenbankverbindungen pro Benutzer wurde überschritten!
        # CLICK USER
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "NavBtnCMDUser77-btnInnerEl"))).click()
        # CLICK LOGOOUT
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "NavBar68ItemCMDLogout-itemEl"))).click()
        print("Logged out. Quitting Driver.")
        driver.quit()
        return day_debit_float, day_so_far_float

    except Exception as e:
        print("Error in Script. Exiting.")
        print(e)
        sys.exit(1)

def weekend():
    return now.weekday() in [5, 6]  # is saturday or sunday

def core_time():
    current_time = now.time()
    start_time = time(9, 0)
    end_time = time(20, 0)
    return start_time <= current_time <= end_time

def creeate_file_if_not_exists():
    print(f"logs.txt did not exist. I created one for you at {os.getcwd()}")
    if not os.path.exists("logs.txt"):
        with open("logs.txt", "w") as file:
            json.dump([], file)

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
    return now.weekday() in [1, 2, 4]  # is monday or thursday

def main():
    creeate_file_if_not_exists()
    print(f"I WORK HARD at {date_now} {time_now} -> ", end="")


    if weekend():
        print('Weekend!')
        return
    if not core_time():
        print('Not core time!')
        return
    if first_entry_today():
        if homeoffice():
            action = action_homeoffice
        else:
            action = action_normalbuchung
        # TODO: do_bmd_stuff() with action.
        # TODO: also quit booking if day_debit is 0.0, but still return day_debit and day_so_far

        day_debit = 8.0
        day_sofar = 0.0

        result_time = now + timedelta(hours=day_debit)
        day_ends = result_time.strftime('%H:%M')

        print(f"Starting {action} at {time_now}, ending at {day_ends}")
        if day_debit == 0.0:
            new_entry = {"date": date_now, "day": day_now, "action": "cancel booking", "start": time_now, "end": day_ends, "finished": "yes"}
        else:
            new_entry = {"date": date_now, "day": day_now, "action": action, "start": time_now, "end": day_ends, "finished": "no"}
        file_append_entry(new_entry)

    elif not first_entry_today():
        # print("not first entry today")
        last_entry = file_get_last_entry()
        if last_entry["finished"] == "yes":
            print("Day is finished. Nothing to do.")
            return

        string_time = last_entry['end']
        parsed_time = datetime.strptime(string_time, "%H:%M").time()
        end_datetime = datetime.combine(now.date(), parsed_time)

        if now < end_datetime:
            time_difference = end_datetime - now
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes = remainder // 60
            time_left_string = f"{hours:02}:{minutes:02}"
            print(f"Do more work. Can go home in {time_left_string}")
        else:
            print(f"Feierabend!")
            # TODO: do_bmd_stuff() with action_logout
            last_entry["finished"] = "yes"
            last_entry["logout_time"] = time_now
            file_update_last_entry(last_entry)

if __name__ == '__main__':
    main()
