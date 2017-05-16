#!/usr/bin/env python
#!encoding:utf-8
#date:2017-05-08

'''The target file class'''

class target_file:

    def __init__(self,file_path,file_ext,exclude,keywords,level):

        self.file_path=file_path
        self.file_ext=file_ext
        self.exclude=exclude
        self.keywords=keywords
        self.level=level

    def __str__(self):
        return "file_path:%s\nfile_ext:%s\nexclude:%s\nkeywords:%s\nlevel:%s" % (str(self.file_path),str(self.file_ext),str(self.exclude),str(self.keywords),str(self.level))
