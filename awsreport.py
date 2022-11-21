#!/usr/bin/python
# -*- coding: utf-8 -*-
# from asyncio.windows_events import NULL
from datetime import datetime
from datetime import date
from sre_constants import IN_IGNORE
import boto3
import sys, csv, datetime, time, re
import os
from os.path import expanduser
import json
import pandas as pd
data = []

with open("/var/local/etc/aws/credentials") as f:
    lines = f.read() ##Assume the sample file has 3 lines
    firstline = lines.split('\n', 1)[0]
string = firstline
profilename = re.sub(r"[\([{})\]]", "", string)
print('AwS Account name :', profilename)
print('--------------------------------')

if not os.environ.get('AWS_SHARED_CREDENTIALS_FILE', None):
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = \
        '/var/local/etc/aws/credentials'

if not os.environ.get('AWS_PROFILE', None):
    os.environ['AWS_PROFILE'] = profilename
client = boto3.client('ec2', region_name='ap-south-1')
response = client.describe_instances()
# json_string = json.dumps(response, indent=2, default=str)
# print(json_string)
instances = response["Reservations"]
for owner in instances:
    ownerid   = owner['OwnerId']
for instance in instances:
   allinstance = instance['Instances'][0]
   imageid = allinstance.get('ImageId')
   instanceid = allinstance.get('InstanceId')
   intype = allinstance.get('InstanceType')
   Keyname = allinstance.get('KeyName')
   availabilityzone = allinstance.get('Placement').get('AvailabilityZone')
   privateipaddress = allinstance.get('PrivateIpAddress')
   ipadd = allinstance.get('PrivateIpAddress')
   publicdnsname = allinstance.get('PublicDnsName')
   Status = allinstance.get('State').get('Name')
   StateCode = allinstance.get('State').get('Code')
   SubnetId = allinstance.get('SubnetId')
   vpcid = allinstance.get('VpcId')
   rootdevicetype = allinstance.get('RootDeviceType')
   architecture= allinstance.get('Architecture')
   launchtime = allinstance.get('LaunchTime')
   CoreCount = allinstance.get('CpuOptions').get('CoreCount')
   ThreadsPerCore = allinstance.get('CpuOptions').get('ThreadsPerCore')
   NetworkInterfaces = allinstance.get('NetworkInterfaces')
   blockdevicemappings = allinstance.get('BlockDeviceMappings',None)
   osname = allinstance.get('PlatformDetails')
   print("---------")
   devicename = []
   volumeid  = []
   volumestatus = []
   for blockdevice in blockdevicemappings:
        devicename.append(blockdevice.get('DeviceName'))
        #volumeid.append(blockdevice.get('Ebs').get('VolumeId'))
        #volumestatus.append(blockdevice.get('Ebs').get('Status'))
        print(privateipaddress, devicename) #, volumeid, volumestatus)
        #volumeid = blockdevice.get('Ebs').get('VolumeId')
        #volumestatus = blockdevice.get('Ebs').get('Status')  # 👉️ "volumestatus"
   data.append((privateipaddress, devicename)) #, volumeid, volumestatus)
for df in data:

df = pd.DataFrame(data, columns=['Private-ip-address','devicename','Volume-id','Volume-status'])
df.to_csv('csvreport.csv', index=False, sep=',')
