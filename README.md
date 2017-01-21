# makerbot-notify

For Makerware print job (email) notifications (on Linux).

![Example motion capture][print_cap]

It can be configured to send an email (with optional webcam capture) when a Makerware print job completes, even on older models like the Replicator, or Replicator 2/2X.

# Background

I was jealous when my OctoPi jobs running on my Lulzbot had all sorts of fancy plugins and webcam support and other stuff. One big area especially was notifications when a job was complete.

I made this python script to fix that!

# Limitations at the moment

 - requires gmail and Linux for email. filesystem stuff probably would need some updates on other platforms, but I haveen't tried
 - designed for tethered Makerware prints (locates and parses the app logfile)
 - probably many hardcoded things

# Usage


```bash
cd ~/projects/makerbot-notify
# first edit create_cfg.py to match your gmail setting
./create_cfg.py
cd ~
# <<assumes makerware is already open/running!>>

~/projects/makerbot-notify/read_log.py
```

Relies on a JSON config file. Edit `create_cfg.py` to match your config, and generate one.  Then launch the script (after Makerware has been opened).

Added webcam support based on `motion` app, which is intended to send you an image from the completed print.

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

 1. Clone the repo locally
 1. Edit the `create_cfg.py` and run it
 1. Run `read_log.py`


## Platform notes

### ubuntu 16.04



If you get error like this
```
ImportError: No module named dateutil.parser
```

```
sudo apt install python-dateutil
```

[print_cap]: https://github.com/idcrook/makerbot-notify/raw/gh-pages/img/print_snapshot.jpg
