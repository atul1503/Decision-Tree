'''
Documentation:
---------------

Version 1.6:-
                1)Now null or empty value rows will be deleted automatically.
                2)Added the option to delete columns in the name of "Dont't care" attributes.



'''
from math import log


fileName=input('Enter the file path: ')
null=-999

class tree:
    def __init__(self):
        self.parent=null
        self.semiVariable=null
        self.children=null
        self.data=null
        self.name=null
        self.final=null
        self.depth=0
                    
    def bfs(self):
        if self.final!=1:
            print('Tree Depth: ',self.depth,' : ',self.name,' [',end=' ')
            for i in range(len(self.children)):
                print(self.children[i].semiVariable,'->',self.children[i].name,end=', ')
            print(']')
            for i in range(len(self.children)):
                self.children[i].bfs()

e=lambda a,b:(-1)*(a/(a+b))*log(a/(a+b))+(-1)*(b/(a+b))*log(b/(a+b))

def targetCount(subset,targetIndex):  #gets the count of positive and negative of target attribute
    pos=0
    neg=0
    for i in range(1,len(subset)):
        if subset[i][targetIndex]==targetLabels[0]:
            pos=pos+1
        elif subset[i][targetIndex]==targetLabels[1]:
            neg=neg+1
    return pos,neg

def Count(subset,index,pattern):
    count=0
    for i in range(len(subset)):
        if subset[i][index]==pattern:
           count=count+1
    return count


def attValueCount(subset,index,value,targetIndex):
    pos=0
    neg=0
    for i in range(len(subset)):
        if subset[i][index]==value and subset[i][targetIndex]==targetLabels[0]:
            pos=pos+1
        elif subset[i][index]==value and subset[i][targetIndex]==targetLabels[1]:
            neg=neg+1
    return pos,neg
    
def targetEntropy(subset,targetIndex):
    pos,neg=targetCount(subset,targetIndex)
    posProb=0
    negProb=0
    if pos==0:
        return 0
    elif neg==0:
        return 0
    entropy=-((pos)/(neg+pos))*log((pos)/(neg+pos))-((neg)/(neg+pos))*log((neg)/(neg+pos))
    return entropy    

def attEntropy(subset,index,pattern,targetIndex):
    temp=attValueCount(subset,index,pattern,targetIndex)
    if temp[0]==0 or temp[1]==0:
        return 0
    entropy=e(temp[0],temp[1])
    return entropy

def getVariety(subset,index):
    un=[]
    for i in range(1,len(subset)):
        if subset[i][index] not in un:
            un.append(subset[i][index])
    return un

def calcInfGain(subset,index,targetIndex):
    sum=0
    un=getVariety(subset,index)
    for i in range(len(un)):
        sum=sum+((-1)*Count(subset,index,un[i])/(len(subset)-1))*attEntropy(subset,index,un[i],targetIndex)
    
    InfGain=targetEntropy(subset,targetIndex)+sum
    return InfGain
    
def rootNodeIndex(subset,targetIndex):
    l=[]
    index=0
    for i in range(len(subset[0])):
        if i!=targetIndex:
            temp=[calcInfGain(subset,i,targetIndex),i]
            l.append(temp)
    try:    
        maxi=l[0][0]
    except:
        print("\nCan't find a better model.Try adding more attributes.")
        input()
        quit()
    for i in range(len(l)):
        if maxi<l[i][0]:
            maxi=l[i][0]
            index=l[i][1]
        elif maxi==l[i][0]:
            index=l[i][1]
    return index
    
def getDuplicates(subset,count):
    duplicate=[]
    for i in range(count):
        duplicate.append([x[:] for x in subset])
    return duplicate
        
def extractor(subset,index,value):
    temp=subset[0]
    temp.pop(index)
    l=[]
    l.append(temp)
    for i in range(len(subset)):
        if i!=0:
            if subset[i][index]==value:
                temp=subset[i]
                temp.pop(index)
                l.append(temp)
    return l    
    
    
