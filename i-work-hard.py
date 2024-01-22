import argparse
import json
import os

import credentials as cred
import bmd_automation as bmd
from datetime import datetime, time, timedelta

BMD_USER = cred.BMD_USER
BMD_PASS = cred.BMD_PASS
BMD_URL = cred.BASE_URL

HOMEOFFICE_DAYS = cred.HOMEOFFICE_DAYS
MY_NAME = cred.BMD_MY_NAME

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

def weekend():
    return now.weekday() in [5, 6]  # is saturday or sunday

def core_time():
    current_time = now.time()
    start_time = time(9, 0)
    end_time = time(20, 0)
    return start_time <= current_time <= end_time

def create_file_if_not_exists():
    """
    Creates a logs.txt file if it does not exist
    :return: True if file was created, False if file already existed
    """
    if not os.path.exists("logs.txt"):
        with open("logs.txt", "w") as file:
            json.dump([], file)
        log(f"Created empty logs.txt at {os.getcwd()}")
        return True
    else:
        return False

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
    """
    This is the logic behind time booking. Timed stuff.
    :return:
    """
    global verbose, headless
    parser = argparse.ArgumentParser(description='BMD Buchung')
    parser.add_argument('-v', action='store_true', help='verbose output. print everything.')
    parser.add_argument('-w', action='store_true', default=False, help='run in windowed mode. no headless browser.')
    args = parser.parse_args()
    verbose = args.v
    headless = not args.w

    create_file_if_not_exists()

    if weekend():
        # log('Weekend!')
        return
    if not core_time():
        # log('Not core time!')
        return

    if first_entry_today():
        # First login today. Start time booking
        bmd.start_bmd(url=cred.BASE_URL, user=cred.BMD_USER, password=cred.BMD_PASS)
        if homeoffice():
            action = "homeoffice"
            log(f"Starting {action}")
            day_debit, day_so_far = bmd.book_homeoffice()
            result_time = now + timedelta(hours=day_debit)
            day_ends = result_time.strftime('%H:%M')
            log(f"Started {action} at {time_now}, ending at {day_ends}")
        else:
            action = "normalbuchung"
            log(f"Starting {action}")
            day_debit, day_so_far = bmd.book_normalbuchung()
            result_time = now + timedelta(hours=day_debit)
            day_ends = result_time.strftime('%H:%M')
            log(f"Started {action} at {time_now}, ending at {day_ends}")
            bmd.sign_off()

        # Write status to file
        if day_debit == 0.0:
            new_entry = {"date": date_now, "day": day_now, "action": "cancel booking", "start": time_now, "end": day_ends, "finished": "yes"}
        else:
            new_entry = {"date": date_now, "day": day_now, "action": action, "start": time_now, "end": day_ends, "finished": "no"}
        file_append_entry(new_entry)

    else:
        last_entry = file_get_last_entry()
        if last_entry["finished"] == "yes":
            # log("Day is finished. Nothing to do.")
            return

        string_time = last_entry['end']
        parsed_time = datetime.strptime(string_time, "%H:%M").time()
        end_datetime = datetime.combine(now.date(), parsed_time)

        if now < end_datetime:
            time_difference = end_datetime - now
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes = remainder // 60
            # log(f"Do more work. Can go home in {hours:02}:{minutes:02}")
        else:
            log(f"Feierabend!")
            bmd.start_bmd(url=cred.BASE_URL, user=cred.BMD_USER, password=cred.BMD_PASS)
            bmd.book_going()
            last_entry["finished"] = "yes"
            last_entry["logout_time"] = time_now
            file_update_last_entry(last_entry)

            log(f"Starting LEA")
            bmd.perform_daily_lea()


if __name__ == '__main__':
    main()

    """
    bmd.start_bmd(url=credentials.BASE_URL, user=credentials.BMD_USER, password=credentials.BMD_PASS)
    # bmd.perform_daily_lea()
    # bmd.book_normalbuchung()
    my_projects = [{"projekt": "2130000", "tatigkeit": "1902", "stunden": "8"},  # remory
                   {"projekt": "2127099", "tatigkeit": "1902", "stunden": "16"},  # reworkx
                   {"projekt": "2127099", "tatigkeit": "1902"}]  # value one digital GmbH(Arbeitgeber) -> restliche stunden
    bmd.perform_weekly_lea(my_projects)
    bmd.sign_off()
    pass
    """
