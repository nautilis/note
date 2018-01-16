#!/usr/bin/python
import os
import time

'''
make a new md file which under the category diretory
'''
category = raw_input("which category is the new note?\r\n").strip()

if not os.path.exists("./{}".format(category)):
    os.mkdir(category) 

filename = raw_input("What's the filename?\r\n")

localtime = time.localtime(time.time())
date = time.strftime("%Y%m%d", localtime)
filename_with_time = "./{}/{}_{}.md".format(category, date, filename)

if not os.path.isfile(filename_with_time):
    command = "touch {}".format(filename_with_time)
    os.system(command)

open_it = "vim {}".format(filename_with_time) 
os.system(open_it)
exit()
