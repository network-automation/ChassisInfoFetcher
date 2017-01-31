#!/usr/bin/env python
"""
 ******************************************************************************
 * Copyright (c) 2014  Juniper Networks. All Rights Reserved.
 *
 * YOU MUST ACCEPT THE TERMS OF THIS DISCLAIMER TO USE THIS SOFTWARE
 *
 * JUNIPER IS WILLING TO MAKE THE INCLUDED SCRIPTING SOFTWARE AVAILABLE TO YOU
 * ONLY UPON THE CONDITION THAT YOU ACCEPT ALL OF THE TERMS CONTAINED IN THIS
 * DISCLAIMER. PLEASE READ THE TERMS AND CONDITIONS OF THIS DISCLAIMER
 * CAREFULLY.
 *
 * THE SOFTWARE CONTAINED IN THIS FILE IS PROVIDED "AS IS." JUNIPER MAKES NO
 * WARRANTIES OF ANY KIND WHATSOEVER WITH RESPECT TO SOFTWARE. ALL EXPRESS OR
 * IMPLIED CONDITIONS, REPRESENTATIONS AND WARRANTIES, INCLUDING ANY WARRANTY
 * OF NON-INFRINGEMENT OR WARRANTY OF MERCHANTABILITY OR FITNESS FOR A
 * PARTICULAR PURPOSE, ARE HEREBY DISCLAIMED AND EXCLUDED TO THE EXTENT ALLOWED
 * BY APPLICABLE LAW.
 * 
 * IN NO EVENT WILL JUNIPER BE LIABLE FOR ANY LOST REVENUE, PROFIT OR DATA, OR
 * FOR DIRECT, SPECIAL, INDIRECT, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE DAMAGES
 * HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY ARISING OUT OF THE
 * USE OF OR INABILITY TO USE THE SOFTWARE, EVEN IF JUNIPER HAS BEEN ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGES.
 * 
 * 
 ********************************************************************************
 * Project GIT  :  https://git.juniper.net/asmeureanu/ChassisInfoFetcher
 ********************************************************************************
"""

from __future__ import print_function
import base64
import os
import socket
import sys
import time
import traceback
import string
import re
import json

import paramiko

from StringIO import StringIO

from multiprocessing import Pool
from datetime import date, datetime, timedelta

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.exception import *
from lxml import etree as ET

import logging
import logging.config



class XMLToPlainText:

    def __init__(self):
        self.parsedValues=[]

    def __call__(self,args):
        return self.cleanNamespace("<hello></hello>")


    def cleanNamespace(self,text):
        textEdit = re.sub('<configuration.*>', '', text)
        textEdit = re.sub('</configuration>', '', textEdit)

        it = ET.iterparse(StringIO(textEdit))
        for _, el in it:
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
        root = it.root

        string=""



        self.parse_tree(root)
        for value in self.parsedValues:
            string = string + value + "\n"
        self.parsedValues = []
        return string

     # process job OVERIDDED from the directFecther since it uses SpaceEz and not direct connections

    def parse_tree(self, root, commandLine=[""]):
        #print ("Hello {}".format(root.tag))
        blacklist = {"name","contents","daemon-process"}
        ignore = {"configuration", "undocumented","rpc-reply", "cli"}
        if(root.tag not in ignore):  #!!!ignores comments, and the <configuration> and <rpc-reply> tags and root.tag.find("{")==-1)
            if root.tag not in blacklist:
                commandLine.append(root.tag)
                #print ("{}".format(root.tag))
            if(len(root)==0):
                if(root.text!=None):
                    if len(root.text.strip().replace(" ",""))==len(root.text.strip()):
                        line = " ".join(commandLine) + " " + root.text.strip() + "\n"
                    else:
                        line = " ".join(commandLine) + ' "' + root.text.strip() + '"'
                else:
                    line = " ".join(commandLine) 
                self.parsedValues.append(line.strip())
                #commandLine.pop()
            else:


                if (root[0].tag=="name" and len(root)>1):
                    commandLine.append(root[0].text.strip())
                    for i in xrange(1,len(root)):
                        self.parse_tree(root[i],commandLine)
                    #print ("1 {}".format(commandLine))
                    commandLine.pop()
                else:
                    for child in root:
                        self.parse_tree(child,commandLine)

            #print ("2 {}".format(commandLine))
            if root.tag not in blacklist:
                commandLine.pop()
        elif root.tag == "cli":
            pass
        else:
            for child in root:
                self.parse_tree(child,commandLine)




if __name__ == '__main__':

    logging.config.fileConfig('conf/logging.conf')
    try:
        with open('conf/xmlToPlainText.conf') as data_file:    
            fileNames = json.load(data_file)
    except:
        msg="Loading and Verifying File List : Unable to read input or parse file 'xmlToPlainText.conf' responsible for storing input and output file names for xml to plaintext transformation."
        logging.error(msg)
        sys.exit(1)

    try:
        with open(fileNames["input"], "r") as data_file:
            text = data_file.read()
    except:
        msg="Loading and Verifying File List : Unable to read input or parse file 'xmlToPlainText.conf' responsible for storing input and output file names for xml to plaintext transformation."
        logging.error(msg)
        sys.exit(1)

    df=XMLToPlainText()
    text = df.cleanNamespace(text)

    # To test single process job  for debugging purposes use the following: 
    #df.job("{'username': 'mkim', 'host': '172.30.77.181', 'password': 'mkim', 'port': '22'}")
    try:
        with open(fileNames["output"], "w") as data_file:
            data_file.write(text)
    except:
        msg="Unable to write output file."
        logging.error(msg)
        sys.exit(1) 