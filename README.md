# ansible-geom-module
Ansible module for reading data from the FreeBSD storage frameworks geom command line tool

## geom

## Description
This module allows reading values from the FreeBSD storage frameworks geom command line tool. For details about the command options consult the geom(8) man page.

version_added: "2.8"

## Options
|                | Description                     | Type   | Choices                  | Default    | Required |
|----------------|---------------------------------|--------|--------------------------|------------|----------|
| ```command```  | The geom subcommand to execute. | String | ```list```, ```status``` | ```list``` | Yes      |
| ```devclass``` | The device class to query.      | String | ```cache```, ```concat```, ```eli```, ```journal```, ```label```, ```mirror```, ```mountver```, ```multipath```, ```nop```, ```part```, ```raid```, ```raid3```, ```sched```, ```shsec```, ```stripe```, ```virstor``` | ```part``` | Yes |
| ```device``` | An optional device name to query. | String |  |  | No |

## Requirements
- A BSD operating system with the geom command line utility

## Links:
  - name: FreeBSD System Manager's Manual - geom
    description: geom - universal control utility for GEOM classes
    link: https://www.freebsd.org/cgi/man.cgi?query=geom&apropos=0&sektion=8

## Examples
```
- name: Get partition data via geom
  geom:
    devclass: part
    
- name: Get partition status via geom
  geom:
    command: status
    devclass: part
```

## Example return data:
```
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
```
