# Example binary 
import random


class Solution:
	def __init__(self):
		self.program=[]
	
	def generateSimpleSolutions(self,var):
		pass

class Razonador:
	def __init__(self):
		self.examples=ExamBin()

		while True:
			match random.randomint(0,2):
				case 0:
					print("Genera una nueva solucion")
					# get random sample
					sample = random.choice(self.examples.examples)
					
				case 1:
					print("Muta una solucion")
				case 2:
					print("Testea una solucion")
					



class ExamBin:
	def __init__(self):
		self.makeExamples()
		
	
	def makeExamples(self):
		examples=1000
		self.examples=[]
		for i in range(examples):
			var={}
			var["a"]=random.random()*2-1
			var["b"]=random.random()*2-1
			var["c"]=random.random()*2-1

			self.examples.append(var)

	def simple(self,var):
		if var["c"]<0:
			return var["a"]
		else:
			return var["b"]



if __name__ == "__main__":
	ExamBin()