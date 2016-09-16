import re
import urllib

from BeautifulSoup import *


url = 'https://pr4e.dr-chuck.com/tsugi/mod/python-data/data/known_by_Dugald.html '
position=int(raw_input('Enter Position'))
count=int(raw_input('Enter Count'))

#perform the loop "count" times.
for i in range(0,count):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    tags=soup.findAll('a')
    for tag in tags:
        url= tag.get('href')
        tags=soup.findAll('a')
        # if the link does not exist at that position, show error.

        # if the link at that position exist, overwrite it so the next search will use it.
        url = tags[position-1].get('href')
print url