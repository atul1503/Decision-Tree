from math import log


fileName='train.txt'
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
        
    def rightSearch(self):
        if self.left==null and self.right==null:
            print(self.name)
        else:
            print(self.name)
            self.left.rightSearch()
            self.right.rightSearch()
            
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
    maxi=l[0]
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
    
def printData(info,delimiter):
    for i in range(len(data)):
        for j in range(len(data[i])):
            print(data[i][j],end=delimiter*' ')
        print()
    
    
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
start.data=data
maxDepth=float(input('Enter the max depth:'))
DecisionTreeLearn(attributeNames,start,maxDepth)
start.bfs()
input()