#!/usr/bin/env python

# Send notifications based on makerware print job status (from parsing logfile)

#
# TODO:
#  - implement logging
#  - send image from webcam with email?
#  - class modules
#  - create github repo
#
# DONE
#  - email notification
#  - use most recent logfile if none specified
#


import dateutil.parser
import datetime
import json
import os
import re
import smtplib
import sys
import time

exc_path = os.path.dirname(sys.argv[0])

# http://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-ones-from-json-in-python
def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

CONFIG = {}
with open (os.path.join(exc_path, 'example.json'), 'r') as jsonfile:
    CONFIG = json_load_byteified(jsonfile)

print 'will send any email as', CONFIG[0]['gmail']['gmail_user']


# http://code.activestate.com/recipes/157035-tail-f-in-python/#c4
def tail_f(file):
    interval = 1.0

    while True:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(interval)
            file.seek(where)
        else:
            yield line

def send_notification(data):
    # print data
    status = data['status']
    start = data['start_time']
    done = data['change_time']
    filename = data['filename']
    duration = done - start
    s = '%(duration)s job %(filename)s %(status)s' % vars()
    print s
    short = '%(status)s %(filename)s' % vars()
    if done > CURRENT_TIME:
        print "will send notice"
        send_email(short, s)

def send_email(subj, jobinfo):
    print "sending email"
    email_config =  CONFIG[0]['gmail']
    gmail_user     =  email_config['gmail_user']
    gmail_password =  email_config['gmail_password']
    to             =  email_config['email_to_list']
    subject        = subj
    body           = jobinfo
    fromc          = gmail_user
    
    email_text = """\
From: %s  
To: %s  
Subject: %s

%s
""" % (fromc, ", ".join(to), subject, body)

    print email_text
    
    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(fromc, to, email_text)
        server.close()

        print 'Email sent!'
    except:  
        print 'Something went wrong...'
    
    

inputFile = re.compile(r'\s*"input_file"\s*\:\s*"([^"]+)"')

# "input_file" : "/tmp/MakerBot Desktop-Oyu7m1/Deanerys_v1.gcode",

jobWatch = re.compile(r"conveyor::JobWatch")
jobWatchjobSetJobID = re.compile(r"JobWatch::setJobID")
setJobID = re.compile(r"set job ID (\d+)")
jobWatchjobChanged = re.compile(r"JobWatch::jobChanged")
jobChanged = re.compile(r"Job (\d+) (\S+)")

# void conveyor::JobWatch::setJobID(conveyor::JobID)
# 2016-03-06 18:41:38
# PrintDialog job: set job ID 0
# void conveyor::JobWatch::jobChanged(conveyor::JobID)
# 2016-03-06 19:15:17
# Job 0 canceled
# void conveyor::JobWatch::setJobID(conveyor::JobID)
# 2016-03-06 19:17:17
# PrintDialog job: set job ID 1
# void conveyor::JobWatch::jobChanged(conveyor::JobID)
# 2016-03-06 21:52:39
# Job 1 concluded

# >>> import dateutil.parser
# >>> dateutil.parser.parse("Sun Mar  6 21:52:39 2016")
# datetime.datetime(2016, 3, 6, 21, 52, 39)

line1 = ""
line2 = ""
line3 = ""
i = 0

CURRENT_TIME = datetime.datetime.now()
JOB_INFO = {}
filename = ""

# Logfiles live in ~/Things/Logs
logfile_dir = os.path.expanduser("~/Things/Logs")
if sys.argv[1:]:
    logfile_name = sys.argv[1]
else:
    
    dated_files = [( os.path.getmtime(os.path.join(logfile_dir, fn)), 
                     os.path.basename(os.path.join(logfile_dir, fn)) )
               for fn in os.listdir(logfile_dir) if fn.lower().endswith('.log')]
    # print dated_files
    dated_files.sort()
    dated_files.reverse()
    newest = dated_files[0][1]
    logfile_name = os.path.join(logfile_dir, newest)
    
print logfile_name

for line in tail_f(open(logfile_name,'r')):
    i += 1
    line1 = line2
    line2 = line3
    line3 = line
    # print i
    
    m = jobWatch.search(line1)
    if m:
        # print JOB_INFO
        timestamp = dateutil.parser.parse(line2)
        # print line1.strip()
        # print timestamp
        print line3.strip()
        if jobWatchjobChanged.search(line1):
            status = jobChanged.search(line3)
            if status:
                thisJobID = status.group(1)
                thisStatus = status.group(2)
                JOB_INFO[thisJobID]['change_time'] = timestamp
                JOB_INFO[thisJobID]['status'] = thisStatus
                JOB_INFO[thisJobID]['filename'] = filename
                notify_data = JOB_INFO[thisJobID]
                send_notification(notify_data)
            # print status.groups()
        elif jobWatchjobSetJobID.search(line1):
            jobId = setJobID.search(line3)
            if jobId:
                JOB_INFO[jobId.group(1)] = {'start_time' : timestamp}
            
    g = inputFile.match(line1)
    if g:
        # print g.groups()
        filename = os.path.basename(g.group(1))
        #print filename
