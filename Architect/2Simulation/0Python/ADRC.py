import numpy as np
import matplotlib.pyplot as plt
import math
import random


#public function
#
def sign(val):
	
	if val>1e-6:
		val  = 1
	elif val < -1e-6:
		val = -1
	else:
		val = 0

	return val

#zone-functon
def fsg(x,d):

	output = (sign(x+d) - sign(x-d))/2

	return output

#power function
def fal(e,alpha,zeta):

	s = (sign(e+zeta)-sign(e-zeta))/2

	fal_output = e*s/(pow(zeta,1-alpha))+pow(abs(e),alpha)*sign(e)*(1-s)

	return fal_output



######################################################################
#
#class td filter
#
class ADRC_TD():

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
	# TD tracker
	#
	# x1(k+1) = x1(k) + h * x2(k)
	# x2(k+1) = x2(k) - r0 * u(k)
	# fhan(x1,x2,r0,h0)

	def fhan(self,excpt):

		x1_delta = self.x1 - excpt
		self.h0 = self.N0 * self.h
		d = self.r * self.h0 * self.h0
		a0 = self.x2 * self.h0
		y = x1_delta + a0

		a1 = math.sqrt(d*(d+8*abs(y)))
		a2 = a0 + sign(y)*(a1-d)/2
		a = (a0 + y)*fsg(y,d) + a2*(1 - fsg(y,d))

		self.fh = -self.r * (a/d) * fsg(a,d) - self.r * sign(a)*(1-fsg(a,d))

		self.x1 = self.x1 + self.h * self.x2
		self.x2 = self.x2 + self.h * self.fh
#
#class ESO
#
class ADRC_ESO():
	"""docstring for ADRC_ESO"""
	def __init__(self,beta01,beat02,beta03,z1,b0):
		self.beta01 = beta01
		self.beta02 = beta02
		self.beta03 = beta03
		self.b0 = b0
		self.e = 0.0

	def fleso(self):
		eso.e = eso.z1 - eso.y
		#update observe
		eso.z1 += eso.z2 - eso.beta01 * eso.e
		eso.z2 += eso.z3 - eso.beta02 * eso.e + eso.b * eso.u
		eso.z3 += -eso.beta03*eso.e

#
#class NL
#
class ADRC_NL():
	"""docstring for ADRC_NL"""
	def __init__(self,beta0,beta1,beat2,N1,C,alpha1,alpha2,zeta,b):
		self.beta0 = beta0
		self.beta1 = beta1
		self.beta2 = beta2
		self.N1 = N1
		self.C = C
		self.alpha1 = alpha1
		self.alpha2 = alpha2
		self.zeta = zeta
		self.b = b



#
#Setup function
#
def setup():
	
	w0 = 1
	b1 = 3*w0
	b2 = 3*w0*w0
	b3 = w0*w0*w0
	print('b1=%f,b2=%f,b3=%f' %(b1,b2,b3))
	
	#r h N0 C
	td = ADRC_TD(300000.0,0.01,3.0,1.0);
	
	#set cycle times
	size=500

	#set X axis value
	X  = np.array(range(0,size))

	#TD
	Y_TD_h0  = np.array(range(size), dtype = float)
	Y_TD_a0  = np.array(range(size), dtype = float)
	Y_TD_s   = np.array(range(size), dtype = float)
	Y_TD_fh  = np.array(range(size), dtype = float)
	Y_TD_x1  = np.array(range(size), dtype = float)
	Y_TD_x2  = np.array(range(size), dtype = float)
	Y_TD_fh  = np.array(range(size), dtype = float)

	for k in np.arange ( size ):
		Y_TD_s[k]  = 1000*math.sin(k%180/57.29) + random.randint(-200,200)
		#execute td
		td.fhan(Y_TD_s[k])

		Y_TD_h0[k] = td.h0
		Y_TD_fh[k] = td.fh
		Y_TD_x1[k] = td.x1
		Y_TD_x2[k] = td.x2
		Y_TD_fh[k] = td.fh

	fig = plt.figure()
	ax1 = fig.add_subplot(3, 2, 1)
	ax2 = fig.add_subplot(3, 2, 3)
	ax3 = fig.add_subplot(3, 2, 5)
	ax4 = fig.add_subplot(3, 2, 2)
	ax5 = fig.add_subplot(3, 2, 4)
	ax6 = fig.add_subplot(3, 2, 6)

	ax1.set_xlabel("cycle time")
	ax1.set_ylabel("rate")
	ax1.plot(X, Y_TD_fh, color='red', label='fh')
	ax1.legend()

	ax2.set_xlabel("cycle time")
	ax2.set_ylabel("rate")
	ax2.plot(X, Y_TD_x1,  color='green', label='x1')
	ax2.plot(X, Y_TD_s,  color='red', label='signal')
	ax2.legend()

	ax3.set_xlabel("cycle time")
	ax3.set_ylabel("rate")
	# ax3.plot(X, Y_TD_fh,  color='blue', label='fh')
	ax3.plot(X, Y_TD_x2,  color='blue', label='x2')	
	ax3.legend()

	plt.show()


if __name__ == "__main__":
	setup()
