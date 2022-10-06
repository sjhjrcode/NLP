import pandas as pd
import openpyxl
import numpy as np
def sentancebreak(breaking, sh):
    check = True
    broken = breaking.split(' ')
    store = []
    for l in broken:
        check = True
        for i in range(1,sh.max_row+1):
            keyword = sh.cell(row=i,column=1).value
            if(l == keyword):
                print("keyword check")
                for j in range(1,sh.max_column+1):
                   
                    print("one check")
                    one = sh.cell(row=i,column=j).value
                    print(one)
                    if(one == 1):
                        check = False
                        print("store check")
                        store.append(keyword+" 0 0 "+sh.cell(row=1,column=j).value)
                        break
                break
                        

        if(check==True):
            store.append(l+" 0 0 0")

    store.append(". O\n")

    return store


def adding(base, add):
    for k in add:
        base.append(k)
    return base
        
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

sentances = ["-DOCSTART- -X- -X- O\n"]
#file = open("read.txt",'w')

for i in range(1,sh.max_row+1):
    keyword = sh.cell(row=i,column=1).value
    for j in range(1,sh.max_column+1):
        one = sh.cell(row=i,column=j).value
        if(one == 1):
            sentances.append(keyword+" 0 0 "+sh.cell(row=1,column=j).value+"\n")
            break

for w in get:
    filer = (f"I want to go to the {w}")
    temp = sentancebreak(filer,sh)
    adding(sentances,temp)
for w in get:
    filer = (f"Navigate to {w}")
    temp = sentancebreak(filer,sh)
    sentances=adding(sentances,temp)



with open('eng_custom.train', 'w') as file:
      

    file.writelines("% s\n" % data for data in sentances)
