#!/usr/bin/env python3

__author__ = 'Benjamin Daschel'


"""
Adapted from http://echorand.me/site/notes/articles/python_linux/article.html#block-devices

Read block device data from sysfs
"""

# from __future__ import print_function
import glob
import re
import os
import platform

import subprocess


PLATFORM_LINUX = 'Linux'
PLATFORM_MAC = 'Darwin'

DEVICE_PATH_OSX = '/dev/*'
DEVICE_PATH_LINUX = '/sys/block/*'

SAFE_PROTOCOLS = ['Secure Digital', 'USB']

# Add any other device pattern to read from
dev_pattern = ['sd.*','mmcblk*', 'disk[\d]$']


def is_system_name(name):

    return name == platform.system()

def get_os_block_device_path():

    if is_system_name(PLATFORM_LINUX):
        return DEVICE_PATH_LINUX
    elif is_system_name(PLATFORM_MAC):
        return DEVICE_PATH_OSX


def size(device):
    nr_sectors = open(device+'/size').read().rstrip('\n')
    sect_size = open(device+'/queue/hw_sector_size').read().rstrip('\n')

    # The sect_size is in bytes, so we convert it to GiB and then send it back
    return (float(nr_sectors)*float(sect_size))/(1024.0*1024.0*1024.0)


def get_block_device_list():

    block_devices = []
    for device in glob.glob(get_os_block_device_path()):
        for pattern in dev_pattern:
            if re.compile(pattern).match(os.path.basename(device)):
                block_devices.append(get_block_device_info(device))
                continue

    return block_devices

def get_block_device_info(device):

    if is_system_name(PLATFORM_MAC):
        output = subprocess.Popen('diskutil info {}'.format(device), stdout=subprocess.PIPE, shell=True)\
            .stdout\
            .read()\
            .decode('unicode_escape')

        info = {
            'node': re.search('^\s+(Device Node:)\s+([\w/]+)$', output, flags=re.MULTILINE).group(2),
            'size': re.search('^\s+(Total Size:).*\((\d+)\sBytes\).*$', output, flags=re.MULTILINE).group(2),
            'name': re.search('^\s+Device / Media Name:\s+(.*)$', output, flags=re.MULTILINE).group(1),
            'protocol': re.search('^\s+Protocol:\s+([\w\s]+)$', output, flags=re.MULTILINE).group(1)
        }
        return info


def filter_safe_block_devices(devices):

    return [device for device in devices if device['protocol'] in SAFE_PROTOCOLS]


def print_block_device_list():

    for device in filter_safe_block_devices(get_block_device_list()):
        print(device)


if __name__=='__main__':
    print_block_device_list()
