import numpy as np
import matplotlib.pyplot as plt
import math
import random
import sqlite3
import getopt
import sys

# sign function
def sign(val):
	
	if val>1e-6:
		val  = 1
	elif val < -1e-6:
		val = -1
	else:
		val = 0

	return val

#zone-functon
# return +/-1:inside
# return  0  :outside
def fsg(x,d):

	output = (sign(x+d) - sign(x-d))/2

	return output

#power function
def fal(e,alpha,zeta):

	s = fsg(e,zeta)

	fal_output = e*s/(pow(zeta,1-alpha))+pow(abs(e),alpha)*sign(e)*(1-s)

	return fal_output	

#
#class ESO
#
class ESO():
	"""docstring for ESO"""
	def __init__(self,beta01,beta02,beta03):
		self.beta01 = beta01
		self.beta02 = beta02
		self.beta03 = beta03
		self.b0 = 0.0
		self.z1 = 0.0
		self.z2 = 0.0
		self.z3 = 0.0
		self.y = 0.0
		self.b = 0
		self.u = 0
		self.e = 0.0
		self.fe = 0
		self.fe1 = 0

	def fleso(self):
		h = 0.05
		self.fe = fal(self.e,0.5,h)
		self.fe1 = fal(self.e,0.25,h)
		self.e = self.z1 - self.y
		#update observe
		self.z1 += self.z2 - self.beta01 * self.e
		self.z2 += self.z3 - self.beta02 * self.e + self.b * self.u
		self.z3 += -self.beta03*self.e

def graph_display(plot,xnums,ynums,ID,xval,yval,name,xlabs,ylabs,color):
	ax = plot.add_subplot(xnums,ynums,ID)
	ax.set_xlabel(xlabs)
	ax.set_ylabel(ylabs)
	ax.plot(xval, yval, color=color, label=name)
	ax.legend()

#
#Setup function
#
def setup():
	
	#Open DB file
	conn = sqlite3.connect('/home/peng/Documents/2019-06-06-13-48-42.db')
	cursor = conn.cursor()
	cursor.execute("SELECT rx_pitch FROM ATTITUDE_BEAM;")
	rows=cursor.fetchall()

	#beta01 beta02 beta03
	eso = ESO(300.0,4000.0,10000)
	eso.b = 0
	eso.u = 0

	#set cycle times
	size=len(rows)

	#set X axis value
	X  = np.array(range(0,size))

	#eso
	Y_TD_z1  = np.array(range(size), dtype = float)
	Y_TD_z2  = np.array(range(size), dtype = float)
	Y_TD_z3  = np.array(range(size), dtype = float)
	Y_TD_x1  = np.array(range(size), dtype = float)
	Y_TD_x2  = np.array(range(size), dtype = float)
	Y_TD_x3  = np.array(range(size), dtype = float)

	for k in np.arange ( size ):
		Y_TD_x1[k]  = rows[k][0]
		#execute td
		eso.y = rows[k][0]
		eso.b = rows[k][0]
		eso.u = rows[k][0]
		eso.fleso()

		Y_TD_z1[k] = eso.z1
		Y_TD_z2[k] = eso.z2
		Y_TD_z3[k] = eso.z3
		Y_TD_x1[k] = eso.y

	fig = plt.figure()
	graph_display(fig,1,2,1,X,Y_TD_z1,"eso z1","cycle time","rate",'red')
	graph_display(fig,1,2,1,X,Y_TD_z2,"eso z2","cycle time","rate",'red')
	graph_display(fig,1,2,1,X,Y_TD_z3,"eso z3","cycle time","rate",'green')
	graph_display(fig,1,2,1,X,Y_TD_x1,"eso x1","cycle time","rate",'red')
	plt.show()


if __name__ == "__main__":
	setup()
