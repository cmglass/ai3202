#CSCI 3202 Introduction to Artificial intelligence
#University of Colorado at Boulder
#HW5	Fall 2015
#Author: Chris Glass

#usage: Assignment3_Glass.py [world file] [Epsilon(optional)]



import random
import sys
import queue as Q

#GLOBAL VARIABLES
coords=[]
NODES=[]
node_queue=Q.Queue()

#GLOBAL VALUES
left_bias=0.1
right_bias=0.1
correctness=0.8
delta=100
gamma=0.9
epsilon=0.5
height=7 #world size of 0,0 is one square
width=9
start_x=0
start_y=7

class node:
	util=0
	delta=100

	def __init__(self, loc_x,loc_y,value):
		self.x=loc_x
		self.y=loc_y
		if(value=="3"):
			self.value=-2
		elif(value=="1"):
			self.value=-1
		elif(value=="2"):
			self.value=0
		elif value=="4":
			self.value=1
		else:
			self.value=int(value)
		self.H=10000
		self.util=0
		self.parent=None
		self.next=None




	def set_utility(self):
		x1=self.x
		y1=self.y
		x2=self.x+1
		y2=self.y+1		
		x3=self.x-1
		y3=self.y-1
		#print(x1,y1)
		A1=1
		A2=1
		A3=1
		A4=1
		a1=.8
		b1=.1
		c1=.1
		a2=.8
		b2=.1
		c2=.1

		if(x1==9 or coords[y1][x1+1]=="2"):
			x2=x1
			A1=0
			c2=0
			a2=a2+.1
		if(x1==0 or coords[y1][x1-1]=="2"):
			x3=x1
			A2=0
			b2=0
			a2=a2+.1
		if(y1==7 or coords[y1+1][x1]=="2"):
			y2=y1
			c1=0
			a1=a1+.1
			A3=0
		if(y1==0 or coords[y1-1][x1]=="2"):
			y3=y1
			b1=0
			a1=a1+.1
			A4=0

		A1=A1*(a1*NODES[x2][y1].util+b1*NODES[x1][y3].util+c1*NODES[x1][y2].util)
		A2=A2*(a1*NODES[x3][y1].util+b1*NODES[x1][y3].util+c1*NODES[x1][y2].util)
		A3=A3*(a2*NODES[x1][y2].util+b2*NODES[x3][y1].util+c2*NODES[x2][y1].util)
		A4=A4*(a2*NODES[x1][y3].util+b2*NODES[x3][y1].util+c2*NODES[x2][y1].util)
		util=self.value+gamma*max(A1,A2,A3,A4)
		if(util>50):
			util=50
			self.delta=0
			return
		diff=util-self.util
		self.util=util
		delta_n=abs(diff)
		self.delta=delta_n


	def __lt__(self,other):
		return self.util<other.util

	def __gt__(self,other):
		return self.util>other.util
	
	def __eq__(self,other):
		return self.util==other.util




if(len(sys.argv)<2):
	print("not enought arguments ")
	print("usage: Assignment5_Glass [world file] [Epsilon]")
	print("please specify a worldfile or enter \"default\"")
 	
	sys.exit()

world=sys.argv[1]
if world=="default":
	world="World1MDP.txt"
if len(sey.argv)>2:
	epslion=sys.arg[2]
#world= "World1MDP.txt"

# read in map
with open(world) as F:
	line=F.readlines()
	for x in line:
		if x=="\n":
			break
		coords.append(x.split())


#populate NODES

for x in range(0,width+1):
	NODES.append([])
	for y in range(0,height+1):
		#print(x,y)
		NODES[x].append(node(x,y,coords[y][x]))


err=epsilon*((1-gamma)/gamma)
print(err)
while(delta>err):
	delta=0
	for x in range(width,-1,-1):
		for y in range(0,height+1):
			#print(x,y)
			NODES[x][y].set_utility()
			if(delta<NODES[x][y].delta):
				delta=NODES[x][y].delta


N=NODES[start_x][start_y]
N.next=max(NODES[start_x+1][start_y],NODES[start_x-1][start_y],NODES[start_x][start_y-1])
while(N.util<N.next.util and N.next.util!=50):
	N=N.next
	
	x=N.x
	y=N.y
	y3=y-1
	y2=y+1
	x3=x-1
	x2=x+1
	if(x==9 or coords[y][x+1]=="2"):
		x2=x
	if(x==0 or coords[y][x-1]=="2"):
		x3=x
	if(y==7 or coords[y+1][x]=="2"):
		y2=y
	if(y==0 or coords[y-1][x]=="2"):
		y3=y

	N1=NODES[x2][y]
	N2=NODES[x3][y]
	N3=NODES[x][y2]
	N4=NODES[x][y3]
	N.next=max(N1,N2,N3,N4,)

N=NODES[start_x][start_y]
print(N.util)
while(N.next):
	print(N.next.util)
	N=N.next
