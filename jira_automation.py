from collections import Counter
from typing import cast

from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue
from datetime import datetime, timedelta, timezone

import credentials as cred

verbose = False

def log(message):
    if verbose:
        now = datetime.now()
        date_now = now.strftime("%d.%m.%Y")
        time_now = now.strftime("%H:%M")
        print(f"I WORK HARD at {date_now} {time_now} -> {message}")

def printIssues(issues):
    for issue in issues:
        print(f"{issue.key} | {issue.fields.summary} [{issue.fields.customfield_10016} h]")
        try:
            print(f"    {issue.fields.project} -> {issue.fields.customfield_10020[0].name}")
        except:
            print(f"    {issue.fields.project} -> BACKLOG")
        print(f"    Status: {issue.fields.status}")

def issue_to_string(issue):
    if issue.fields.customfield_10016 is None:
        hours = 0
    else:
        hours = issue.fields.customfield_10016
    if issue.fields.resolution is None:
        resolution = "[ ]"
    else:
        resolution = "[✓]"
    return(f"{resolution} {issue.key} | {issue.fields.summary} [{hours} h]")

def list_my_issues():
    """
    This is the old tester-method. Pls do not use for poroductive.
    :return:
    """
    jira = JIRA(server="https://value-one.atlassian.net", basic_auth=(cred.JIRA_USER, cred.JIRA_TOKEN))

    displayname = jira.myself()["displayName"]
    mail = jira.myself()["emailAddress"]
    print(f"Logged in as {displayname} ({mail})")

    print("-"*80)  # ##################################################################
    boards = jira.boards()
    print(f"Boards: {len(boards)}")
    for board in boards:
        print(f"    {board.name} ({board.id})")
        try:
            sprints = jira.sprints(board.id)
            for sprint in sprints:
                print(f"        {sprint.name} ({sprint.id})")
        except:
            pass

    print("-"*80)  # ##################################################################
    active = jira.search_issues('assignee=currentUser() AND Sprint in openSprints() ORDER BY created ASC')
    print(f"ALL ACTIVE ISSUES [{len(active)}]")
    printIssues(active)

    print("-"*80)  # ##################################################################
    backlog = jira.search_issues('assignee=currentUser() AND Sprint is EMPTY AND issuetype!=Sub-Task ORDER BY created ASC')
    print(f"BACKLOG ohne Sub-Tasks [{len(backlog)}]")
    printIssues(backlog)

def is_done_this_week(string):
    """
    checks if given string is after monday this week.
    :param string:
    :return:
    """
    if string is None:
        return False

    now = datetime.now()
    # Calculate the difference in days to Monday (0 represents Monday)
    days_until_monday = (now.weekday() - 0) % 7
    # Adjust the current date to Monday at midnight
    monday_at_midnight = now - timedelta(days=days_until_monday, hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    monday_at_midnight = monday_at_midnight.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)

    # rint("Current Date and Time:", now)
    # print("Monday at Midnight:", monday_at_midnight)

    format_string = '%Y-%m-%dT%H:%M:%S.%f%z'
    datetime_object = datetime.strptime(string, format_string)

    if datetime_object > monday_at_midnight:
        # print(f"{string} is after {monday_at_midnight}")
        return True
    else:
        return False

def list_users():
    """
    dumb method. because I don't know how to query users yet.
    may take a looooooooong time if more issues are present.
    :return:
    """
    jira = JIRA(server="https://value-one.atlassian.net", basic_auth=(cred.JIRA_USER, cred.JIRA_TOKEN))
    all_stories = jira.search_issues('issuetype=Story')
    users = set()

    for story in all_stories:
        user = story.fields.assignee
        if user is not None:
            users.add(story.fields.assignee)

    print(f"\n{'─' * 50}\nFOUND {len(users)} USERS AMONG ALL ISSUES")
    for user in users:
        name = user.raw.get("displayName", "None")
        mail = user.raw.get("emailAddress", "None")
        print(f"  {name} ({mail})")

def get_project_hours(assignee, print_verbose=False):
    global verbose
    verbose = print_verbose
    jira = JIRA(server="https://value-one.atlassian.net", basic_auth=(cred.JIRA_USER, cred.JIRA_TOKEN))
    all_open_issues = jira.search_issues(f'assignee="{assignee}" AND Sprint in openSprints() ORDER BY created ASC')

    log(f"\n{'─' * 50}\nSPRINT SUMMARY for {assignee}")

    projects = set()
    for issue in all_open_issues:
        try:
            projects.add(issue.fields.project.name)
        except AttributeError:
            log(f"AttributeError (project name) for {issue.key}")
    log(f"Projects: {projects}")

    timeentries = {}

    for project in projects:
        finished_issues = []
        finished_hours = 0
        total_hours = 0
        log(f"  {project}")

        for issue in all_open_issues:

            if issue.fields.customfield_10016 is None:
                hours = 0
            else:
                hours = issue.fields.customfield_10016
            total_hours += hours
            if issue.fields.project.name == project and is_done_this_week(issue.fields.resolutiondate):
                finished_hours += hours
                finished_issues.append(issue)

        log(f"    {project} total:    {len(all_open_issues)} issues, {total_hours} h")
        for issue in all_open_issues:
            log(f"      {issue_to_string(issue)}")
        log(f"    {project} finished: {len(finished_issues)} issues, {finished_hours} h")
        for issue in finished_issues:
            log(f"      {issue_to_string(issue)}")
        timeentries[project] = finished_hours
    log(f"{'─' * 50}\n")
    return timeentries
