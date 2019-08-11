# ansible-geom-module
Ansible module for reading data from the FreeBSD storage frameworks geom command line tool

## geom

## Description
This module allows reading values from the FreeBSD storage frameworks geom command line tool. For details about the command options consult the geom(8) man page.
This module was developed and tested with Ansible 2.8.

## Options
|                | Description                     | Type   | Choices                  | Default    | Required |
|----------------|---------------------------------|--------|--------------------------|------------|----------|
| ```command```  | The geom subcommand to execute. | String | ```list```, ```status``` | ```list``` | Yes      |
| ```devclass``` | The device class to query.      | String | ```cache```, ```concat```, ```eli```, ```journal```, ```label```, ```mirror```, ```mountver```, ```multipath```, ```nop```, ```part```, ```raid```, ```raid3```, ```sched```, ```shsec```, ```stripe```, ```virstor``` | ```part``` | Yes |
| ```device``` | An optional device name to query. | String |  |  | No |

## Requirements
- A BSD operating system with the geom command line utility

## Links:
- FreeBSD System Manager's Manual - geom - universal control utility for GEOM classes: [geom(8)](https://www.freebsd.org/cgi/man.cgi?query=geom&apropos=0&sektion=8)

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
### Partition list (command=list devclass=part (Default)):
```
# ansible example.com -m geom
example.com | SUCCESS => {
    "changed": false,
    "geoms": [
        {
            "consumers": [
                {
                    "mediasize": "42949672960 (40G)",
                    "mode": "r1w1e2",
                    "name": "vtbd0",
                    "sectorsize": "512"
                }
            ],
            "entries": "152",
            "first": "40",
            "fwheads": "16",
            "fwsectors": "63",
            "geom_name": "vtbd0",
            "last": "83886040",
            "modified": "false",
            "providers": [
                {
                    "efimedia": "HD(2,GPT,8d8691b1-71e1-11e9-acd0-5bc9b916b6f9,0x428,0x13ffbb0)",
                    "end": "20971479",
                    "index": "2",
                    "label": "(null)",
                    "length": "10736852992",
                    "mediasize": "10736852992 (10G)",
                    "mode": "r1w1e1",
                    "name": "vtbd0p2",
                    "offset": "544768",
                    "rawtype": "516e7cb6-6ecf-11d6-8ff8-00022d09712b",
                    "rawuuid": "8d8691b1-71e1-11e9-acd0-5bc9b916b6f9",
                    "sectorsize": "512",
                    "start": "1064",
                    "stripeoffset": "544768",
                    "stripesize": "0",
                    "type": "freebsd-ufs"
                },
                {
                    "efimedia": "HD(2,GPT,8d8691b1-71e1-11e9-acd0-5bc9b916b6f9,0x428,0x13ffbb0)",
                    "end": "20971479",
                    "index": "2",
                    "label": "(null)",
                    "length": "10736852992",
                    "mediasize": "10736852992 (10G)",
                    "mode": "r1w1e1",
                    "name": "vtbd0p2",
                    "offset": "544768",
                    "rawtype": "516e7cb6-6ecf-11d6-8ff8-00022d09712b",
                    "rawuuid": "8d8691b1-71e1-11e9-acd0-5bc9b916b6f9",
                    "sectorsize": "512",
                    "start": "1064",
                    "stripeoffset": "544768",
                    "stripesize": "0",
                    "type": "freebsd-ufs"
                }
            ],
            "scheme": "GPT",
            "state": "OK"
        }
    ]
}


```

### Partition status (command=status devclass=part):
```
$ ansible example.com -m geom -a command=status
example.com | SUCCESS => {
    "changed": false,
    "geoms": [
        {
            "components": "vtbd0",
            "name": "vtbd0p1",
            "status": "OK"
        },
        {
            "components": "vtbd0",
            "name": "vtbd0p2",
            "status": "OK"
        }
    ]
}
```
