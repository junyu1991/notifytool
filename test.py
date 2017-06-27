#!/usr/bin/env python
#!encoding:utf-8
#date:2017-05-08

from lib import tools
from lib import notify_tool

def test():
    #result=tools.get_target_files('/home/yujun/work/python/mytool/notify/config/target_file.xml')
    result=notify_tool.get_monitor_and_exclude()
    tools.log(str(result),tools.WARN)
    for r in result:
        tools.log(r,tools.ERROR)


if __name__=='__main__':
    notify_tool.test()
