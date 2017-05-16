#!/usr/bin/env python
#!encoding:utf-8
#@date:2017-05-10

'''
notify tool
'''

import pyinotify
import os
import tools

def get_monitor_event(event_str):
    return None


class EventHandler(pyinotify.ProcessEvent):

    def process_IN_CREATE(self,event):
        tools.log("Creating:%s" % event.pathname)

    def process_IN_DELETE(self,event):
        tools.log("Deleting:%s" % event.pathname,tools.WARN)

    def process_IN_ACCESS(self,event):
        tools.log("Accessing:%s" % event.pathname,"UNDERLINE")

    def process_IN_OPEN(self,event):
        tools.log("Openning:%s" % event.pathname)

    def process_IN_MODIFY(self,event):
        tools.log("Modifing:%s" % event.pathname,tools.WARN)

    def process_IN_ATTRIB(self,event):
        tools.log("Changing attribute:%s" % event.pathname,tools.WARN)

    def process_IN_CLOSE_WRITE(self,event):
        tools.log("Close file with writing:%s" % event.pathname,tools.WARN)

    def process_IN_CLOSE_NOWRITE(self,event):
        tools.log("Close file without writing:%s" % event.pathname,tools.INFO)

    def process_IN_MOVED_TO(self,event):
        tools.log("Move to :%s" % event.pathname,tools.WARN)

    def process_IN_MOVED_FROM(self,event):
        tools.log("Move from:%s" % event.pathname,tools.WARN)


def test():
    handler=EventHandler()
    wm=pyinotify.WatchManager()
    notifier=pyinotify.Notifier(wm,handler)
    wm.add_watch(["/etc/passwd",""],pyinotify.ALL_EVENTS,rec=True,auto_add=True)
    notifier.loop()
test()

