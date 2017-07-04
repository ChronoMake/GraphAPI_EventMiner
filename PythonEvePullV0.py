# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 12:33:37 2017

@author: Arjun Menon
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 11:20:53 2017

@author: Arjun Menon
"""

#####FACEBOOK PULL EVENTS#####

import requests,facebook
import json,csv,sys
import time
from collections import OrderedDict
token="EAAJ4aC7OZBhUBAJuVIx9iQpSPqGoKK5qnFFm6z0ktU47XlInQhHXki1ZC63FHoerDS9uBTaXEBlpNLz6N7d9ykj24NjggIH0hcn1mKvlBZBZAvv3jgvNRif27ZCGeSUne5x4H2Dolx27UrqgG5NxJRi7kXyGkEHYZD"
graph = facebook.GraphAPI(access_token=token, version = 2.9)
f = csv.writer(open("asdasd.csv", "w",newline=''))
f.writerow(['Event ID','Name','Start_Time','End_Time','Owner Name','Owner ID','Tickets URL','Maybe_Attending','Attending_Count','Interested','Event Description','City','Location Name','Street','Zip Code'])
city='Hyderabad'
tags=['id','name','start_time','end_time','owner name','owner id','ticket_uri','maybe_count','attending_count','interested_count','description','city','Location Name','Street','Zip Code']
#Facebook Search Query Field##Results page is the scrape source
events = graph.request('/search?q=Events in '+city+'&type=event&limit=1000')
eventList = events['data']
#In case you'd like to print as a string in JSON format
#print(json.dumps(eventList, indent=4, sort_keys=True))
######Store ID lists from query response to scrape individually from the Events pages#######
idList=[]
for event in range(len(eventList)):
    idList.append(eventList[event]['id'])
#print(idList)

##print(json.dumps(eventList, indent=4, sort_keys=True)) ##To print out the search list
res=[]
print("ID List generated")          #Notification

for i in range(len(idList)):
    dmp=requests.get(url="https://graph.facebook.com/v2.9/"+idList[i]+"?fields=category%2Cname%2Cowner%2Cattending_count%2Cinterested_count%2Cdescription%2Cend_time%2Cmaybe_count%2Cplace%2Cupdated_time%2Cstart_time%2Cticket_uri&access_token="+token)
    dmp=dmp.json()      ##Store each event's info in Json format in a list
    try:
        if dmp['place']['location']['country']=="India":    ##Validation to detect anomalies such as Hyderabad->Pakistan
            res.append(dmp)
    except KeyError as e:  #Handle situations where country is no specified 
            res.append(dmp)
            #print("Country unavailable at "+dmp['id'])         ##For Testing
res=json.dumps(res, indent=4)       
#print(res)
x=json.loads(res)
###CSV header definition and extracting and setting to appropriate fields###
dictemp=OrderedDict()  ##To ensure correct ordering##
    #print(x.keys())
for even in x:
    try:
        for key in tags:
            try:
                if key=="owner name":
                    dictemp[key]=even['owner']['name']
                elif key=="owner id":
                    dictemp[key]=even['owner']['id']
                elif key=="city":
                    dictemp[key]=even['place']['location']['city']
                elif key=="Location Name":
                    dictemp[key]=even['place']['name']
                elif key=="Street":
                    dictemp[key]=even['place']['location']['street']
                elif key=="Zip Code":
                    dictemp[key]=even['place']['location']['zip']
                else:
                    dictemp[key]=even[key]
            except KeyError as e:       ##Handle cases where fields are missing
                #print(e)  
                dictemp[key]=" "        ##Set fields to empty
        f.writerow(dictemp.values())    ##Write individual Event to sheet
    except Exception as p:
        print(p)
        try:
            dictemp['description']=even['description'].encode(sys.stdout.encoding, errors='replace') #Handle char encoding anomalies#
            dictemp['name']=even['name'].encode(sys.stdout.encoding, errors='replace')
            dictemp['owner name']=x[even]['owner']['name'].encode(sys.stdout.encoding, errors='replace')
        except Exception as l:
            print(l)
            continue
        try:
            f.writerow(dictemp.values())        #Write to CSV
        except:
            continue

with open('asdasd.csv') as f1:                  #Close File
    z = csv.reader(f1, delimiter='\t')