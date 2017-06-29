#!/usr/bin/env python
#!encoding:utf-8
#@date:2017-05-10

'''
notify tool
'''

import pyinotify
import os
import json
import sys
import re
import time
import socket

from email_tool import EmailTool

import file_tool

from tools import Monitor_Log

'''
define global variables
'''
target_files=[]
key_words=''
regx=None
emailtool=None
s_monitors=None

def get_monitor_event(event_str):
    return None


class TomcatEventHandler(pyinotify.ProcessEvent):
    '''
    TomcatEventHandler,the handler tha handle tomcat file change
    2017-06-02
    '''

    def __init__(self,whitelist=[]):
        self.__whitelist=whitelist
        self.__tomcat_regx=re.compile('.*(\.xml|\.jar|\.sh)$')
        self.__ip=get_ip()
        self._log=Monitor_Log(logname='TomcatLog',logfile='%s-tomcat-' % self.__ip)


    def process_IN_OPEN(self,event):
        pass

    def process_IN_MODIFY(self,event):
        self.__log.warning("Modifing file %s" % event.pathname)

    def process_IN_CREATE(self,event):
        self.__log.warning("Creating file %s" % event.pathname)

    def process_IN_DELETE(self,event):
        self.__log.warning("Deleting file %s" % event.pathname)
        if(self.__tomcat_regx.search(event.pathname) and (event.pathname not in self.__whitelist)):
            if get_email_tool():
                string='''The Tomcat file %s was deleted at %s .(IP : %s)''' % (event.pathname,time.ctime(),self.__ip)
                emailtool.send_text(message=string,subject='%s tomcat file deleted' % self.__ip)


    def process_IN_CLOSE_WRITE(self,event):
        self.__log.warning("Write file %s" % event.pathname)
        if (event.pathname.endswith('.jsp') or event.pathname.endswith('.jspx')) and (not is_filechange_ok(event.pathname)) and (event.pathname not in self.__whitelist):
            if get_email_tool():
                string='''Web shell(%s) found in the machine %s at %s''' % (event.pathname,self.__ip,time.ctime())
                emailtool.send_email_with_attachment(send_file=[event.pathname],message=string,subject="Web shell found at %s" % self.__ip)

        elif(self.__tomcat_regx.search(event.pathname) and (event.pathname not in self.__whitelist)):
            if get_email_tool():
                string='''Important file %s changed at %s at %s''' % (event.pathname,self.__ip,time.ctime())
                emailtool.send_text(message=string,subject='File changed at %s' % self.__ip)


    def process_IN_ATTRIB(self,event):
        self.__log.warning("Change attribute %s" % event.pathname)

    def process_IN_MOVED_TO(self,event):
        pass

    def process_IN_MOVED_FROM(self,event):
        pass


