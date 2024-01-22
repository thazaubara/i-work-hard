from collections import Counter
from typing import cast

from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue

import credentials as cred

def printIssues(issues):
    for issue in issues:
        print(f"{issue.key} | {issue.fields.summary} [{issue.fields.customfield_10016} h]")
        try:
            print(f"    {issue.fields.project} -> {issue.fields.customfield_10020[0].name}")
        except:
            print(f"    {issue.fields.project} -> BACKLOG")
        print(f"    Status: {issue.fields.status}")


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

if False:
    print("-"*80)  # ##################################################################

    all_issues = jira.search_issues('assignee=currentUser()')
    print(f"ALL ISSUES [{len(all_issues)}]")
    printIssues(all_issues)

print("-"*80)  # ##################################################################

active = jira.search_issues('assignee=currentUser() AND Sprint in openSprints()')
print(f"ALL ACTIVE ISSUES [{len(active)}]")
printIssues(active)

print("-"*80)  # ##################################################################

backlog = jira.search_issues('assignee=currentUser() AND Sprint is EMPTY AND issuetype!=Sub-Task')
print(f"BACKLOG ohne Sub-Tasks [{len(backlog)}]")
printIssues(backlog)



pass


