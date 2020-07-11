# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 03:59:38 2020
 
This code labelled for the proposed dataset.
It check on each Trx via API ( Address from and Adress to -->> Scam_From and Scam_to)
"""

import pandas as pd
import requests
        
filename= "Dataset.csv"
df=pd.read_csv(filename)
columns=[]
for col in df.columns:
    columns.append(col)

val_from_address = df['from_address']
val_to_address = df['to_address']


def checkAddress_API(addr):
    url = "https://etherscamdb.info/api/check/"+addr
    payload  = {}
    headers = {}
    attack = False
    categ=''
    response = requests.request("GET", url, headers=headers, data = payload)
    #response= requests.get(url, verify=False)
    response =  response.json() # convert cookies to json format
    result = response['result']
    if ( result == 'blocked'):
        attack = True
        result2= response['entries']
        data2 = result2[0]
        categ = data2['category']
    return attack, categ 
    
from_scam = []
to_scam= []
from_category=[]
to_category=[]

numberTrx=  df.shape[0]
for i in range(numberTrx):
    from_address=val_from_address[i]
    to_address=val_to_address[i]
    print(i)
    isSCam, typeScame = checkAddress_API(from_address) 
    if (isSCam== True):
        from_scam.append(1)
        from_category.append(typeScame)
    else:
        from_scam.append(0)
        from_category.append('null')
   
    # To Address 
    isSCam, typeScame = checkAddress_API(to_address)
    if (isSCam == True):
        to_scam.append(1)
        to_category.append(typeScame)
    else:
        to_scam.append(0)
        to_category.append('null')

        
df['from_scam'] = from_scam
df['to_scam'] = to_scam
df['from_category']=from_category 
df['to_category']=to_category 
df.to_csv(filename,index=False)

