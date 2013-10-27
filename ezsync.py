#!/bin/python
import argparse
import json
import logging
import os
import smtplib
import subprocess
import time

CONFIG_FILE = 'config.json'
LOG_FILE = 'ezsync.log'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--profile', help='Backup profile')
    parser.add_argument('-e', '--email', help='Email address to send a report upon completion')
    parser.add_argument('-d', '--dry', help='Dry run', action='store_true')
    parser.add_argument('-l', '--list', help='List profiles', action='store_true')
    return parser.parse_args()

def send_email(login, to, subject='', message=''):
    """login = {user, password, server, port=587}"""
    client = smtplib.SMTP('%s:%s' % (login['server'], login.get('port', 587)))
    client.starttls()
    client.login(login['user'], login['password'])
    client.sendmail(login['user'], to, 'Subject: %s\n\n%s' % (subject, message))
    client.quit()

def expand_path(path):
    return os.path.expandvars(os.path.expanduser(path))

def run_rsync(profile, flags):
    source = expand_path(profile['source'])
    target = expand_path(profile['target'])
    excludes = [('--exclude="%s"' % e) for e in profile.get('excludes', [])]
    command = ['rsync'] + flags + excludes + [source, target]
    logging.info('Running profile \"%s\"' % profile['name'])
    starttime = time.time()
    returncode = subprocess.call(command)
    endtime = time.time()
    print ' '.join(command)
    if returncode != 0:
        logging.warning('%s\nReturn code: %d' % (' '.join(command), returncode))
    logging.info('Complete. Elapsed time: %0.2f s', endtime - starttime)
    return returncode == 0

def init_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        filemode='w',
        level=logging.DEBUG,
        format='[ezsync] %(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

def main():
    init_logging()
    args = parse_args()
    config = json.loads(open(CONFIG_FILE).read())

    # Find the profile specified, otherwise select all of them. Profile name
    # need not be unique, so collect all matching names.
    if args.profile:
        profiles = [p for p in config['profiles'] if p['name'] == args.profile]
    else:
        profiles = config['profiles']

    # Listing profiles is an exclusive option; nothing else is done.
    if args.list:
        print '\n'.join(set([p['name'] for p in profiles]))
        return
        
    # Build a list of flags.
    flags = config['flags']
    if 'excludes' in config:
        flags += [('--exclude="%s"' % e) for e in config['excludes']]
    if args.dry:
        flags += ['-n']

    # Now, do it!
    success = True
    for profile in profiles:
        success = run_rsync(profile, flags) and success
    if args.email:
        send_email(
            login=config['email'],
            to=args.email,
            subject=('[OK]' if success else '[WARNING]') + ' ezsync complete.',
            message=open(LOG_FILE).read())
    
if __name__ == '__main__':
    main()