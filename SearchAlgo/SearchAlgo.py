from flask import Flask,redirect,url_for,render_template,request,jsonify

import random
import datetime
import copy
import time
import json

#Empty array initialized to use across different functions
uniqueArr ,uniqueSorted = [],[]
root=None
RBT=None


app = Flask(__name__)


@app.route('/',methods = ['GET','POST'])
def index():
    return render_template('SearchAlgo.html')



@app.route('/generateAllDS',methods = ['GET','POST'])
def generateAllDS():
    global uniqueArr
    global uniqueSorted
    global root
    global RBT
    

    inputsize = 0
    userarray = 0
    try:
        userarray=request.json['userarray']
    except KeyError:
        print('No userarray')
    

    test = request.json.get(inputsize, 0)
    try:
        inputsize =  int(request.json['inputsize'])
    except KeyError:
        print('No inputsize')

    if inputsize != 0:
        uniqueArr = random.sample(range(inputsize*1000), inputsize)
    else:
        uniqueArr=[int(e) for e in userarray.split(',')]
        
    #Sorted array for binary search  
    uniqueSorted = sorted(uniqueArr)
    
    #Insert values in Binary search tree and create its DS
    root=insert(None,uniqueArr[0])
    for i in range(1,len(uniqueArr)):
        insert(root,uniqueArr[i])
    preorderTraversalBST(root)
    
    #Insert values in Red black tree and create its DS
    RBT = RBTree()
    rbtroot = None
    for i in range(len(uniqueArr)):
        rbtroot = RBT.insertRBTNode(uniqueArr[i]) 
    dataStructureArray = dict()

    #RBT.preorderTraversalRBT()
   
    #6 12 100000//12
    #7 14
    
    if inputsize != 0 and inputsize>10000:
        l = len(uniqueArr)//2        
        dataStructureArray['unique']=uniqueArr[:2500]+uniqueArr[l-1250:l+1250]+uniqueArr[-2500:]
        
    else:
        dataStructureArray['unique']=uniqueArr
    return dataStructureArray

@app.route('/generateBSTDS',methods = ['GET','POST'])
def generateBSTDS():
    global root
    dictPreOrderBST=dict()
    dictPreOrderBST['BST']=preorderTraversalBST(root)
    return dictPreOrderBST

@app.route('/generateRBTDS',methods = ['GET','POST'])
def generateRBTDS():
    global RBT
    dictPreOrderRBT=dict()
    res = RBT.preorderTraversalRBT()
    dictPreOrderRBT['RBT']= res
    return dictPreOrderRBT

@app.route('/generateBSDS',methods = ['GET','POST'])
def generateBSDS():
    global uniqueSorted
    dictBS=dict()
    dictBS['BS']= uniqueSorted
    return dictBS

@app.route('/searchAllElements',methods = ['GET','POST'])
def searchAllElements():
    global uniqueArr,uniqueSorted,root,RBT

    searchElement =  int(request.json['searchelement'])
    selectedAlgo = request.json['selectedAlgo']
    arr_time_LS = []
    arr_time_BS = []
    arr_time_BST = []
    arr_time_RBT= []

    dataRunningTime = dict()
    for j in selectedAlgo:
        if j == "LS":
           for i in range(10):
                a1 = datetime.datetime.now()
                f = linear_search(uniqueArr, searchElement) 
                b1 = datetime.datetime.now()
                c1 = b1 - a1
                arr_time_LS.append(c1.microseconds)
           dataRunningTime[j] = [avg(arr_time_LS),f]
        if j == "BS":
           for i in range(10):
                a1 = datetime.datetime.now()
                f = binary_search(uniqueSorted, searchElement) 
                b1 = datetime.datetime.now()
                c1 = b1 - a1
                arr_time_BS.append(c1.microseconds)
           dataRunningTime[j] = [avg(arr_time_BS),f]
        if j == "BST":
           for i in range(10):
                a1 = datetime.datetime.now()
                f = bstSearch(root, searchElement) 
                b1 = datetime.datetime.now()
                c1 = b1 - a1
                arr_time_BST.append(c1.microseconds)
           dataRunningTime[j] = [avg(arr_time_BST),f]
        if j == "RBT":          
           for i in range(10):
                a1 = datetime.datetime.now()
                f = RBT.search(searchElement)
                b1 = datetime.datetime.now()
                c1 = b1 - a1
                arr_time_RBT.append(c1.microseconds)
           dataRunningTime[j] = [avg(arr_time_RBT),f]
    
    return dataRunningTime

#------------------------------------Binary search-----------------------------------------------------------------------------------------------------------------
def binary_search(inputarray, searchvalue):
    start = 0
    end = len(inputarray) - 1
    mid = 0

    while start <= end:
        mid = (end + start) // 2
        if inputarray[mid] == searchvalue:
            return True
        if inputarray[mid] < searchvalue:
            start = mid + 1
        elif inputarray[mid] > searchvalue:
            end = mid - 1
    return False    

#------------------------------------linear search---------------------------------------------------------------------------------------------------------
def linear_search(inputarray, searchvalue): 
    for i in range(0,len(inputarray)):
        if inputarray[i] == searchvalue:
            return True
    return False

#----------------------------------------Binary Search Tree-----------------------------------------------------------------------------------------------------------------
#class defined for BST
class nodeBST:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

