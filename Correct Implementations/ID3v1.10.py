'''
Documentation:
---------------

Version 1.8:-
                1)Added support for multi class classification.
                2)Now other than file name input , all other inputs can have predecided default values and you can just press ENTER on them to skip them.



'''
from math import log



fileName=input('Enter the file path: ')
null=-999
l=[]


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
            if self.parent!=null:
                print('Tree Depth ',self.depth,' : ',self.semiVariable,'->',self.name,' [',end=' ')
            else:
                print('Tree Depth ',self.depth,' : ',self.name,' [',end=' ')
                
            for i in range(len(self.children)):
                print(self.children[i].semiVariable,'->',self.children[i].name,end=', ')
            print(']')
            for i in range(len(self.children)):
                self.children[i].bfs()
                
            
            
            
            

e=lambda a,b:(-1)*(a/(a+b))*log(a/(a+b))+(-1)*(b/(a+b))*log(b/(a+b))

def targetCount(subset,targetIndex,targetLabels):  #gets the count of positive and negative of target attribute
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
    for i in range(1,len(subset)):
        if subset[i][index]==pattern:
           count=count+1
    return count


def attValueCount(subset,index,value,targetIndex,targetLabels):
    pos=0
    neg=0
    for i in range(len(subset)):
        if subset[i][index]==value and subset[i][targetIndex]==targetLabels[0]:
            pos=pos+1
        elif subset[i][index]==value and subset[i][targetIndex]==targetLabels[1]:
            neg=neg+1
    return pos,neg
    
def targetEntropy(subset,targetIndex,targetLabels):
    pos,neg=targetCount(subset,targetIndex,targetLabels)
    posProb=0
    negProb=0
    if pos==0:
        return 0
    elif neg==0:
        return 0
    entropy=-((pos)/(neg+pos))*log((pos)/(neg+pos))-((neg)/(neg+pos))*log((neg)/(neg+pos))
    return entropy    

def attEntropy(subset,index,pattern,targetIndex,targetLabels):
    temp=attValueCount(subset,index,pattern,targetIndex,targetLabels)
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

def calcInfGain(subset,index,targetIndex,targetLabels):
    sum=0
    un=getVariety(subset,index)
    for i in range(len(un)):
        sum=sum+((-1)*Count(subset,index,un[i])/(len(subset)-1))*attEntropy(subset,index,un[i],targetIndex,targetLabels)
    
    InfGain=targetEntropy(subset,targetIndex,targetLabels)+sum
    return InfGain
    
def rootNodeIndex(subset,targetIndex,targetLabels):
    l=[]
    index=0
    for i in range(len(subset[0])):
        if i!=targetIndex:
            temp=[calcInfGain(subset,i,targetIndex,targetLabels),i]
            l.append(temp)
    try:    
        maxi=l[0][0]
    except:
        print("\nCan't find a better model.Try adding more attributes.")
        input()
        exit()
        
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
    
    
def DecisionTreeLearn(attributes,node,stopper,targetIndex,targetLabels):
    if targetEntropy(node.data,targetIndex,targetLabels)==0 or (node.depth>=stopper and stopper>0):
        try:
            y=Count(node.data,targetIndex,targetLabels[0])
            n=Count(node.data,targetIndex,targetLabels[1])
        except:
           print("\nCan't find a better model.Try adding more attributes.Error in DecisionTreeLearn().")
           input()
           exit()
           
        if y>n:
            node.name=targetLabels[0]+' (Accuracy : '+str((y*100)/(y+n))+'%) '
        elif y==n:
            node.name="Can't Decide! "
        else:
            node.name=targetLabels[1]+' (Accuracy : '+str((n*100)/(y+n))+'%) '
   
        node.final=1
        return
    info=[x[:] for x in node.data]
    index=rootNodeIndex(info,targetIndex,targetLabels)
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
        DecisionTreeLearn(attributes,node.children[i],stopper,targetIndex,targetLabels)
    node.data=0
        
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

