# coding: utf-8
#!/usr/bin/env python
# <*******************
# 
#   Copyright (c) 2017 Juniper Networks . All rights reserved.
#   Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the 
#   documentation and/or other materials provided with the distribution.
#
#   3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this 
#   software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
#   LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
#   EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# *******************>

import urwid
import json
import utils
from assistedFetcher import AssistedFetcher
from urlparse import urlparse
from ui_dialog import ui_dialog
import utils


class ui_help(ui_dialog):
    # assisted mode main dialog
    def ShowDialog(self,button):
        caption = urwid.Text(('standoutLabel',u'Help | Chassis Information Fetcher 2.0')) 
        help = urwid.Text([u"""The application is designed to help juniper equipments owners to retrive information about their devices for Advanced Services deliverables. It automatially detects the type of device (for example: MX, SRX, QFX) and executes the necessary "show" commands for that device.

It supports multiple operation modes:
     a) Direct mode
        In direct mode the tool retrieves the device list and login details stored in the ‘hosts.csv’ file and proceeds to connect to the devices in a parallel fashion. 
        The hosts file can be found in the ChassisInfoFetcher2.0 directory. The format of each entry in the file should be: 
        <Device IP address, Username, Password, SSH port>

        Alternatively, you can include only the IP address of the devices in the hosts file and specify the username, password, and SSH port in the Settings menu (Direct Mode > Settings).
 
        The Direct Mode > Commands section lists the commands that are to be executed by the tool for each device group – these can be modified by the engineer (note: only ‘show’ commands and ‘request support information’ are valid commands).

     b) Assisted mode
        In assisted mode the tool retrieves the device list from Junos Space. The Junos space login details as well as the login details of the devices need to be specified in the Settings section of Junos Space | Assisted Fetcher. 
        Afterwards the tool connects to all devices in parallel and extracts their chassis information.

     c) Service Inside Service Now (SNSI) mode
        In SNSI mode the tool connects to Junos Space, retrieves the iJMB files collected by Junos Space and extracts the needed chassis information. The Settings menu is the same as that of the Full Fetcher. 
        The following list provides the list of files that contain the configuration information. 

            •   *_AISESI.txt—Contains event support information; output of multiple Junos OS show commands
            •   *_rsi.txt—Contains “request support information” of the device
            •   *_cfg_xml.xml—Contains device configuration information in XML format (show configuration | display inheritance | display xml)
            •   *_shd_xml.xml—Contains output of the “show chassis hardware” command in XML format
            •   *_ver_xml.xml—Contains the hostname and version information about the software (including the software help files and AI-Scripts bundle) running on the device (show version)

        That is why in the command section of the Service Now Service Insight mode, the relevant files are specified and not actual commands (for example, include: _AISESI.txt, _cfg_xml, _shd_xml).

     d) Full mode
        In full mode the CIF tool retrieves the device list from Junos Space and instructs Junos Space to connect to all the devices in parallel. In this mode you need to enter only the Junos Space login details in the Settings menu.

            """])
        
        closeButton = self.menu_button(u'Close', self.exit_window)

        self.top.open_box(urwid.Pile([caption,help,closeButton]))
          
             
   