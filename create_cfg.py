#!/usr/bin/env python

import json

# partly based on http://stackabuse.com/how-to-send-emails-with-gmail-using-python/

example_config = [{
    'gmail': {
        'gmail_user': 'david.crook@gmail.com',
        'gmail_password': '',
        'email_to_list': ['me@gmail.com', 'bill@gmail.com'],
        'subject': 'print job status'
    },
}, {
    'motion': {
        'motion_dir': '/data/motion'
    }
}]

# write json file
output_json = 'example.json'
with open(output_json, 'w') as jsonfile:
    print 'saving to', output_json
    json.dump(example_config, jsonfile)
