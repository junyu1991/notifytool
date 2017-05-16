#!/usr/bin/env python
#!encoding:utf-8
#date:2017-05-08

from lib import tools

def test():
    result=tools.get_target_files('~/work/python/mytool/notify/config/target_file.xml')
    for r in result:
        tools.log(r,tools.ERROR)


if __name__=='__main__':
    test()
