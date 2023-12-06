import random

class Signal:
	def __init__(self, name,f=None):
		self.name = name
		self.f=f
		self.fathers=[]
	
	def iterator(self):
		if self.f:
			self.value = self.f()
		else:
			self.value = random.randint(0, 1)

class Net:
	def __init__(self):
		self.signals = []
		self.links={}
		self.man=[]
		self.woman=[]
		self.name2signal={}
	
	def Signal(self, name,f=None, man=True,woman=True):
		if name in self.name2signal:
			return self.name2signal[name]
		signal = Signal(name,f)
		self.name2signal[name]=signal
		self.signals.append(signal)

		if man:
			self.man.append(signal)
		if woman:
			self.woman.append(signal)

		return signal
	
	def iterator(self):
		for signal in self.signals:
			signal.iterator()
		return True
	def print(self):
		for signal in self.signals:
			if hasattr(signal,"value"):
				print(signal.name,signal.value)
		print("")
		print("Links:")
		l=list(self.links.items())
		l.sort(key=lambda x: x[1],reverse=True)
		for k,l in l:
			print(k[0].name,"=",k[1].name,l)
		# for k,l in self.links.items():
		# 	print(k[0].name,k[1].name,l)
		print("")
	
	def equal(self,a,b):
		if a==0 and b==0:
			return True
		if a==1 and b==1:
			return True
		if a==2 or b==2:
			return False
		if a==0.5 or b==0.5:
			return True
		return False
	
	def coremux(self,y,a,b):
		eq1=self.equal(y.value,a.value)
		eq2=self.equal(y.value,b.value)
		if eq1 and eq2:
			return 0.5
		if eq1:
			return 0
		if eq2:
			return 1
		return 2
	
	def elementals(self,k):
		if len(k.fathers)==0:
			return [k]
		r=[]
		for f in k.fathers:
			r+=self.elementals(f)
		return r

	def linkable(self,k1,k2,k3):
		v1=self.elementals(k1)
		v2=self.elementals(k2)
		v3=self.elementals(k3)
		for v in v1:
			if v in v2:
				return False
			if v in v3:
				return False
		return True

	def guess(self):
		for w in self.woman:
			for m in self.man:
				if m!=w:
					if self.equal(m.value,w.value):
						if (w,m) not in self.links:
							self.links[(w,m)]=0
						self.links[(w,m)]+=1
		# traslada print
		l=list(self.links.items())
		l.sort(key=lambda x: x[1],reverse=True)

		if l[0][1]<40:
			return

		# fabrica multiplexor		
		# busca top con común que no esté
		for i in range(len(l)):
			for j in range(i+1,len(l)):
				l1=l[i]
				l2=l[j]
				k1=l1[0]
				k2=l2[0]
				name=None
				if k1[1]==k2[1] and self.linkable(k1[1],k1[0],k2[0]):
					y=l1[0][1]
					a=l1[0][0]
					b=l2[0][0]
					name="("+k1[0].name+","+k2[0].name+")->"+k1[1].name
					f=lambda: self.coremux(y,a,b)

				if k1[0]==k2[0] and self.linkable(k1[0],k1[1],k2[1]):
					# identifica los l creadores, devuelve name y 
					y=l1[0][0]
					a=l1[0][1]
					b=l2[0][1]
					name="("+k1[1].name+","+k2[1].name+")->"+k1[0].name
					f=lambda: self.coremux(y,a,b)
				
				if k1[1]==k2[0] and self.linkable(k1[1],k1[0],k2[1]):
					y=l1[0][1]
					a=l1[0][0]
					b=l2[0][1]
					name="("+k1[0].name+","+k2[1].name+")->"+k1[1].name
					f=lambda: self.coremux(y,a,b)
				
				if k1[0]==k2[1] and self.linkable(k1[0],k1[1],k2[0]):
					y=l1[0][0]
					a=l1[0][1]
					b=l2[0][0]
					name="("+k1[1].name+","+k2[0].name+")->"+k1[0].name
					f=lambda: self.coremux(y,a,b)

				if name==None:
					#print("k1,k2",k1[0].name,k1[1].name,k2[0].name,k2[1].name)
					continue

				if not y in self.man:
					continue
					
				s=self.Signal(name,f,woman=False)
				s.fathers=[y,a,b]
				return 
					
			
		# comun arriba / diferencia abajo
		# pon como hombre cuando ganan (+ y -)

if __name__ == "__main__":
	net=Net()
	man=False
	net.Signal("1",man=False,f=lambda: 1)
	net.Signal("0",man=False,f=lambda: 0)
	a=net.Signal("a",man=man)
	b=net.Signal("b",man=man)
	c=net.Signal("c",man=man)
	net.Signal("r1",man=man)
	net.Signal("r1",man=man)
	net.Signal("r2",man=man)
	net.Signal("r3",man=man)
	net.Signal("r4",man=man)
	net.Signal("y",lambda: a.value if c.value==0 else b.value,woman=False)
	net.Signal("and",lambda: a.value*b.value,woman=False)
	net.Signal("or",lambda: min(1,a.value+b.value),woman=False)


	while net.iterator():
		net.guess()
		net.print()