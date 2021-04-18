from InductiveLearningWithCategoricalData import readData
from math import log


null=-999
class tree:
    def __init__(self):
        self.parent=null
        self.left=null
        self.right=null
        self.data=null
        self.name=null
        
    def rightSearch(self):
        if self.left==null and self.right==null:
            print(self.name)
        else:
            print(self.name)
            self.left.rightSearch()
            self.right.rightSearch()
    def bfs(self):
        if self.left==null and self.left==null:
            print(self.name,'  : leaf Node')
        else:
            print(self.name)
            self.left.bfs()
            self.right.bfs()
    
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

def calcInfGain(subset,index):
    InfGain=targetEntropy(subset)+((-1)*Count(subset,index,'yes')/(len(subset)-1))*attEntropy(subset,index,'yes')+((-1)*Count(subset,index,'no')/(len(subset)-1))*attEntropy(subset,index,'no')
    return InfGain
    
def rootNodeIndex(subset):
    l=[]
    index=0
    for i in range(len(subset[0])-1):
        l.append(calcInfGain(subset,i))
    maxi=l[0]
    for i in range(len(l)):
        if maxi<l[i]:
            maxi=l[i]
            index=i
    return index
        
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
    
    
    
    
def DecisionTreeLearn(attributes,node):
    if targetEntropy(node.data)==0 or len(node.data[0])==1:
        node.name=node.data[1][-1]
        return
    info=[x[:] for x in node.data]
    info_copy=[x[:] for x in info]
    index=rootNodeIndex(info)
    node.name=info[0][index]
    right=[]
    left=[]
    right=extractor(info,index,'yes')
    left=extractor(info_copy,index,'no')
    node.right=tree()
    node.right.parent=node
    node.right.data=right
    node.left=tree()
    node.left.parent=node
    node.left.data=left
    DecisionTreeLearn(attributes,node.left)
    DecisionTreeLearn(attributes,node.right)
    
fileName='train.txt'
attributeNames,data=readData(fileName)
start=tree()
data.insert(0,attributeNames)
start.data=data
DecisionTreeLearn(attributeNames,start)
start.bfs()