def readData(fileName,delim,skip=200,end=100):
    f=open(fileName,'r')
    temp=f.readline()
    temp=temp[:-1]
    data=[]
    attributeNames=temp.split(delim)
    for line in f:
        if skip==0:
            if ('eof' in line):
                break;
            line=line[:-1]
            list=line.split(delim)
            data.append(list)
            break
        skip=skip-1
        
    while(end!=0):
        temp=f.readline()
        if ('eof' in temp):
            break;
        temp=temp[:-1]
        list=temp.split(delim)
        data.append(list)
        end=end-1

    f.close()
    return attributeNames,data
    
    
def cleaner(subset,dc):
    if dc!=['']:
        for idx in dc:
            if '-' in idx:
                idx.strip()
                sexp=0
                snum=0
                for i in range(len(idx)-1,-1,-1):
                    if idx[i]=='-':
                        break
                    else:
                        snum=snum+int(idx[i])*(10**sexp)
                        sexp=sexp+1
                fexp=0
                fnum=0
                for j in range(i-1,-1,-1):
                    if idx[j]=='-':
                        break
                    else:
                        fnum=fnum+int(idx[j])*(10**fexp)
                        fexp=fexp+1
                        
                dc=dc+list(range(fnum,snum+1))
        
        i=0
        while i<len(dc):
            if isinstance(dc[i],str) and  '-' in dc[i]:
                dc.pop(i)
                i=i-1
            i=i+1
            
            
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
        
def beautify(subset):
    for i in range(len(subset)):
        for j in range(len(subset[i])):
            print(subset[i][j],end=1*' ')
        print()




        
    
def multiClassifier(classes,attributes,subset,maxDepth,targetIndex):
    copy=tuple(tuple(x) for x in subset)
    targetIndexCopy=targetIndex
    objects=[0]*len(classes)
    for i in range(len(classes)):
        subset=list(list(x) for x in copy)
        targetIndex=targetIndexCopy
        for j in range(len(subset)):
            if classes[i]==subset[j][targetIndex]:
                subset[j].append(classes[i])
                subset[j].pop(targetIndex)
            elif j!=0:
                subset[j].append('Not '+classes[i])
                subset[j].pop(targetIndex)
            elif j==0:
                subset[j].append(classes[i])
                subset[j].pop(targetIndex)
                
        targetIndex=len(subset[0])-1
        objects[i]=tree()
        targetLabels=['Not '+classes[i],classes[i]]
        distinct=[]
        targetIndex=postProcess(subset,attributes,distinct,targetIndex)
        objects[i].data=subset
        DecisionTreeLearn(attributes,objects[i],maxDepth,targetIndex,targetLabels)
        print('Decision Tree for ',classes[i])
        print('--------------------\n\n\n')
        objects[i].bfs()
        print('--------------------\n\n\n')
        #DecisionTreeLearn(attributes,node,stopper,targetIndex,targetLabels)
        
        


delim=input('Enter the delimiter like comma or space etc ; or press ENTER : ') or ','

attributeNames,data=readData(fileName,delim,int(float(input("Enter the no. of data sets to skip ; or press ENTER : ") or 0)),
int(float(input('Enter the no. of training data sets ; or press ENTER : ') or 100)))
data.insert(0,attributeNames)
print('\n\nAttribute Names with Index:')
for i in range(len(attributeNames)):
    print(i,':',attributeNames[i],end=' , ')
dc=input("\nEnter the indexes or index range of attributes that are to be elliminated ; or press ENTER : ").split(',')
cleaner(data,dc)
print('\n\nAttribute Names with Index:')
for i in range(len(data[0])):
    print(i,':',data[0][i],end=' , ')
print('\n\n')
targetIndex=int(input('\nEnter the index of the target attribute ; or press ENTER : ') or len(data[0])-1)
maxDepth=float(input('Enter the max depth ; or press ENTER : ') or -1) 
print()
classes=getVariety(data,targetIndex)
if len(classes)>2:
    multiClassifier(classes,attributeNames,data,maxDepth,targetIndex)
else:
    node=tree()
    distinct=[]
    targetIndex=postProcess(data,attributeNames,distinct,targetIndex)
    node.data=data
    DecisionTreeLearn(attributeNames,node,maxDepth,targetIndex,classes)
    print('Decision Tree for ',data[0][targetIndex])
    print('--------------------\n\n\n')
    node.bfs()
    print('--------------------\n\n\n')
input()