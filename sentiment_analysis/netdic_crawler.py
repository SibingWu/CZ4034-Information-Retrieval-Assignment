from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl
import csv
from tkinter import messagebox
import time
import re

string = "<li><span><a href=\"https://www.netlingo.com/word/ff-2.php\">#FF</a></span><div class=\"explain\">Follow Friday</div></li>"

try:
    found = re.search("explain\">(.+?)</div></li>", string).group(1)
    print(found)
except AttributeError:
    pass
right_element = re.search('>(.+?)</div>', string).group(1)
#print(right_element)

#ignore ssl certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

LoopCount = 0
#messagebox.showinfo("Start","Tracker in operation!")
html = urllib.request.urlopen('https://www.netlingo.com/acronyms.php', context=ctx).read() #takes input url
soup = BeautifulSoup(html, 'html.parser') #returns a soup object

# Retrieve all of the anchor tags
tags = soup('li')
ListTags = []
for tag in tags:
    ListTags.append(str(tag))
ListTags = ListTags[107:]
ListTags = ListTags[:-26]

left = []
right = []
for i in ListTags: 
    try: 
        right_element = re.search("explain\">(.+?)</div></li>", i).group(1)
        left_element = re.search('php\">(.+?)</a>', i).group(1)
    except AttributeError:
        pass
        continue
    left.append(left_element)
    right.append(right_element)
print(left[0], right[0])
