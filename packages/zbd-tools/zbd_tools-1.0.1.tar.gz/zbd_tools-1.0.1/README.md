Copyright (C) 2022 Western Digital Corporation or its affiliates.

# zbd-tools

*zbd-tools* is a tool set providing functions determining the availability
of zone block device support. These tools will help identify kernel
configurations and whether zone block device software packages are
installed.

## Contributions and Bug Reports

Contributions are accepted as github pull requests or via email (`git
send-email` patches). Any problem may also be reported through github issues
page or by contacting:

* Tommy.McGee (tommy.mcgee@opensource.wdc.com)
* [Repository](https://github.com/westerndigitalcorporation/zbd-tools)

PLEASE DO NOT SUBMIT CONFIDENTIAL INFORMATION OR INFORMATION SPECIFIC TO DRIVES
THAT ARE VENDOR SAMPLES OR NOT PUBLICLY AVAILABLE.

### Requirements
*zbd-tools* requires the following for installation and usage:

- Python 3.0 or higher

### Installation Using *pip*
The following command can be executed to fetch and install the *zbd-tools* package.

```
$ pip install zbd-tools
Collecting zbd-tools
  Downloading zbd_tools-1.0-py3-none-any.whl (6.3 kB)
Installing collected packages: zbd-tools
Successfully installed zbd-tools-1.0
```

To uninstall *zbd-tools* from the system, use the following command.

```
$ pip uninstall zbd-tools
Found existing installation: zbd-tools 1.0
Uninstalling zbd-tools-1.0:
  Would remove:
    /usr/local/bin/zbd-check
    /usr/local/lib/python3.9/dist-packages/check/*
    /usr/local/lib/python3.9/dist-packages/zbd_tools-1.0.dist-info/*
Proceed (Y/n)? Y
Successfully uninstalled zbd-tools-1.0
```

## Usage

*zbd-tools* provides the *zbd-check* utility to check the zoned block device
features and applications supported by a Linux distribution.

### *zbd-check*

This utility allows checking a Linux distribution for zoned block device
support. Three different class of features are checked:
1. Kernel features: device types, device mapper targets and file systems support
   are checked.
2. User Libraries: *zbd-check* will list the installation status of user
   libraries related to zoned block devices.
3. User Applications: *zbd-check* will list the installation status of user
   applications related to zoned block devices.

*zbd-check* command line usage is displayed using the option "--help".


```
$ zbd-check --help
usage: zbd-check.py [-h] [--version]
options:
  -h, --help  show this help message and exit
  --version   show the version of zbd-check
```

The following shows an example output of the *zbd-check* utility executed on a
system running Fedora Linux 37.

```
$ zbd-check
------------------------------------------------------------------------
System Information:
------------------------------------------------------------------------
- Distribution: Fedora Linux 37 (Workstation Edition)
- Kernel Version: 6.0

------------------------------------------------------------------------
Kernel features:
------------------------------------------------------------------------
- Zoned block devices: supported
- Devices types:
    - SAS and SATA SMR hard-disks: supported
    - NVMe ZNS devices: supported
    - SCSI debug device ZBC emulation: supported
    - null_blk device zoned mode: supported
- file systems:
    - zonefs: supported
    - f2fs zoned mode: supported
    - btrfs zoned mode: supported
- Device mapper targets:
    - dm-linear: supported
    - dm-flakey: supported
    - dm-crypt: supported
    - dm-zoned: supported

------------------------------------------------------------------------
User Kernel zone management API:
------------------------------------------------------------------------
- Zone management kernel API header file: installed

------------------------------------------------------------------------
User Libraries:
------------------------------------------------------------------------
- libzbc:
    - Dynamic library installed, version 5.13.0
    - Static library installed
    - Development header files installed
- libzbd:
    - Dynamic library installed, version 2.0.2
    - Static library installed
    - Development header files installed
- libnvme:
    - Dynamic library installed, version 1.2
    - Static library not installed
    - Development header files installed

------------------------------------------------------------------------
User Applications:
------------------------------------------------------------------------
- fio: installed, version fio-3.29-7-g01686
- nvme-cli: installed, version 2.2.1
- dm-zoned-tools: installed, version 2.2.1
- zonefs-tools: installed, version 1.5.2
```
