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

	def feso(self):
		h = 0.05
		self.fe = fal(self.e,0.5,h)
		self.fe1 = fal(self.e,0.25,h)
		self.e = self.z1 - self.y
		#update observe
		self.z1 += self.z2 - self.beta01 * self.e
		self.z2 += self.z3 - self.beta02 * self.e + self.b * self.u
		self.z3 += -self.beta03*self.e

class LESO(object):
	"""docstring for LESO"""
	def __init__(self,beta01,beta02,beta03,h):
		self.beta01 = beta01
		self.beta02 = beta02
		self.beta03 = beta03
		self.b0 = 0.0
		self.z1 = 0.0
		self.z2 = 0.0
		self.z3 = 0.0
		self.y = 0.0
		self.u = 0
		self.e = 0.0
		self.h = h

	def fleso(self):
		self.e = self.z1 - self.y
		#update observe
		self.z1 += self.h*(self.z2 - self.beta01 * self.e)
		self.z2 += self.h*(self.z3 - self.beta02 * self.e + self.b0*self.u)
		self.z3 += self.h*(-self.beta03*self.e)
		

def graph_display(plot,row,col,ID,x,y,name,c,s):
	ax = plot.add_subplot(row,col,ID)
	ax.plot(x,y,color=c,label=name,ls=s)
	ax.legend()

#
#Setup function
#
def setup():
	
	#Open DB file
	conn = sqlite3.connect('/home/peng/Documents/2020-05-09-14-16-50.db')
	cursor = conn.cursor()

	cursor.execute("SELECT rx_pitch FROM ATTITUDE_BEAM;")
	beam=cursor.fetchall()

	cursor.execute("SELECT pitch_desired FROM PID_TUNING;")
	ctrl=cursor.fetchall()

	cursor.execute("SELECT pitch_error FROM PID_TUNING;")
	error=cursor.fetchall()

	#beta01 beta02 beta03
	eso = LESO(35,60,160,0.03)
	eso.b0 = 0
	eso.z1 = 53.0
	#set cycle times
	size=len(beam)

	#set X axis value
	X  = np.array(range(0,size))

	#eso
	Y_TD_z1  = np.array(range(size), dtype = float)
	Y_TD_z2  = np.array(range(size), dtype = float)
	Y_TD_z3  = np.array(range(size), dtype = float)
	Y_TD_x1  = np.array(range(size), dtype = float)
	Y_TD_u   = np.array(range(size), dtype = float)
	uY_TD_err = np.array(range(size), dtype = float)

	for k in np.arange ( size ):
		#execute td
		eso.y = beam[k][0]
		eso.u = ctrl[k][0]
		eso.fleso()

		Y_TD_z1[k] = eso.z1
		Y_TD_z2[k] = eso.z2
		Y_TD_z3[k] = eso.z3
		Y_TD_x1[k] = eso.y
		Y_TD_u[k] = eso.u
		# Y_TD_err[k] = error[k][0]

	row = 3
	col = 1
	fig = plt.figure()
	graph_display(fig,row,col,1,X,Y_TD_x1,"eso x1",'blue','-')
	graph_display(fig,row,col,1,X,Y_TD_z1,"eso z1",'red','-')
	graph_display(fig,row,col,2,X,Y_TD_z2,"eso z2",'green','-')
	graph_display(fig,row,col,3,X,Y_TD_z3,"eso z3",'orange','-')

	# row = 1
	# col = 1
	# fig = plt.figure()
	# graph_display(fig,row,col,1,X,Y_TD_x1,"eso x1",'green','-')
	# graph_display(fig,row,col,1,X,Y_TD_z1,"eso z1",'red','--')

	# graph_display(fig,row,col,1,X,Y_TD_u,"eso u",'red','--')
	# graph_display(fig,row,col,1,X,Y_TD_err,"eso err",'green','-')
	plt.show()


if __name__ == "__main__":
	setup()