#Insertion function in BST
def insert(NodeBST, data):
    if NodeBST == None:
        return nodeBST(data)
    if data < NodeBST.data:
        NodeBST.left = insert(NodeBST.left, data)
    elif data > NodeBST.data:
        NodeBST.right = insert(NodeBST.right, data)
    return NodeBST

#Function to search in RBT
def bstSearch(rootBST, key):
    while rootBST != None:
        if key == rootBST.data:
            return True
        if key > rootBST.data:
            rootBST = rootBST.right
        elif key < rootBST.data:
            rootBST = rootBST.left
    return False

#Preorder Traversal BST
def preorderTraversalBST(rootBST):
    result = []
    if rootBST:
        result.append(rootBST.data)
        result = result + preorderTraversalBST(rootBST.left)
        result = result + preorderTraversalBST(rootBST.right)
       # print(result,"BST")
    return(result)


#----------------------------------------------------------------RBT --------------------------------------------------------------------------------------------------------------------------------
class RBTNode():
    def __init__(self,data):
        self.data = data                                   
        self.parent = None                               
        self.left = None                                
        self.right = None                                
        self.color = "RED"                                  


class RBTree():
    def __init__(self):
        self.element = RBTNode(0)
        self.element.color = "BLACK"
        self.element.left = None
        self.element.right = None
        self.root = self.element

    # Insert New RBTNode
    def insertRBTNode(self, key):
        node = RBTNode(key)
        node.parent = None
        node.data = key
        node.left = self.element
        node.right = self.element
        node.color = "RED"                                 

        tempNode = None
        newNode = self.root

        while newNode != self.element:                           
            tempNode = newNode
            if node.data < newNode.data:
                newNode = newNode.left
            else:
                newNode = newNode.right

        node.parent = tempNode                                
        if tempNode == None :                                   
            self.root = node
        elif node.data < tempNode.data :                          
            tempNode.left = node
        else :
            tempNode.right = node

        if node.parent == None :                         
            node.color = "BLACK"
            return

        if node.parent.parent == None :                  
            return

        self.fixPosition (node)                         

    # Left rotation RBT
    def rotateLeft (self , newNode ) :
        tempNode = newNode.right                                      
        newNode.right = tempNode.left                                 
        if tempNode.left != self.element :
            tempNode.left.parent = newNode

        tempNode.parent = newNode.parent                              
        if newNode.parent == None :                            
            self.root = tempNode                              
        elif newNode == newNode.parent.left :
            newNode.parent.left = tempNode
        else :
            newNode.parent.right = tempNode
        tempNode.left = newNode
        newNode.parent = tempNode


    #Right rotation RBT
    def rotateRight ( self , newNode ) :
        tempNode = newNode.left                                       
        newNode.left = tempNode.right                                
        if tempNode.right != self.element :
            tempNode.right.parent = newNode

        tempNode.parent = newNode.parent                              
        if newNode.parent == None :                            
            self.root = tempNode                               
        elif newNode == newNode.parent.right :
            newNode.parent.right = tempNode
        else :
            newNode.parent.left = tempNode
        tempNode.right = newNode
        newNode.parent = tempNode


    # Fix Up Insertion
    def fixPosition(self, fixNode):
        while fixNode.parent.color == "RED":                        
            if fixNode.parent == fixNode.parent.parent.right:         
                u = fixNode.parent.parent.left                  
                if u.color == "RED":                          
                    u.color = "BLACK"                          
                    fixNode.parent.color = "BLACK"
                    fixNode.parent.parent.color = "RED"            
                    fixNode = fixNode.parent.parent                   
                else:
                    if fixNode == fixNode.parent.left:               
                        fixNode = fixNode.parent
                        self.rotateRight(fixNode)                        
                    fixNode.parent.color = "BLACK"
                    fixNode.parent.parent.color = "RED"
                    self.rotateLeft(fixNode.parent.parent)
            else:                                         
                u = fixNode.parent.parent.right                
                if u.color == "RED":                         
                    u.color = "BLACK"                          
                    fixNode.parent.color = "BLACK"
                    fixNode.parent.parent.color = "RED"           
                    fixNode = fixNode.parent.parent                  
                else:
                    if fixNode == fixNode.parent.right:               
                        fixNode = fixNode.parent
                        self.rotateLeft(fixNode)                        
                    fixNode.parent.color = "BLACK"
                    fixNode.parent.parent.color = "RED"
                    self.rotateRight(fixNode.parent.parent)              
            if fixNode == self.root:                            
                break
        self.root.color = "BLACK"                             
    

     # # Function for preorder traversal of RBT  
    def preorderRBT (self,node) :
        res=[] 
        if node != self.element:
            res.append(node.data)
            res = res + self.preorderRBT(node.left)
            res = res + self.preorderRBT(node.right)
        #print(res,"Red black tree")
        return res
        

    def preorderTraversalRBT(self) :
        return self.preorderRBT(self.root)

#Function for search in RBT
    def search(self,key):
        return self.search_helper(self.root, key)

    def search_helper(self,node,key):
        while node != self.element:
            if key == node.data:
                return True
            if key < node.data:
                node = node.left
            else:
                node = node.right
        return False
        
def avg(arr):
    return timeFunc(round(sum(arr[1:])/len(arr[1:]),2))

def timeFunc(t):
    return t
if __name__ == '__main__':
   app.run(host='localhost',port=9874,debug=True)


