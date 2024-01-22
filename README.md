# I WORK HARD
Automation of time booking ... because that sucks.

# Preparation
Download chromedriver for platform.
https://googlechromelabs.github.io/chrome-for-testing/#stable

I use mac, I put the binary in `/usr/local/bin`

Let the OS verify the binary. May be skipped with other OS.

`xattr -d com.apple.quarantine chromedriver`

## Links
Install chromedriver
https://www.geeksforgeeks.org/how-to-install-selenium-webdriver-on-macos/

## Problems
everywhere. 😜 

# Time Booking

This tool should book time depending on day. 

Because I am an honest worker, i start my day at 9:00 and end it at 17:00. 

Monday and Friday are office days, this should also be taken into account.

The script writes a file, to keep track of its actions. There is no need to launch the whole selenium process over and over again. Just when it is time to actually do something (book time or log out.). There is no loop. I still need to check it every x minutes.

Therefore it runs in crontab every 5 minutes.

![image-20231114160809927](./_images/image-20231114160809927.png)

## Logs

Contents of `log.txt`

```
user@ubuntu-server:~/scripts/i-work-hard$ cat logs.txt 
[
    {
        "date": "14.11.2023",
        "day": "Tuesday",
        "action": "homeoffice",
        "start": "09:00",
        "end": "16:58",
        "finished": "yes",
        "logout_time": "17:00"
    }
]
```

Just run the script in crontab and let it do the hard work of using BMD.

```
user@ubuntu-server:~/scripts/i-work-hard$ tail -f /var/log/syslog | grep 'WORK'
I WORK HARD at 14.11.2023 16:20 -> Do more work. Can go home in 00:37
I WORK HARD at 14.11.2023 16:25 -> Do more work. Can go home in 00:32
I WORK HARD at 14.11.2023 16:30 -> Do more work. Can go home in 00:27
I WORK HARD at 14.11.2023 16:35 -> Do more work. Can go home in 00:22
I WORK HARD at 14.11.2023 16:40 -> Do more work. Can go home in 00:17
I WORK HARD at 14.11.2023 16:45 -> Do more work. Can go home in 00:12
I WORK HARD at 14.11.2023 16:50 -> Do more work. Can go home in 00:07
I WORK HARD at 14.11.2023 16:55 -> Do more work. Can go home in 00:02
I WORK HARD at 14.11.2023 17:00 -> Feierabend!
I WORK HARD at 14.11.2023 17:05 -> Day is finished. Nothing to do.
```

# Fake Activity Recording 

Because i am an honest worker, LADIDA .... , i need to track my activity across my working hours. Would be nice to automate this.

With the function `perform_daily_lea()` you can just do that. It books 3:00 on a project and the remaining time on another project. Hardcoded for now.

I know it's bad, but works for now.

This is run after the day is finished. 

# True Activity Recording

This is now an unofficial script of our team at work. Yay i guess? 

1. Get the times from Jira Projects
2. Jam it into our activity recording tool inside BMD. 
3. Profit!

Same as Fake Activity Recording, but with real values. Get the values from Jira API. The activity recording is performed on Fridays after working hours. To calculate something, you know. And its company policy.



