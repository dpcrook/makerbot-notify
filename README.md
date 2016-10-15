# makerbot-notify

This script is for Makerware print job completing notification on  Linux.

# Background

I was jealous when my OctoPi jobs had all sorts of fancy plugins and webcam support and other stuff, especially notifications when a job was complete.
I made this quick-and-dirty python script to help as start to assuage my jealosy.

# Limitations at the moment

 - requires gmail and Linux for email. filesystem stuff probably would need some updates on other platforms
 - designed for tethered Makerware prints (parses the logfile)
 - lotsa hardcoded things
 
# Usage

```bash
cd ~/projects/makerbot-notify
# first edit create_cfg.py to match your gmail setting
./create_cfg.py
cd ~
# <<assumes makerware is already open/running!>>

~/projects/makerbot-notify/read_log.py
```

### example output

from the terminal

```
PrintDialog job: set job ID 1
Job 1 concluded
print job pgp-4-top.gcode concluded took 0:20:09
will send notice
sending email
From: your@gmail.com
To: your@gmail.com
Subject: pgp-4-top.gcode concluded

print job pgp-4-top.gcode concluded took 0:20:09

Email sent!
```

## installing this script

 - clone the rpo locally
 - edit the `create_cfg.py` and run it
 
### ubuntu 16.04



If you get error like this
```
ImportError: No module named dateutil.parser
```

```
sudo apt install python-dateutil
```
