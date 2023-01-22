import pandas as pd
import openpyxl
import numpy as np
import csv

sentances  = ["i want to make coffee:DA"]
sentances.append("where am i:LR")
sentances.append("what can i do here:AR")
sentances.append("prepare meal:DA")
sentances.append("use refrigerator:DA")
sentances.append("use fan:DA")
sentances.append("use oven:DA")
sentances.append("use stove:DA")
sentances.append("i would like to wash sheets:DA")
sentances.append("i would like to watch television:DA")
sentances.append("wash sheets:DA")
sentances.append("wash clothes:DA")
sentances.append("cook dinner:DA")
sentances.append("i would like to cook dinner:DA")
sentances.append("where is the coffee:DA")
sentances.append("rewind video:REV")
sentances.append("pause video:PV")
sentances.append("skip forward:FFV")
sentances.append("negative:N")
sentances.append("positive:P")
sentances.append("yes:P")
sentances.append("no:N")
sentances.append("hello yes:P")
sentances.append("hello no:N")
sentances.append("shutdown app:SD")
sentances.append("shut:SD")
sentances.append("hello:0")
#sentances.append("play video")
sentances.append("hello shut down app:SD")
sentances.append("hello shut:SD")
#sentances.append("hello play video")
sentances.append("hello negative:N")
sentances.append("hello positive:P")
sentances.append("correct:P")
sentances.append("incorrect:N")
sentances.append("hello correct:P")
sentances.append("hello incorrect:N")
sentances.append("i want to make coffee:DA")
sentances.append("where am i:LR")
sentances.append("start camera:OC")
sentances.append("stop camera:CC")
sentances.append("open camera:OC")
sentances.append("close camera:CC")

sentances.append("hello start camera:OC")
sentances.append("hello stop camera:CC")
sentances.append("hello open camera:OC")
sentances.append("hello close camera:CC")

sentances.append("hello i would like to wash sheets:DA")
sentances.append("hello i would like to watch television:DA")
sentances.append("hello wash sheets:DA")
sentances.append("hello wash clothes:DA")
sentances.append("hello cook dinner:DA")
sentances.append("hello i would like to cook dinner:DA")
sentances.append("hello where is the coffee:DA")
sentances.append("hello rewind video:REV")
sentances.append("hello pause video:PV")
sentances.append("hello skip forward:FFV")

df = pd.read_excel("./Keyword Map NLP.xlsx")
Loc = df.loc[df['Loc']==1]
#print(Loc)
workbook = openpyxl.load_workbook('./Keyword Map NLP.xlsx')
sh = workbook.active
                 
get= []
print("start")
for i in range(1,sh.max_column+1):
    #print(i)
    search = sh.cell(row=1,column=i).value
    #print(search)
    if(search == 'Loc'):
        for j in range(2,sh.max_row+1):
            one = sh.cell(row=j,column=i).value
            if(one == 1):
                #print(sh.cell(row=j,column=1).value)
                get.append(sh.cell(row=j,column=1).value)
        break
                 
for w in get:
    filer = (f"i want to go to the {w}:NAV")
    sentances.append(filer)

for w in get:
    filer = (f"navigate to {w}:NAV")
    sentances.append(filer)

fields  = ["description","category"]
with open('text_train.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)  
    csvwriter.writerow(fields) 
    rows = []
    for data in sentances:
    # creating a csv writer object 
        
        
    # writing the fields 

        rows.append(data.split(":")) 
    # writing the data rows 
    #print(rows)
    csvwriter.writerows(rows)

with open('text_test.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)  
    csvwriter.writerow(fields) 
    rows = []
    for data in sentances:
    # creating a csv writer object 
        
        
    # writing the fields 

        rows.append(data.split(":")) 
    # writing the data rows 
    #print(rows)
    csvwriter.writerows(rows)