class EventHandler(pyinotify.ProcessEvent):
    '''
    Special monitor files
    create=[]
    delete=[]
    access=[]
    open=[]
    modify=[]
    change=[]
    '''
    #self.__message_string="""File %s was %s at %s at %s ,please handle it."""

    def __init__(self,create,delete,access,open,modify,change,whitelist):
        self.__create=create
        self.__delete=delete
        self.__access=access
        self.__open=open
        self.__modify=modify
        self.__change=change
        self.__whitelist=whitelist
        self.__ip=get_ip()
        self.__message_string="""File %s was %s at %s at %s ,please handle it."""
        self.__log=Monitor_Log(logname='SystemLog',logfile='%s-system-' % self.__ip)

    def process_IN_CREATE(self,event):
        self.__log.warning("Creating:%s" % event.pathname)
        if event.pathname in self.__create:
            if get_email_tool():
                emailtool.send_email_with_attachment(send_file=[event.pathname],\
                                                    message="Special file %s created at %s at time,please handle it" % (event.pathname,self.__ip,time.ctime()),\
                                                    subject="Special file %s created at %s" % (event.pathname,self.__ip))
        #file_tool.handle_file_event(event,_FILE_CHANGED)

    def process_IN_DELETE(self,event):
        self.__log.warning("Deleting:%s" % event.pathname)
        if event.pathname in self.__delete:
            string='''File %s was deleted at %s  at %s,please handle it''' % (event.pathname,self.__ip,time.ctime())
            if get_email_tool():
                emailtool.send_text(message=string,subject='File delete at %s' % self.__ip)
        #file_tool.handle_file_event(event,_FILE_DELETED)

    def process_IN_ACCESS(self,event):
        self.__log.warning("Accessing:%s" % event.pathname)
        if event.pathname in self.__access:
            print "SENDING EMAIL"
            string=self.__message_string % (event.pathname,"access",self.__ip,time.ctime())
            if get_email_tool():
                emailtool.send_text(message=string,subject='File access')

    def process_IN_OPEN(self,event):
        self.__log.warning("Openning:%s" % event.pathname)

    def process_IN_MODIFY(self,event):
        self.__log.warning("Modifing:%s" % event.pathname)
        string=self.__message_string % (event.pathname,"changed",self.__ip,time.ctime())
        if event.pathname not in self.__whitelist:
            if get_email_tool():
                emialtool.send_text(message=string,subject='Important file modified')

    def process_IN_ATTRIB(self,event):
        self.__log.warning("Changing attribute:%s" % event.pathname)

    def process_IN_CLOSE_WRITE(self,event):
        self.__log.warning("Close file with writing:%s" % event.pathname)
        string=self.__message_string % (event.pathname,"changed",self.__ip,time.ctime())
        if event.pathname not in self.__whitelist:
            if get_email_tool():
                emailtool.send_text(message=string,subject='Important file delete at %s' % self.__ip)

    def process_IN_CLOSE_NOWRITE(self,event):
        self.__log.warning("Close file without writing:%s" % event.pathname)

    def process_IN_MOVED_TO(self,event):
        self.__log.warning("Move to :%s" % event.pathname)

    def process_IN_MOVED_FROM(self,event):
        self.__log.warning("Move from:%s" % event.pathname)

class MonitorFile():
    '''
    Class of handle config json file
    :date:2017-06-20
    '''
    def __init__(self,configfile):
        if not os.path.exists(configfile):
            print("ConfigFile not exists")
            sys.exit(-1)
        try:
            with open(configfile,'rb') as f:
                self.__config=json.load(f)
        except ValueError,e:
            print("Config file is not a json file")
            sys.exit(-1)

    def get_tomcat_files(self):
        '''
        Get monitor tomcat files from json file
        :param:None
        :return:return the list of monitor tomcat files,exclude tomcat\'s work,log,temp folder
        :date:2017-06-20
        '''
        tomcat_list=self.__config.get('monitor-tomcats')
        tomcat_files=[]
        for tl in tomcat_list.get('tomcat-dirs'):
            tl=os.path.expandvars(tl)
            if os.path.exists(tl):
                temp_list=os.listdir(tl)
                if temp_list.count('logs'):
                    temp_list.remove('logs')
                if temp_list.count('temp'):
                    temp_list.remove('temp')
                if temp_list.count('work'):
                    temp_list.remove('work')
                tomcat_files.append([os.path.join(tl,templ) for templ in temp_list])
        return (tomcat_files,tomcat_list.get("white-list"))

    def get_file(self,config_name):
        '''
        Get config by the config option name
        :return:return the result which configed in the config file,return None if no config option
        :param:config_name ,the config option name
        :date:2017-06-26
        '''
        result=self.__config.get(config_name)
        if isinstance(result,list):
            temp_result=[]
            for r in result:
                temp_result.append(os.path.expandvars(r))
            return temp_result
        elif isinstance(result,dict):
            temp_result=dict()
            for k,v in result.iteritems():
                tv=[]
                for vv in v:
                    tv.append(os.path.expandvars(vv))
                temp_result[k]=tv
        else:
            temp_result=None

        return temp_result


    def get_monitor_files(self):
        '''
        Get monitor files from config json file
        :return: return a list of monitor files,return None if "monitor-files" not configed
        :date:2017-06-20
        '''
        return self.__config.get('monitor-files')

    def get_monitor_folders(self):
        '''
        Get monitor folder from config json file
        :return:return a list of monitor folder,return None if "monitor-folders" not configed
        :date:2017-06-20
        '''
        return self.__config.get('monitor-folders')


