# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 16:58:00 2017

@author: Arjun Menon
"""

import re,requests
import json
from bs4 import BeautifulSoup

####THIS CODE ADDS A PARAMETER THAT ALLOWS AN INDENT PARAMETER FOR PRETTIFY#####
orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)
def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))
BeautifulSoup.prettify = prettify


in_wordworld=requests.get(url='https://en.wikipedia.org/wiki/List_of_city_name_changes')
in_wordworld=in_wordworld.text
country=[]
#in_wordworld=in_wordworld.json()
#res=json.dumps(in_wordworld, indent=4)
#print(res)
soup=BeautifulSoup(in_wordworld,'html.parser')
print(soup.prettify())
for link in soup.find_all('span',{"class":"mw-headline"})[:-2]:
    try:
        country_name=link.a.text
        country.append(country_name)
    except AttributeError as e:
        #print("Not Country "+str(e))
        continue
    
for i in soup.find_all('li'):
    test=i.contents
###########################################################################
pars=re.compile(r'\w* → \w+', re.MULTILINE)
for link in soup.find_all('span',{"class":"mw-headline"})[:-2]:
    listnames=[]
    country_name=link.a.text
    h2tag=link.parent
    curr=h2tag.next_sibling
    while(curr.name!='ul'):
        curr=curr.next_sibling  ##Reach <ul> country tags
    curr=str(curr)
    soup2=BeautifulSoup(curr,'html.parser')
    soup2.prettify()
    for city in soup2.find_all('li'):
        city_1=str(city)
        key_city=city.find_all('a')[-1].text
        p=pars.findall(city_1)
        print(p)
        
        
        
        
        
        