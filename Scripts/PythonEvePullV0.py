# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 15:12:41 2017

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
pagiQnext=""
tags=['id','name','start_time','end_time','owner name','owner id','ticket_uri','maybe_count','attending_count','interested_count','description','city','Location Name','Street','Zip Code']
#Facebook Search Query Field##Results page is the scrape source
events = graph.request('/search?q=Events in '+city+'&type=event&limit=50&access_token='+token)
eventList = events['data']
if events['paging']:    
    pag=events['paging']
    print(json.dumps(pag, indent=4))
while events['paging']['cursors']['after']:
    pagiQnext='/search?q=Events in '+city+'&type=event&limit=50&access_token='+token+'&after='+events['paging']['cursors']['after']
    #In case you'd like to print as a string in JSON format
    #print(json.dumps(eventList, indent=4, sort_keys=True))
    ######Store ID lists from query response to scrape individually from the Events pages#######
    idList=[]
    querylist=""
    querylisarr=[]
    for event in range(len(eventList)):
        idList.append(eventList[event]['id'])
        if event%50==49:
            querylist+=eventList[event]['id']
            querylisarr.append(querylist)
            querylist=""
        elif event==(len(eventList)-1):
            querylist+=eventList[event]['id']
            querylisarr.append(querylist)
        else:
            querylist+=eventList[event]['id']+','
    #print(idList)    
    #for qin in range(len(querylisarr)):
    
    for iter_reqbatch in range(len(querylisarr)):
        dmp=requests.get(url="https://graph.facebook.com/v2.9/?ids="+querylisarr[iter_reqbatch]+"&fields=category,name,owner,attending_count,interested_count,description,end_time,maybe_count,place,updated_time,start_time,ticket_uri&access_token="+token)
        dmp=dmp.json()
        res=json.dumps(dmp, indent=4)       
        #print(res)
        x=json.loads(res)
    ###CSV header definition and extracting and setting to appropriate fields###
        dictemp=OrderedDict()  ##To ensure correct ordering##
        #print(x.keys())
        for even in x.keys():
            try:
                for key in tags:
                    try:
                        if key=="owner name":
                            dictemp[key]=x[even]['owner']['name']
                        elif key=="owner id":
                            dictemp[key]=x[even]['owner']['id']
                        elif key=="city":
                            dictemp[key]=x[even]['place']['location']['city']
                        elif key=="Location Name":
                            dictemp[key]=x[even]['place']['name']
                        elif key=="Street":
                            dictemp[key]=x[even]['place']['location']['street']
                        elif key=="Zip Code":
                            dictemp[key]=x[even]['place']['location']['zip']
                        else:
                            dictemp[key]=x[even][key]
                    except KeyError as e:       ##Handle cases where fields are missing
                        #print(e)  
                        dictemp[key]=" "        ##Set fields to empty
                try:
                    if x[even]['place']['location']['country']=="India":    ##Validation to detect anomalies such as Hyderabad->Pakistan
                        print(dictemp['id'])
                        f.writerow(dictemp.values()) 
                except KeyError as e:  #Handle situations where country is no specified 
                        print(dictemp['id'])
                        f.writerow(dictemp.values())
                        ##Write individual Event to sheet after validating country
            except Exception as p:
                print(p)
                try:
                    dictemp['description']=x[even]['description'].encode(sys.stdout.encoding, errors='replace') #Handle char encoding anomalies#
                    dictemp['name']=x[even]['name'].encode(sys.stdout.encoding, errors='replace')
                    dictemp['owner name']=x[even]['owner']['name'].encode(sys.stdout.encoding, errors='replace')
                except Exception as l:
                    print(l)
                    continue
                try:
                    f.writerow(dictemp.values())        #Write to CSV
                    print(dictemp['id']+"in the catch part")
                except:
                    print("Writing Trouble! Ooops!")
                    continue
        print("Completed batch "+str(iter_reqbatch))
        time.sleep(2)
    with open('asdasd.csv') as f1:                  #Close File
        z = csv.reader(f1, delimiter='\t')
    events = graph.request(pagiQnext)
    eventList = events['data']
    pag=events['paging']
    print(json.dumps(pag, indent=4))
print("While done")