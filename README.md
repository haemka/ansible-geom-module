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
    "geoms": {
        "vtbd0": {
            "consumers": {
                "vtbd0": {
                    "mediasize": "42949672960 (40g)",
                    "mode": "r1w1e2",
                    "name": "vtbd0",
                    "sectorsize": "512"
                }
            },
            "entries": "152",
            "first": "40",
            "fwheads": "16",
            "fwsectors": "63",
            "geom_name": "vtbd0",
            "last": "83886040",
            "modified": "false",
            "providers": {
                "vtbd0p1": {
                    "efimedia": "hd(1,gpt,86e1234b-71e1-11e9-acd0-5bc9b916b6f9,0x28,0x400)",
                    "end": "1063",
                    "index": "1",
                    "label": "freebsd boot",
                    "length": "524288",
                    "mediasize": "524288 (512k)",
                    "mode": "r0w0e0",
                    "name": "vtbd0p1",
                    "offset": "20480",
                    "rawtype": "83bd6b9d-7f41-11dc-be0b-001560b84f0f",
                    "rawuuid": "86e1234b-71e1-11e9-acd0-5bc9b916b6f9",
                    "sectorsize": "512",
                    "start": "40",
                    "stripeoffset": "20480",
                    "stripesize": "0",
                    "type": "freebsd-boot"
                },
                "vtbd0p2": {
                    "efimedia": "hd(2,gpt,8d8691b1-71e1-11e9-acd0-5bc9b916b6f9,0x428,0x13ffbb0)",
                    "end": "20971479",
                    "index": "2",
                    "label": "freebsd root",
                    "length": "10736852992",
                    "mediasize": "10736852992 (10g)",
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
                "vtbd0p3": {
                    "efimedia": "hd(3,gpt,7c0dc12f-ab17-4b56-92ad-27176b6886e6,0x13fffd8,0x3c00001)",
                    "end": "83886040",
                    "index": "3",
                    "label": "zfs pool",
                    "length": "32212255232",
                    "mediasize": "32212255232 (30g)",
                    "mode": "r0w0e0",
                    "name": "vtbd0p3",
                    "offset": "10737397760",
                    "rawtype": "516e7cba-6ecf-11d6-8ff8-00022d09712b",
                    "rawuuid": "7c0dc12f-ab17-4b56-92ad-27176b6886e6",
                    "sectorsize": "512",
                    "start": "20971480",
                    "stripeoffset": "2147463168",
                    "stripesize": "0",
                    "type": "freebsd-zfs"
                }
            },
            "scheme": "gpt",
            "state": "ok"
        }
    }
}
```

### Partition status (command=status devclass=part):
```
$ ansible example.com -m geom -a command=status
example.com | SUCCESS => {
    "changed": false,
    "geoms": {
        "vtbd0p1": {
            "components": "vtbd0",
            "status": "OK"
        },
        "vtbd0p2": {
            "components": "vtbd0",
            "status": "OK"
        },
        "vtbd0p3": {
            "components": "vtbd0",
            "status": "OK"
        }
    }
}
```
