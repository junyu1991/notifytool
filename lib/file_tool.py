#!/usr/bin/env python
#!encoding:utf-8
#@date:2017-05-16

import tools

def handle_file_event(event,change_flag=1):
    '''
    Handle file changed
    @param:event the pyinotify event;change_flag the file change flag,default 1(file readed)
            1 file readed,2 file changed,3 file attributed changed,4 file deleted,5 file changed with
            key words showed
    @return:None
    @date:2017-05-18
    @auth:yujun
    '''
 #   target_files=tools.get_target_files()
#    target_path
    pass

def handle_file_changed(event):
    pass

def handle_file_readed(event):
    pass

def handle_file_attrib(event):
    pass

def handle_file_deleted(event):
    pass

def handle_file_key(event):
    pass

