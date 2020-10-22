import numpy as np
import matplotlib.pyplot as plt
import math
import random


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

#graph_display function
def graph_display(plot,xnums,ynums,ID,xval,yval,name,xlabs,ylabs,color):
	ax = plot.add_subplot(xnums,ynums,ID)
	ax.set_xlabel(xlabs)
	ax.set_ylabel(ylabs)
	ax.plot(xval, yval, color=color, label=name)
	ax.legend()


def fhan(x1,x2,r,h):

	#Calculate the output limit.
	d = r*h*h

	#Estimate the velocity.
	a0 = h*x2

	#Estimate the output.
	y = x1 + a0

	# a1 means limit of velocity.
	# a2 means optimized velocity
	a1 = math.sqrt(d*(d+8*abs(y)))
	a2 = a0 + sign(y)*(a1-d)/2

	# Calculate the final delta of x2 :a.
	# If outof d, a is a2
	# If inside d, a is a0+y
	a = (a0 + y)*fsg(y,d) + a2*(1 - fsg(y,d))

	# Calculate the final delta of x2.
	# If outof d, the increment of x2 is r*sign(a)
	# If inside d, fh is r*(a/d)
	output = -r * (a/d) * fsg(a,d) - r * sign(a)*(1-fsg(a,d))
	return output

#
#Setup function
#
def setup():
	
	#set cycle times
	size = 2

	#set X axis value
	X  = list(np.arange(-size,size,0.1))

	#TD
	Y_y0  = list(np.arange(-size,size,0.1))
	Y_y1  = list(np.arange(-size,size,0.1))
	Y_y2  = list(np.arange(-size,size,0.1))
	cnt = 0
	for k in X:

		# Y_y0[cnt] = fhan(k,100,300000,0.05)
		# Y_y1[cnt] = fhan(k,30,300000,0.05)
		# Y_y2[cnt] = fhan(k,10,300000,0.05)
		Y_y0[cnt] = fal(k,1.5,0.001)
		Y_y1[cnt] = fal(k,0.5,0.001)
		Y_y2[cnt] = fal(k,-0.5,0.001)
		cnt+=1

	fig = plt.figure()
	graph_display(fig,1,1,1,X,Y_y0,"fal0","cycle time","rate",'red')
	graph_display(fig,1,1,1,X,Y_y1,"fal1","cycle time","rate",'blue')
	graph_display(fig,1,1,1,X,Y_y2,"fal2","cycle time","rate",'green')
	plt.show()


if __name__ == "__main__":
	setup()
