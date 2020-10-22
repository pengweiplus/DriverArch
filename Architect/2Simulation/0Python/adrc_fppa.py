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
#class td filter
#
class TD():

	"""docstring for Td_filter"""
	def __init__(self,r,h,N0,c):
		self.r = r
		self.h = h
		self.N0 = N0
		self.c = c
		self.h0 = 0.0
		self.fh = 0.0
		self.x1 = 0.0
		self.x2 = 0.0
		self.fh = 0.0

	#
	# TD tracker(Second-Order)
	#
	# x1(k+1) = x1(k) + h * x2(k)
	# x2(k+1) = x2(k) - r0 * u(k)
	# fhan(x1,x2,r0,h0)

	def fhan(self,excpt):
		# Calculate the error between original signal and excepted signal.
		x1_delta = self.x1 - excpt
		# Optimized step value.
		self.h0 = self.N0 * self.h
		# Calulate d and a0
		# d means the estimate increment of signal in one step.
		# a0 means the increment speed of signal in one step.
		d = self.r * self.h0 * self.h0
		a0 = self.x2 * self.h0
		# Optimized transition signal.
		y = x1_delta + a0
		
		# a1 means limit of delta
		# a2 means optimized delta based x2
		a1 = math.sqrt(d*(d+8*abs(y)))
		a2 = a0 + sign(y)*(a1-d)/2

		# Calculate the final delta of x2 :a.
		# If outof d, a is a2
		# If inside d, a is a0+y
		a = (a0 + y)*fsg(y,d) + a2*(1 - fsg(y,d))

		# Calculate the final delta of x2.
		# If outof d, the increment of x2 is r*sign(a)
		# If inside d, fh is r*(a/d)
		self.fh = -self.r * (a/d) * fsg(a,d) - self.r * sign(a)*(1-fsg(a,d))

		# Update x1 by x2,and x2 by fh
		self.x1 = self.x1 + self.h * self.x2
		self.x2 = self.x2 + self.h * self.fh


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
		self.b0 = 0.001
		self.u = 0
		self.e = 0.0
		self.fe = 0
		self.fe1 = 0
		self.f0 = 0

	def fleso(self):
		h = 0.05
		self.fe = fal(self.e,0.5,h)
		self.fe1 = fal(self.e,0.25,h)

		self.e = self.z1 - self.y

		#update observe
		self.z1 += (self.z2 - self.beta01 * self.e)*h
		self.z2 += (self.z3 - self.beta02 * self.fe + self.b0 * self.u)*h
		self.z3 += (-self.beta03 * self.fe1)*h

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
	
	path = '/home/peng/Documents/2020-09-27-16-08-43.db'

	#Open DB file
	conn = sqlite3.connect(path)
	cursor = conn.cursor()
	cursor.execute("SELECT yaw_achieved FROM PID_TUNING;")
	yaw_u0 = cursor.fetchall()

	#Open DB file
	cursor = conn.cursor()
	cursor.execute("SELECT yaw_desired FROM PID_TUNING;")
	yaw_y = cursor.fetchall()

	cursor = conn.cursor()
	cursor.execute("SELECT yaw_error_td FROM PID_TUNING;")
	yaw_dy = cursor.fetchall()

	#Open DB file
	cursor = conn.cursor()
	cursor.execute("SELECT yaw_ff_comp FROM PID_TUNING;")
	yaw_f0 = cursor.fetchall()

	# beta01 beta02 beta03
	eso = ESO(10,2.5,0.5)

	#set cycle times
	size=len(yaw_u0)

	#set X axis value
	X  = np.array(range(0,size))

	#eso
	Y_TD_x1  = np.array(range(size), dtype = float)
	Y_TD_x2  = np.array(range(size), dtype = float)
	Y_TD_z1  = np.array(range(size), dtype = float)
	Y_TD_z2  = np.array(range(size), dtype = float)
	Y_TD_z3  = np.array(range(size), dtype = float)
	Y_TD_y   = np.array(range(size), dtype = float)
	Y_TD_dy   = np.array(range(size), dtype = float)
	Y_TD_f0  = np.array(range(size), dtype = float)
	Y_TD_u0  = np.array(range(size), dtype = float)

	for k in np.arange ( size ):

		#execute eso
		eso.y = yaw_y[k][0]-168.28
		eso.u = yaw_u0[k][0]
		eso.f0 = yaw_f0[k][0]

		eso.fleso()

		Y_TD_z1[k] = eso.z1
		Y_TD_z2[k] = eso.z2
		Y_TD_z3[k] = eso.z3
		Y_TD_y[k] = eso.y
		Y_TD_dy[k] = -yaw_dy[k][0]
		Y_TD_u0[k] = eso.u
		Y_TD_f0[k] = eso.f0

	fig = plt.figure()
	graph_display(fig,3,1,1,X,Y_TD_y,"eso y","cycle time","rate",'blue')
	graph_display(fig,3,1,1,X,Y_TD_z1,"eso z1","cycle time","rate",'red')

	graph_display(fig,3,1,2,X,Y_TD_dy,"eso dy","cycle time","rate",'blue')
	graph_display(fig,3,1,2,X,Y_TD_z2,"eso z2","cycle time","rate",'red')

	# graph_display(fig,3,1,3,X,Y_TD_u0,"eso u0","cycle time","rate",'red')
	# graph_display(fig,3,1,3,X,Y_TD_f0,"eso f0","cycle time","rate",'green')
	
	graph_display(fig,3,1,3,X,Y_TD_z3,"eso z3","cycle time","rate",'blue')
	plt.show()


if __name__ == "__main__":
	setup()
