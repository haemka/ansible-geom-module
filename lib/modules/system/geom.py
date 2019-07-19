#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Henner M. Kruse <github@hmkruse.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: geom
short_description: Read geoms
description:
  - This module allows reading values from the FreeBSD storage
    frameworks geom command line tool. For details about the command options
    consult the geom(8) man page.
version_added: "2.8"
author: Henner M. Kruse (@haemka)
options:
  command:
    description: The geom subcommand to execute.
    type: str
    choices:
      - list
      - status
    default: list
    required: True
  devclass:
    description: The device class to query.
    type: str
    choices: 
      - cache
      - concat
      - eli
      - journal
      - label
      - mirror
      - mountver
      - multipath
      - nop
      - part
      - raid
      - raid3
      - sched
      - shsec
      - stripe
      - virstor
    default: part
    required: True
  device:
    description: An optional device name to query.
    type: str
    default: None
    required: True
requirements:
  - A BSD operating system with the geom command line utility
seealso:
  - name: FreeBSD System Manager's Manual - geom
    description: geom - universal control utility for GEOM classes
    link: https://www.freebsd.org/cgi/man.cgi?query=geom&apropos=0&sektion=8
'''

EXAMPLES = r'''
- name: Get partition data via geom
  geom:
    devclass: part
    
- name: Get disk device data via geom
  geom:
    command: status
    devclass: part
'''

RETURN = r'''
geom:
  description: A dictionary containing the returned GEOMs and sub section items
  returned: success
  type: dict
  sample:
    vtbd0:
      consumers:
        vtbd0:
          mediasize: "42949672960 (40g)"
          mode: "r1w1e2"
          name: "vtbd0"
          sectorsize: "512"
      entries: "152"
      first: "40"
      fwheads: "16"
      fwsectors: "63"
      geom_name: "vtbd0"
      last: "83886040"
      modified: "false"
      providers:
        vtbd0p1:
          efimedia: "hd(1,gpt,86e1234b-71e1-11e9-acd0-5bc9b916b6f9,0x28,0x400)"
          end: "1063"
          index: "1"
          label: "freebsd boot"
          length: "524288"
          mediasize": "524288 (512k)"
          mode: "r0w0e0"
          name: "vtbd0p1"
          offset: "20480"
          rawtype: "83bd6b9d-7f41-11dc-be0b-001560b84f0f"
          rawuuid: "86e1234b-71e1-11e9-acd0-5bc9b916b6f9"
          sectorsize: "512"
          start: "40"
          stripeoffset: "20480"
          stripesize: "0"
          type: "freebsd-boot"
      scheme: "gpt"
      state: "ok"
'''

# noinspection PyPep8
import re
# noinspection PyPep8
from ansible.module_utils.basic import AnsibleModule


def parse_list(output):
    result = dict()

    r = re.compile(r"(Geom name:.*?)(?=\n\n|\n?\Z)", re.S)
    matches = r.findall(output)
    for m in matches:
        r = re.compile((r"(?P<geom_string>Geom name:.*?)"
                        "(?=\nProviders:\n|\nConsumers:\n|\n?\Z)|"
                        "(?<=\nProviders:\n)(?P<providers_string>.+?)"
                        "(?=\nConsumers:\n|\n?\Z)|"
                        "(?<=\nConsumers:\n)(?P<consumers_string>.+?)"
                        "(?=\nProviders:\n|\n?\Z)"), re.S)

        geoms = dict()
        for i in r.finditer(m):
            geoms.update({k: v for k, v in i.groupdict().items()
                          if v is not None})

        items = dict()
        for l in geoms['geom_string'].splitlines():
            item = l.split(":")
            items.update({re.sub(r"\s", "_", item[0]).lower().strip(): item[1].strip()})
            if 'geom_name' in items:
                geom_name = items['geom_name']
                result.update({geom_name: {k: v for k, v in items.items()}})
                if 'providers_string' in geoms:
                    result[geom_name].update({'providers': parse_subsection(geoms['providers_string'])})
                if 'consumers_string' in geoms:
                    result[geom_name].update({'consumers': parse_subsection(geoms['consumers_string'])})

    return result


def parse_subsection(section):
    items = dict()
    result = dict()

    regex = re.compile(r"(?<=\d\.\s).+?(?=\n\S|\n\Z|\Z)", re.S)
    for m in regex.findall(section):
        for l in m.splitlines():
            item = l.split(":")
            items.update({re.sub(r'\s', '_', item[0].lower().strip()): item[1].strip()})
        if 'name' in items:
            name = items['name']
            result.update({name: {k: v for k, v in items.items()}})

    return result


def parse_status(output):
    result = dict()

    for l in output.splitlines():
        items = l.split()
        if items[1] == 'N/A':
            items[1] = None
        if items[2] == 'N/A':
            items[2] = None
        result.update({items[0]: {'status': items[1], 'components': items[2]}})

    return result


def run_geom(devclass, command, device):
    """
    Runs geom
    :return:
    """
    global module, geom_exec

    if command == 'status':
        command = 'status -s'

    if device:
        rc, out, err = module.run_command("%s %s %s %s" % (geom_exec,
                                                           devclass.upper(),
                                                           command, device)
                                          )
    else:
        rc, out, err = module.run_command("%s %s %s" % (geom_exec,
                                                        devclass.upper(),
                                                        command)
                                          )

    if rc != 0:
        module.fail_json(
            msg="Failed.", rc=rc, out=out, err=err
        )
    if command == 'list':
        result = parse_list(out)
    elif command == 'status -s':
        result = parse_status(out)
    else:
        result = None
        module.fail_json(
            msg="Failed.", rc=rc, out=out, err=err
        )

    return result


def run_module():
    global module, geom_exec

    module_args = dict(
        command=dict(type=str, default='list', choices=['list', 'status']),
        devclass=dict(type='str', default='part',
                      choices=['cache', 'concat', 'eli', 'journal', 'label',
                               'mirror', 'mountver', 'multipath', 'nop',
                               'part', 'raid', 'raid3', 'sched', 'shsec',
                               'stripe', 'virstor']
                     ),
        device=dict(type=str, default=None)
    )

    changed = False

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')

    command = module.params['command']
    devclass = module.params['devclass']
    device = module.params['device']

    geom_exec = module.get_bin_path('geom', True)

    geoms = run_geom(devclass, command, device)

    module.exit_json(
        changed=changed,
        geoms=geoms
    )

def main():
    run_module()

if __name__ == '__main__':
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
