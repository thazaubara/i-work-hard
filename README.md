# I WORK HARD
Automation of time booking ... because that sucks.

# Installation
Download chromedriver for platform.
https://googlechromelabs.github.io/chrome-for-testing/#stable

I use mac, I put the binary in `/usr/local/bin`

Let the OS verify the binary. May be skipped with other OS.

`xattr -d com.apple.quarantine chromedriver`

# Links
Install chromedriver
https://www.geeksforgeeks.org/how-to-install-selenium-webdriver-on-macos/

# Problems
Problem chrome newer than what chromedriver supports.

# Logic

![image-20231114160809927](./_images/image-20231114160809927.png)

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

