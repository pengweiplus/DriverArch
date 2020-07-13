import numpy as np
import matplotlib.pyplot as plt
import math
import random

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
	
	#set cycle times
	size=360

	#set X axis value
	X  = np.array(range(0,size))

	#var,std,mean
	Y_TD_var  = np.array(range(size), dtype = float)
	Y_TD_std  = np.array(range(size), dtype = float)
	Y_TD_mean   = np.array(range(size), dtype = float)
	Y_TD_s  = np.array(range(size), dtype = float)

	mean_size = 5;
	mean_arr  = np.array(range(mean_size), dtype = float)

	for k in np.arange ( size ):
		if k>180:
			k-=360
		Y_TD_s[k]  = 3*math.sin(1 * k/57.29) + random.randint(-20,20)

		#execute mean
		mean_arr[k%mean_size] = Y_TD_s[k]
		# if k%mean_size == 0:
		Y_TD_mean[k] = np.var(mean_arr)

	fig = plt.figure()
	graph_display(fig,1,1,1,X,Y_TD_s,"signal","cycle time","rate",'green')
	graph_display(fig,1,1,1,X,Y_TD_mean,"signal var","cycle time","rate",'red')
	plt.show()


if __name__ == "__main__":
	setup()