def get_ip():
    '''
    Get the ip address
    '''
    ip=socket.gethostbyname(socket.gethostname())
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',56895))
        ip=s.getsockname()[0]
    finally:
        s.close()
    return ip


def is_filechange_ok(file_name):
    '''
    Check the jsp file,return True if the file legal,False if the file change illegal
    '''
    if os.path.exists(file_name):
        regx=get_regx()
        with open(file_name,'rb') as f:
            for line in f:
                if regx.match(line):
                    print("The illegal String is: %s" % line)
                    return False
    return True


def get_config_file(configfile):
    '''
    Get config file location
    '''
    lib_dir=os.path.dirname(os.path.abspath(__file__))
    config_dir=os.path.join(os.path.dirname(lib_dir),os.path.join('config/',configfile))
    if not os.path.exists(config_dir):
        print("Config file %s not exists" % config_dir)
        return None
        #sys.exit(-1)
    return config_dir

def get_key_words():
    '''
    Get jsp key words
    '''
    global key_words
    key_configfile=get_config_file('keywords.json')
    if key_configfile:
        with open(key_configfile,'rb') as f:
            key_list=json.load(f)
        key_words='|'.join(key_list.get('tomcat-keywords'))
    return key_words

def get_regx():
    '''
    Get the regx
    '''
    global regx
    if regx:
        return regx
    if not key_words:
        get_key_words()
    temp=".*(%s).*" % key_words
    regx=re.compile(temp)
    print("The regx is %s " % temp)
    return regx

def get_email_tool():
    '''
    Get email tool class
    '''
    global emailtool
    if not emailtool:
        email_config=get_config_file('config.json')
        if email_config:
            with open(email_config,'rb') as f:
                email_data=json.load(f).get('email')
            emailtool=EmailTool(email_data.get('host'),email_data.get('sender'),email_data.get('password'),\
                                email_data.get('receiver'),email_data.get('port'))
        else:
            print('Email config file illegal')
            sys.exit(-1)
    return emailtool


def tomcat_monitor():
    '''
    The method to test the function
    '''

    m=MonitorFile(get_config_file('monitor.json'))
    tomcathandler=TomcatEventHandler(whitelist=m.get_tomcat_files()[1])
    wm=pyinotify.WatchManager()
    tomcat_notifier=pyinotify.ThreadedNotifier(wm,tomcathandler)
    for t in m.get_tomcat_files()[0]:
        print(t)
        wm.add_watch(t,pyinotify.ALL_EVENTS,rec=True,auto_add=True)
    tomcat_notifier.setDaemon(False)
    tomcat_notifier.start()


    '''
    me=get_monitor_and_exclude()
    print me[0],me[1]
    start_monitor(me[0],me[1])
    '''

def system_monitor():
    '''
    Monitor file except tomcat
    '''
    #global s_monitors
    m=MonitorFile(get_config_file('monitor.json'))
    s_monitors=m.get_file('s-monitor-files')
    monitors=m.get_file('monitor-files')
    monitors+=m.get_file('monitor-folders').get('dirs')
    #print monitors
    wm=pyinotify.WatchManager()
    if s_monitors:
        handler=EventHandler(create=s_monitors.get('m-create'),open=s_monitors.get('m-open'),\
                            delete=s_monitors.get('m-delete'),access=s_monitors.get('m-access'),\
                            modify=s_monitors.get('m-modify'),change=s_monitors.get('m-change'),whitelist=m.get_file('monitor-folders').get('white-list'))
        print list(s_monitors.itervalues())
        s_list=[]
        for sm in s_monitors.itervalues():
            for s in sm:
                s_list.append(s)
        print s_list
        wm.add_watch(s_list,pyinotify.ALL_EVENTS,rec=True)
    else:
        handler=EventHandler([],[],[],[],[],[],whitelist=m.get_file('monitor-folders').get('white-list'))
    notifier=pyinotify.ThreadedNotifier(wm,handler)
    wm.add_watch(monitors,pyinotify.ALL_EVENTS,rec=True)
    notifier.setDaemon(False)
    notifier.start()

#monitor_system()
#test()

