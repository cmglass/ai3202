#CSCI 3202 Introduction to Artificial intelligence
#University of Colorado at Boulder
#HW3	Fall 2015
#Author: Chris Glass

#usage: Assignment3_Glass.py [world file][heuristic]

import queue
import sys
import math as M

x_bound=9
y_bound=7

#class to store each square as it is vistied
class node:
	def __init__(self,cost, loc_x,loc_y,mtn):
		self.cost=cost
		self.x=loc_x
		self.y=loc_y
		self.mtn=mtn
		self.H=10000
		self.parent=None

	def set_H(self,dest,huer):
		if(huer==1):
			self.H=abs(self.x-dest[0])+abs(self.y-dest[1])
		else:
			self.H=M.sqrt(M.pow(self.x-dest[0],2)+ M.pow(self.y-dest[1],2))

	def set_parent(self,parent):
		self.parent=parent

	def __lt__(self,other):
		return (self.H+self.cost)<(other.H+other.cost)

#generates nodes based upon current node location
def get_node(N,direction):
	if(direction=='N' and N.y >0):		#checks for direciton and if it is valid
		mtn=int(row[N.y-1][N.x])		#gets square value
		if(mtn==2):						#wall check
			return 0
		return node(N.cost+10+10*mtn,N.x,N.y-1,mtn);		#old cost plus 10 plus mtn cost if avilable
	elif(direction=='NE' and N.x<x_bound and N.y>0):
		mtn=int(row[N.y-1][N.x+1])
		if(mtn==2):
			return 0
		return node(N.cost+14+10*mtn,N.x+1,N.y-1,mtn);
	elif(direction=='E' and N.x<x_bound ):
		mtn=int(row[N.y][N.x+1])
		if(mtn==2):
			return 0
		return node(N.cost+10+10*mtn,N.x+1,N.y,mtn);
	elif(direction=='SE' and N.y<y_bound and N.x<x_bound):
		mtn=int(row[N.y+1][N.x+1])
		if(mtn==2):
			return 0
		return node(N.cost+14+10*mtn,N.x+1,N.y+1,mtn);
	elif(direction=='S' and N.y<y_bound):
		mtn=int(row[N.y+1][N.x])
		if(mtn==2):
			return 0
		return node(N.cost+10+10*mtn,N.x,N.y+1,mtn);
	else:
		return 0

#add eligable nodes assumes movemnt from bottom left to upper right
def search(Node):
	N =get_node(Node,'N')
	if(N):
		N.set_H(destination,huer)	#set hueristic value relative to destination
		N.set_parent(Node)		#set the nodes parent for trace back
		queue_put(N)			#add node to priority queue
		travel_list.append(N)
	NE=get_node(Node,'NE')
	if(NE):
		NE.set_H(destination,huer)
		NE.set_parent(Node)
		queue_put(NE)
		travel_list.append(NE)		
	E=get_node(Node,'E')
	if(E):
		E.set_H(destination,huer)
		E.set_parent(Node)
		queue_put(E)
		travel_list.append(E)	
	SE=get_node(Node,'SE')
	if(SE):
		SE.set_H(destination,huer)
		SE.set_parent(Node)
		queue_put(SE)
		travel_list.append(SE)	
	S=get_node(Node,'S')
	if(S):
		S.set_H(destination,huer)
		S.set_parent(Node)
		queue_put(S)
		travel_list.append(S)	

# print path from desitination to start
def PrintParent(Node):
	while  Node is not None:
		print("X:",Node.x," y:" , Node.y)
		Node=Node.parent

def queue_put(Node):
	for N in travel_list:
		if(N.x==Node.x and N.y==Node.y):
			return 0

	queue.put(Node);


#get commandline args
if(len(sys.argv)<3):
	print("not enought arguments ")
	print("usage: Assignment3_Glass [world file][heuristic]")
	print ("heuristics: manhattan, euclidean")
	sys.exit()
world=sys.argv[1]
heuristic=sys.argv[2]

if(heuristic=="manhattan"):
	huer=1
elif(heuristic=="euclidean"):
	huer=2
else:
	huer=1

#global initilization
destination =(9,0)
start_node=node(0,0,7,0)
queue=queue.PriorityQueue()

i=0
row=[]
try:
	with open(world) as F:
		line=F.readlines()
		for x in line:
			row.append(x.split())
except:
	print("file could not be opened")
	sys.exit()

travel_list=[]
Node=start_node
num_nodes=0
#main loop to find result
while(Node.x!=destination[0] or Node.y != destination[1]):
	search(Node)
	num_nodes=1+num_nodes
	Node=queue.get()


PrintParent(Node) #print reverse path
print(Node.cost)	#print cost of path
print("number of nodes vistied:", num_nodes)
