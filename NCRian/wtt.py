import requests
from json2html import *
import json

response = requests.get("https://samples.openweathermap.org/data/2.5/forecast?zip=30309&appid=b6907d289e10d714a6e88b30761fae22")
a = response.json()
b = a.get("list")
outer = []
for i in range (len(b)):
    outer.append((b[i].get("weather")[0].get("description")))
    outer.append(((b[i].get("wind")).get("speed")))
    outer.append(round((((b[i].get("main")).get("temp_max"))-273.15)*9 /5 ) + 32)
    

print(outer,len(outer))


##for i in range (len(b)):
##    for ii in range (len(i)):
##        outer.append()
        
    
