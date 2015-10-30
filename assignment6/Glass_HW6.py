#change dependancy to 0 or 1 if Known
#change derivatives to 0 or 1 if known statsu= 1,0 or -1
import math as M

#functions

NODES=[]

def Update_NODES():
	for N in NODES:
		N.get_probability()
		print(N.name,":",N.marginal)


def joint(nodes):
	p=1
	conditions=[]
	for n in nodes:
		p=p*n.get_probability();
		conditions.append(n)

	return p


def Distribution(nodes):
	prob_dict={}
	for node in nodes:
		prob_dict.update({node.name:{}})
		for x in range(0,pow(2,len(nodes)-1)):
			for n2 in nodes:
				if(x & pow(2,nodes.index(n2))>0):
					n2.status=1
			prob_dict[node.name].update({x : node.get_probability()})
	return prob_dict



def conditional(base,conditions):
	P=1
	if conditions==[]:
		for N in base:
			P=P*N.get_marginal()
		return P
	divisor=1
	for node in conditions:
		divisor=divisor*node.marginal
		#print(node.name,":",node.notFlag)
		if(node.notFlag):
			node.status=1
		else:
			#if(node.name=="Dyspnoea"):
				#print("setting")
			node.status=0
		#print(node.name,":", node.status)
		for n1 in node.dependencies:
			n1.get_probability()
	for node in base:
		node.get_probability()
		P=P*node.marginal;
	return P


def bayes(n1,n2):
	if(n2==[]):
		return 1
	PA=1
	PB=1
	for N in n1:
		PA=PA*N.marginal
	for N in n2:
		PB=PB*N.marginal

	return conditional(n2,n1)*PB/PA


class probability:
	
	def __init__(self,name):
		self.name=name
		self.status=-1
		self.num_deps=0
		self.dependencies=[]
		self.derivatives=[]
		self.values=[]
		self.notFlag=True


	def Not(self):
		self.notFlag=False
		return self


	def get_marginal(self):
		if(self.status>=0):
			return self.status
		else:
			if(not self.notFlag):
				return (1-self.marginal)
			return self.marginal


	def get_probability(self):
		flags=[0]
		returnval=0
		numflags=1

		#print("GET",self.name)
		for prob in reversed(self.dependencies):
			if(prob.status==-1):
				for x in range(0,numflags):
					flags.append(flags[x]+pow(2,self.dependencies.index(prob)))
				numflags=numflags*2
			else:
				#print(self.name,"Status:",prob.status)
				for y in range(0,numflags):
					flags[y]=flags[y]+ (prob.status*pow(2,self.dependencies.index(prob)))
		flags=sorted(flags)

		for x in range(0,numflags):
			#print("X:",x,"FLAGS:",flags)
			#print("VALUES:",self.values)
			weight=1
			for prob in reversed(self.dependencies):
				#print(self.name,"depends on",prob.name)
				if(flags[x] & pow(2,self.dependencies.index(prob)))>0:
					weight=prob.get_marginal()*weight
					#print("marginal:",prob.marginal,"weight:",weight)
				else:
					weight=(1-prob.get_marginal())*weight
					#print("anti-marginal:",prob.marginal,"weight:",weight)
			returnval=self.values[flags[x]]*weight + returnval
			#print(returnval)
		self.marginal=returnval
		#print("GET")
		#print(self.name,":",self.marginal)
		bayesval=1
		bayes_prob=[]
		for prob in self.derivatives:
			#print(prob.name,":",prob.status)
			if(not prob.status==-1):
				#print("bayes")
				bayes_prob.append(prob)
		bayesval = bayes([self],bayes_prob)
		if bayesval<1:
			print("bayes calc:",bayesval)
			self.marginal=bayesval
			reurnval=bayesval
		if(not self.notFlag):
			return 1-returnval
		return returnval


	def set_marginal(self):
		marginal=0.0
		for x in range(0,pow(2,self.num_deps)):
			weight=1;
			for dep in self.dependencies:
				if(x & pow(2,self.dependencies.index(dep))):
					weight=dep.get_marginal()*weight
				else:
					weight=(1-dep.get_marginal())*weight
			marginal=marginal+weight*self.values[x]
		self.marginal=marginal

	

	def set_values(self,vals):
		if(len(vals)<2^(self.num_deps-1)):
			print("not enough values")
			return
		for val in vals:	#values arranged in binary counting 000,001,010,011,100
			self.values.append(val)
		self.set_marginal()

	def set_dependancy(self,dep_list):
		self.num_deps=len(dep_list)
		for x in dep_list:
			self.dependencies.append(x)

	def set_derivatives(self,derivs):
		self.num_derivs=len(derivs)
		for x in derivs:
			self.derivatives.append(x)



Smoking=probability("smoking")
Smoking.set_values([0.3])

print("smoking done")

Pollution=probability("Pollution")
Pollution.set_values([0.9])

print("Pollution done")


Cancer=probability("cancer")
Xray=probability("Xray")
Xray.set_values([.2,.9])

Dyspnoea=probability("Dyspnoea")
Dyspnoea.set_values([.3,.65,])

Dyspnoea.set_dependancy([Cancer])
Xray.set_dependancy([Cancer])

Cancer.set_dependancy([Smoking,Pollution])
Cancer.set_derivatives([Xray,Dyspnoea])
Cancer.set_values([.02,.05,.001,.03])

NODES.append(Pollution)
NODES.append(Smoking)
NODES.append(Cancer)
NODES.append(Xray)
NODES.append(Dyspnoea)
Update_NODES()


print("Distribution:",Distribution([Smoking,Pollution,Cancer]))
print("Diagnostic:",conditional([Cancer,Pollution],[Dyspnoea]))
print("Diagnostic:",conditional([Pollution.Not()],[Dyspnoea]))
print("Diagnostic:",conditional([Cancer],[Dyspnoea]))
