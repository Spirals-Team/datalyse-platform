#!/usr/bin/env python

import json
import sys
import os

HOSTVARS={
  'ansible_ssh_user': 'ubuntu',
  'ansible_ssh_private_key_file': os.path.expanduser('~/.ssh/google_compute_engine')
}

data = json.load(sys.stdin)
tags = {}

for name, host in data['_meta']['hostvars'].items():
  for tag in host['gce_tags']:
    if tag in tags:
      tags[tag].append(host)
    else:
      tags[tag] = [host]

for host in data['_meta']['hostvars'].values():
  hostvars = dict(HOSTVARS)
  hostvars['ansible_ssh_host'] = host['ansible_ssh_host']

  print '%s\t\t%s' % (host['gce_name'], \
    ' '.join(['%s=%s' % (k,v) for k,v in hostvars.items()]))

print ''

for tag, hosts in tags.items():
  print "[tag_%s]" % tag
  hostvars = dict(HOSTVARS)

  for host in hosts:
    print host['gce_name']
  
  print ''