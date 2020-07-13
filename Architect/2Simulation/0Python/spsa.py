import numpy as np
import matplotlib.pyplot as plt
import math
import random
import sys

#
#class td filter
#
class spsa():

	"""docstring for spsa"""
	def __init__(self,A,a,alpha,c,gamma):
		self.ak = 0
		self.A = A
		self.a = a
		self.alpha = alpha
		self.ck = 0.0
		self.c = c
		self.gamma = gamma
		self.k = 0
		self.delta_k = 0
		self.theta_k = 0
		self.gradient = 0
		self.posx = 0
		self.posy = 0

	#
	# update delta_k
	#
	def update_delta_k(self):
		self.k+=1
		self.ck = self.c/math.pow(self.k,self.gamma)
		self.delta_k = self.ck * random.uniform(-1,1)

	#
	# clean k
	#
	def clean_k(self):
		self.k = 0

	#
	# update theta_k
	#
	def update_theta_k(self,s_diff):
		self.ak = self.a/math.pow((self.k + self.A),self.alpha)
		self.gradient = (s_diff)/(2*self.delta_k)
		self.theta_k  = self.ak * self.gradient 

class quality(object):
	"""docstring for quality"""
	def __init__(self, x,y):
		self.x = x
		self.y = y
	
	def get_power(tx,ty,lx,ly):
		self.x=tx-lx
		self.y=ty-ly
		pos_len = math.sqrt((self.x**2)+(self.y**2))
		if pos_len < 0.1:
			pos_len = 0.1
		if pos_len > 10:
			pos_len = 10
		return pos_len


def graph_display(plot,xnums,ynums,ID,xval,yval,name,xlabs,ylabs,color):
	ax = plot.add_subplot(xnums,ynums,ID)
	ax.set_xlabel(xlabs)
	ax.set_ylabel(ylabs)
	ax.plot(xval, yval, color=color, label=name)
	ax.legend()
	ax.grid(True)

def radar_display(plot):
	plot.axes(polar = True)
	plot.legend()
	plot.grid(True)

#
#Setup function
#
def setup():
	
	#r h N0 C
	obj = spsa(8.6,1.2,0.602,1,0.101);
	qlt = quality(10,10)

	#set cycle times
	size=100

	#set X axis value
	X  = np.array(range(0,size))

	#ck and delta_k
	Y_ck  	   = np.array(range(size), dtype = float)
	Y_delta_k  = np.array(range(size), dtype = float)
	#ak and theta_k
	Y_ak  	   = np.array(range(size), dtype = float)
	Y_theta_k  = np.array(range(size), dtype = float)
	#gradinet
	Y_gradinet = np.array(range(size), dtype = float)

	for k in np.arange ( size ):
		obj.update_delta_k()
		Y_ck[k]		= obj.ck
		Y_delta_k[k]= obj.delta_k

		obj.update_theta_k((size-k)/size)
		Y_ak[k]		 = obj.ak
		Y_theta_k[k] = obj.theta_k
		Y_gradinet[k]= obj.gradient

	fig = plt.figure()
	graph_display(fig,2,1,1,X,Y_ck,"ck","cycle time","rate",'red')
	graph_display(fig,2,1,1,X,Y_delta_k,"delta k","cycle time","rate",'blue')
	graph_display(fig,2,1,2,X,Y_ak,"ak","cycle time","rate",'red')
	graph_display(fig,2,1,2,X,Y_theta_k,"theta k","cycle time","rate",'blue')
	graph_display(fig,2,1,2,X,Y_gradinet,"gradient","cycle time","rate",'green')

	fig2 = plt.figure()
	radar_display(plt)

	plt.show()

if __name__ == "__main__":
	setup()
