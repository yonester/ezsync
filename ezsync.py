#!/bin/python
import argparse
from datetime import datetime
import json
import os
import subprocess

DEFAULT_CONFIG = 'config.json'

def parse_args(profiles):
    parser = argparse.ArgumentParser()
    parser.add_argument('profile', help='Backup profile', choices=profiles)
    parser.add_argument('-d', '--dry', help='Dry run', action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    config = json.loads(open(DEFAULT_CONFIG).read())
    args = parse_args(config['profiles'])
    flags = config['flags'] + \
            (' -n ' if args.dry else ' ') + \
            ' '.join([('--exclude=' + e) for e in config['excludes']])
    profile = config['profiles'][args.profile]
    print str(datetime.today()) + ': Running backup set.'
    for pair in profile['pairs']:
        os.system('rsync {} {} {}'.format(
            flags + ((' ' + pair[2]) if len(pair) == 3 else ''),
            profile['source'] + '/' + pair[0],
            profile['target'] + '/' + pair[1]))
