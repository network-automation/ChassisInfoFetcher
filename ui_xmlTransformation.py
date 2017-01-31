# coding: utf-8
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
 ********************************************************************************
 * Project GIT  :  https://git.juniper.net/asmeureanu/ChassisInfoFetcher
 ********************************************************************************
"""

import urwid
import json
from xmlToPlainText import XMLToPlainText
from urlparse import urlparse
from ui_dialog import ui_dialog
import utils

class ui_xmlTransformation(ui_dialog):
   
             
    # direct mode main dialog
    def ShowDialog(self,button):
        caption = urwid.Text(('standoutLabel',u'Transform XML')) 
        help = urwid.Text([u'The tool provides capability for xml to plain text and xml to set-format transformations.'])
        
        xmlToPlainText = self.menu_button(u'XML to plain text', self.xmlToPlainText_dialog)
        #xmlToSet = self.menu_button(u'XML to set', self.xmlToSet_dialog)

        cancelButton = self.menu_button(u'Cancel', self.exit_window)
        self.top.open_box(urwid.Pile([caption,urwid.Divider(),help, urwid.Divider(),xmlToPlainText, cancelButton]))

        #top.open_box(urwid.Filler(urwid.Pile([caption,urwid.Divider(),help, urwid.Divider(),generalSettings,verifyFileButton, runButton,cancelButton])))



    # direct mode > run  | creates the DirectFetcher object and runs the appropiate console tool
    def xmlToPlainText_run(self,button):
        with open("execute.task", 'w') as f:
            f.write("XMLToPlainText")
        self.exit_program(None)   #closing the graphical interface to run the DirectFetcher

      
    # direct mode > general settings window
    def xmlToPlainText_dialog(self,button):
        caption = urwid.Text(('standoutLabel',u'Transform XML > XML to plain text')) 
        help = urwid.Text([u'Please specify the input file which is in xml format and the name of the output file.'])

        
        tb_username=urwid.Edit(('textbox', u"Input :\n"))
        tb_password=urwid.Edit(('textbox', u"Output :\n"))
        runButton = self.menu_button(u'Run', self.xmlToPlainText_run)
        cancelButton = self.menu_button(u'Cancel', self.exit_window)

        ### loading previouse settings
        def load_settings():
            try:
                settings=None
                with open('conf/xmlToPlainText.conf') as data_file:    
                   settings = json.load(data_file)
                tb_username.set_edit_text(settings["input"])
                tb_password.set_edit_text(settings["output"])

            except:
                self.messageBox("Error", "An error occured while attempting to load existing settings!")
    

        def saveButton_onclick(button):
            ### validation of the fields        
            username=tb_username.get_edit_text()
            password=tb_password.get_edit_text()

            
            if len(str(username)) < 3:
                self.messageBox("Input Error", "Username needs to have at least 3 charcters!")
                return
            if len(str(password)) < 3:
                self.messageBox("Input Error", "Password needs to have at least 3 charcters!")
                return

            #### saving the settings to disk
            try:
                data={}
                data["input"]=username
                data["output"]=password

                with open("conf/xmlToPlainText.conf", 'w') as f:
                    f.write(json.dumps(data, indent=4, sort_keys=True))

                self.messageBox("General Settings", "Settings have been saved succesfull!")
            except:
                self.messageBox("General Settings > Error", "There were errors while attempting to save the settings to disk.\nPlease check permissions rights and/or locks for file: directFetcher.conf")
                    
        saveButton = self.menu_button(u'Save', saveButton_onclick)

        self.top.open_box(urwid.Pile([caption,urwid.Divider(),help,urwid.Divider(),tb_username,tb_password,urwid.Divider(),saveButton,runButton,cancelButton]))
        load_settings()