def DecisionTreeLearn(attributes,node,stopper,targetIndex):
    if targetEntropy(node.data,targetIndex)==0 or node.depth>=stopper:
        y=Count(node.data,targetIndex,targetLabels[0])
        n=Count(node.data,targetIndex,targetLabels[1])
        if y>n:
            node.name=targetLabels[0]+' (Accuracy : '+str((y*100)/(y+n))+'%) '
        elif y==n:
            node.name="Can't Decide! "
        else:
            node.name=targetLabels[1]+' (Accuracy : '+str((n*100)/(y+n))+'%) '
   
        node.final=1
        return
    info=[x[:] for x in node.data]
    index=rootNodeIndex(info,targetIndex)
    node.name=info[0][index]
    uni=getVariety(info,index)
    depth=node.depth
    workSet=getDuplicates(info,len(uni))
    child=[0]*len(uni)
    for i in range(len(uni)):
        child[i]=extractor(workSet[i],index,uni[i])
    if index<targetIndex:
        targetIndex=targetIndex-1
    node.children=[0]*len(child)
    for i in range(len(child)):
        node.children[i]=tree()
        node.children[i].semiVariable=uni[i]
        node.children[i].parent=node
        node.children[i].depth=depth+1
        node.children[i].data=child[i]
        DecisionTreeLearn(attributes,node.children[i],stopper,targetIndex)
        
def isNum(subset,index):
        try:
            temp=0
            temp=temp+float(subset[1][index])
            return 1
        except:
            return 0
        
def postProcess(subset,attributes,distinct,targetIndex):
    i=0
    while i<len(subset[0]):
        if i!=targetIndex:
            if isNum(subset,i):
                for j in range(1,len(subset)):
                    if float(subset[j][i]) not in distinct:
                        key=float(subset[j][i])
                        distinct.append(key)
                        subset[0].insert(len(subset[0]),' Is '+subset[0][i]+">="+str(key)+' ? ')
                        for k in range(1,len(subset)):
                            if float(subset[k][i])<key:
                                subset[k].insert(len(subset[k]),'no')
                            else:
                                subset[k].insert(len(subset[k]),'yes')
        i=i+1
        
    rem=[]
    man=0
    for i in range(len(subset[0])):
        if isNum(subset,i)==1 and i!=targetIndex:
            rem.append(i)
    for i in rem:
        if  i<targetIndex:
            man=man+1
    targetIndex=targetIndex-man
    for i in range(len(subset)):
        sub=0
        for j in range(len(rem)):
            subset[i].pop(rem[j]-sub)
            sub=sub+1
    return targetIndex

def readData(fileName,delim):
    f=open(fileName,'r')
    temp=f.readline()
    temp=temp[:-1]
    attributeNames=temp.split(delim)
    data=[]
    while(1):
        temp=f.readline()
        if ('eof' in temp):
            break;
        temp=temp[:-1]
        list=temp.split(delim)
        data.append(list)
    f.close()
    return attributeNames,data
    
    
def cleaner(subset,dc):
    if dc !=['']:
        for i in range(len(dc)):
            dc[i]=int(dc[i])
        
        dc.sort()
    
        for i in range(len(dc)):
            dc[i]=dc[i]-i
        
        for i in range(len(subset)):
            for  j in dc:
                subset[i].pop(j)
        
    l=[]
    i=0
    while i<len(subset):
        j=0
        while j<len(subset[0]):
            if subset[i][j]=='' and i not in l:
                l.append(i)
            j=j+1
        i=i+1
        
    for i in range(len(l)):
        l[i]=l[i]-i
    for i in l:
        subset.pop(i)
    




delim=input('Enter the delimiter like comma or space etc. :') or ','
attributeNames,data=readData(fileName,delim)
data.insert(0,attributeNames)
print('\n\nAttribute Names with Index:')
for i in range(len(attributeNames)):
    print(i,':',attributeNames[i],end=' , ')
dc=input("\nEnter the indexes of all don't care attributes ,those attributes will be removed . If you donot wish to then press enter:").split(',')
cleaner(data,dc)
print('\n\nAttribute Names with Index:')
for i in range(len(data[0])):
    print(i,':',data[0][i],end=' , ')
print('\n\n')
targetIndex=int(input('\nEnter the index of the target attribute.Use 0 indexing : '))
global targetLabels
targetLabels=getVariety(data,targetIndex)
start=tree()
distinct=[]
targetIndex=postProcess(data,attributeNames,distinct,targetIndex)
start.data=data
maxDepth=float(input('Enter the max depth:'))
DecisionTreeLearn(attributeNames,start,maxDepth,targetIndex)
print('\n\n\n--------------------\n\n\n')
start.bfs()
input('\n\n\n--------------------\n\n\n')