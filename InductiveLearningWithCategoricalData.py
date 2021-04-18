'''
 Documentation:-
 ----------------
1. Create a seperate file for training sets that should be in a csv format.
2. Put 'eof' at the end of the read file.
3. Target attribute should always be the last attribute.
4. Data elements should always be either 'yes' or 'no'.This rule doesnot apply to the attribute names.

'''

def learn(att,data):
    yesCount=0
    noCount=0
    gen=[0]*len(att)
    spec=[0]*len(att)
    for i in range(len(data)):
        if data[i][-1]=='yes':
            yesCount=yesCount+1
            for j in range(len(spec)):
                if data[i][j]=='yes':
                    spec[j]=spec[j]+1
        elif data[i][-1]=='no':
            noCount=noCount+1
            for j in range(len(gen)):
                if data[i][j]=='yes':
                    gen[j]=gen[j]+1
    for i in range(len(gen)):
        gen[i]=[att[i],(gen[i]/noCount)]
        spec[i]=[att[i],(spec[i]/yesCount)]
    final=[0]*len(gen)
    for i in range(len(gen)):
        final[i]=[gen[i][0],(spec[i][1]-gen[i][1])*100]
    final.sort(key=lambda x:x[1],reverse=True)
    final.pop(0)
    return final
        
    

def readData(fileName):
    f=open(fileName,'r')
    temp=f.readline()
    temp=temp[:-1]
    attributeNames=temp.split(',')
    data=[]
    while(1):
        temp=f.readline()
        if ('eof' in temp):
            break;
        temp=temp[:-1]
        list=temp.split(',')
        data.append(list)
    f.close()
    return attributeNames,data
