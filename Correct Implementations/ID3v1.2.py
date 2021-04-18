'''
Documentation:
---------------

Version 1.2:-
                1)Added Support for numerical values for the predictor attributes.


Precautions:
------------
Interpretation may be difficult but remember any attribute name that comes inside the brackets is a branch node and the real meaning can be understood only when traversed till the leaf node.
For example if the data is:


score,win
135,yes
148,no
185,yes
eof


the output is:

score>=148.0 [ no -> yes, yes -> score>=185.0, ]
score>=185.0 [ no -> no, yes -> yes, ]

the string "yes-> score>=185.0" inside the first bracket can be interpreted as "if current node's verdict is yes then the next verdict depends on the branch node "score>=185.0" and not meant to be taken literally.



'''
from math import log


fileName=input('Enter the input file path if in another directory,else just enter the name: ')
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
            print(self.name,'[',end=' ')
            for i in range(len(self.children)):
                print(self.children[i].semiVariable,'->',self.children[i].name,end=', ')
            print(']')
            for i in range(len(self.children)):
                self.children[i].bfs()

e=lambda a,b:(-1)*(a/(a+b))*log(a/(a+b))+(-1)*(b/(a+b))*log(b/(a+b))

def targetCount(subset):  #gets the count of positive and negative of target attribute
    pos=0
    neg=0
    for i in range(len(subset)):
        if subset[i][-1]=='yes':
            pos=pos+1
        elif subset[i][-1]=='no':
            neg=neg+1
    return pos,neg

def Count(subset,index,pattern):
    count=0
    for i in range(len(subset)):
        if subset[i][index]==pattern:
           count=count+1
    return count


def attValueCount(subset,index,value):
    pos=0
    neg=0
    for i in range(len(subset)):
        if subset[i][index]==value and subset[i][-1]=='yes':
            pos=pos+1
        elif subset[i][index]==value and subset[i][-1]=='no':
            neg=neg+1
    return pos,neg
    
def targetEntropy(subset):
    pos,neg=targetCount(subset)
    posProb=0
    negProb=0
    if pos==0:
        return 0
    elif neg==0:
        return 0
    entropy=-((pos)/(neg+pos))*log((pos)/(neg+pos))-((neg)/(neg+pos))*log((neg)/(neg+pos))
    return entropy    

def attEntropy(subset,index,pattern):
    temp=attValueCount(subset,index,pattern)
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

def calcInfGain(subset,index):
    sum=0
    un=getVariety(subset,index)
    for i in range(len(un)):
        sum=sum+((-1)*Count(subset,index,un[i])/(len(subset)-1))*attEntropy(subset,index,un[i])
    
    InfGain=targetEntropy(subset)+sum
    return InfGain
    
def rootNodeIndex(subset):
    l=[]
    index=0
    for i in range(len(subset[0])-1):
        l.append(calcInfGain(subset,i))
    try:
        maxi=l[0]
    except:
        print("Can't find a better model.Try adding more attributes.")
        input()
        quit()
        
    for i in range(len(l)):
        if maxi<l[i]:
            maxi=l[i]
            index=i
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
        if subset[i][index]==value:
            temp=subset[i]
            temp.pop(index)
            l.append(temp)
    return l    
    
    
def DecisionTreeLearn(attributes,node,stopper):
    if targetEntropy(node.data)==0 or node.depth>=stopper:
        if Count(node.data,-1,'yes')>Count(node.data,-1,'no'):
            node.name='yes'
        elif Count(node.data,-1,'yes')==Count(node.data,-1,'no'):
            node.name="Can't Decide! "
        else:
            node.name='no'
   
        node.final=1
        return
    info=[x[:] for x in node.data]
    index=rootNodeIndex(info)
    node.name=info[0][index]
    uni=getVariety(info,index)
    depth=node.depth
    workSet=getDuplicates(info,len(uni))
    child=[0]*len(uni)
    for i in range(len(uni)):
        child[i]=extractor(workSet[i],index,uni[i])
    node.children=[0]*len(child)
    for i in range(len(child)):
        node.children[i]=tree()
        node.children[i].semiVariable=uni[i]
        node.children[i].parent=node
        node.children[i].depth=depth+1
        node.children[i].data=child[i]
        DecisionTreeLearn(attributes,node.children[i],stopper)
        
def isNum(subset,index):
        try:
            temp=0
            temp=temp+float(subset[1][index])
            return 1
        except:
            return 0
        
def postProcess(subset,attributes,distinct):
    i=0
    while i<len(subset[0]):
        if isNum(subset,i):
            for j in range(1,len(subset)):
                if float(subset[j][i]) not in distinct:
                    key=float(subset[j][i])
                    distinct.append(key)
                    subset[0].insert(-1,'Is '+subset[0][i]+">="+str(key)+' ? ')
                    for k in range(1,len(subset)):
                        if float(subset[k][i])<key:
                            subset[k].insert(-1,'no')
                        else:
                            subset[k].insert(-1,'yes')
        i=i+1
    
    rem=[]
    for i in range(len(subset[0])):
        if isNum(subset,i):
            rem.append(i)
    for i in range(len(subset)):
        sub=0
        for j in rem:
            subset[i].pop(j-sub)
            sub=sub+1
        
            
                
                



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



attributeNames,data=readData(fileName)
start=tree()
data.insert(0,attributeNames)
distinct=[]
postProcess(data,attributeNames,distinct)
start.data=data
maxDepth=float(input('Enter the max depth:'))
DecisionTreeLearn(attributeNames,start,maxDepth)
print('\n\n\n-----------------\n\n\n')
start.bfs()
print('\n\n\n-----------------\n\n\n')
input()