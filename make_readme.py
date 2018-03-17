#! /usr/bin/python
import os
import re
import urllib

dirnames = []
results = [] 
dirs = os.listdir(".")
for dir in dirs:
    if dir[0] == "." or os.path.isfile(dir):
        continue
    dirnames.append(dir)

for dir in dirnames:
    files = os.listdir("./{}/".format(dir))
    result = {dir: files}
    results.append(result)

print results

string = ""
for result in results:
    for key, values in result.iteritems():
        string += "## {}  \r\n".format(key)
        for value in values:
            url = urllib.quote("/{}/{}".format(key, value))
            #string += "- [{}](https://github.com/nautilis/note/blob/master/{}/{})  \r\n".format(value, key, value)
            string += "- [{}]({})  \r\n".format(value, url)

print string

with open ("./readme.md", "w")as f:
    f.write(string)
    



