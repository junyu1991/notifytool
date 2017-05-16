#!/usr/bin/env python
#!encoding:utf-8
#date:2017-05-08

import os
import time
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from target import target_file

WARN='WARNING'
ERROR='FAIL'
INFO="ENDC"

def get_target_files(config_file='../config/target_file.xml'):
    '''
    Get the monitor file from config xml file
    param:config file
    return:return monitor file list
    date:2017-05-08
    author:yujun
    '''
    if not os.path.exists(config_file):
        log("File %s not exists"%(config_file),ERROR)
        return []
    log("Parsing file %s" % (config_file))
    target_files=[]
    try:
        target_xml=ET.ElementTree(file=config_file)
        root=target_xml.getroot()
        if root.tag == 'target-files':
            for child in root:
                file_path=''
                file_ext=''
                exclude=''
                keywords=''
                level=''
                for c in child:
                    if c.tag=='file-path':
                        file_path=c.text
                    if c.tag=='file-ext':
                        file_ext=c.text
                    if c.tag=='exclude':
                        exclude=c.text
                    if c.tag=='key-words':
                        keywords=c.text
                    if c.tag=='level':
                        level=c.text

                temp=target_file(file_path=file_path,file_ext=file_ext,exclude=exclude,keywords=keywords,level=level)
                target_files.append(temp)
        return target_files
    except Exception,e:
        log("Exception %s" % str(e),ERROR)
        return []


color_dict={'HEADER':'\033[95m','OKBLUE':'\033[94m','OKGREEN':'\033[92m',
            'WARNING':'\033[93m','FAIL':'\033[91m','ENDC':'\033[0m',
            'BOLD':'\033[1m','UNDERLINE':'\033[4m'}

def log(strs,level=INFO,logfile='./log/%s.log'):
    '''
    Log method
    param: strs,string to print;levele,the print level;logfile the log file
    return:None
    '''

    logfile=logfile % time.ctime()
    try:
        strs="[%s] %s" %(time.ctime(),strs)
        color=color_dict[level]
        print(color+strs+color_dict['ENDC'])
    except:
        print(strs)

def send_email():
    pass
