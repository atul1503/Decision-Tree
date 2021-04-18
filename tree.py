""" 
Documentation
--------------
Thankyou for your curiosity to know more about this file :)
This is a Python program for implementing a Tree Data Structure which can 1)insert 2)do depth first search traversal 3)What?You want more?
This is a prototype as you can see that the input is pretty minimal and can be made more interactive by using more runtime input as well.
But the author is really using this as practice for Decision Trees which he was unable to implement because of certain factors,but thats okay because sometimes things may not go your way but still you can try it again.

About the future of this file
-----------------------------
The file will be used as package for decision tree projects and so I may implement bfs and other traversal methods as well or other functions that may seem necessary.

"""
null=0
class tree:
    def __init__(self):
        self.parent=null
        self.left=null
        self.right=null
        self.data=null
    def backtrack(self):
        if self.parent==null:
            print(self.data)
            return
        print(self.data)
        self.parent.backtrack()
    def dfs(self,target):
        if self.data==target:
            print('Node found ! The path is :')
            self.backtrack()
        elif self.data>target:
            self.left.dfs(target)
        else:
            self.right.dfs(target)
    def insert(self,node):
        if node==null:
            print('Insert anything but null')
            return
        if self.data>node:
            if self.left==null:
                self.left=tree()
                self.left.parent=self
                self.left.data=node
                print('Node Inserted')
                return
            self.left.insert(node)
            print('Node Inserted')
        elif self.data<node:
            if self.right==null:
                self.right=tree()
                self.right.parent=self
                self.right.data=node
                print('Node Inserted')
                return
            self.right.insert(node)
            print('Node Inserted')
        else:
            print('Node is already present')
            return
        
            
       