#!/usr/bin/env python
#!encoding:utf-8
#date:2017-05-08

import os
import time
import traceback

import logging,logging.handlers

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
                file_path=[]
                file_ext=dict()
                exclude=''
                level=''
                for c in child:
                    if c.tag=='file-path':
                        file_ext_=[]
                        if c.text:
                            file_ext_=c.text.split('|')
                        file_pre=c.attrib.get('parent')
                        if not file_pre:
                            file_pre=''
                        for fe in file_ext_:
                            file_path.append(os.path.join(file_pre,fe))
                    elif c.tag=='file-ext':
                        file_ext[c.text]=c.attrib.get('key_words')
                    elif c.tag=='exclude':
                        exclude=c.text
                    elif c.tag=='level':
                        level=c.text

                temp=target_file(file_path=file_path,file_ext=file_ext,exclude=exclude,keywords=None,level=level)
                target_files.append(temp)
        return target_files
    except Exception,e:
        traceback.print_exc()
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


class Monitor_Log():
    '''
    The logging wrapper class
    '''

    import logging,logging.handlers

    def __init__(self,logname,logfile,*args):
        pre=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../log/')
        logfilename=os.path.join(pre,logfile)

        self.__logger=logging.getLogger(logname)

        filehandler=logging.handlers.TimedRotatingFileHandler(logfilename,when='midnight',interval=5,backupCount=3,encoding='utf8')
        filehandler.suffix='%Y%m%d_%H%M%S.log'
        filehandler.setLevel(logging.DEBUG)

        fmt_str='%(asctime)s-[%(levelname)s]-%(name)s:%(message)s'
        formatter=logging.Formatter(fmt_str)

        filehandler.setFormatter(formatter)

        self.__logger.addHandler(filehandler)
        self.debug('Init logging tool success')

    def warning(self,message):
        self.__logger.warning(message)

    def debug(self,message):
        self.__logger.debug(message)

    def info(self,message):
        self.__logger.info(message)

    def error(self,message):
        self.__logger.error(message)

    def critical(self,message):
        self.__logger.critical(message)




