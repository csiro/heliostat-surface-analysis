import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_points_3d(raw_x,raw_y,raw_z,x=np.ndarray(shape=(0,0)),y=np.ndarray(shape=(0,0)),z=np.ndarray(shape=(0,0)),title=None):
	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')
	ax.scatter(raw_x[:,0].tolist(),raw_y[:,0].tolist(),raw_z[:,0].tolist())
	if x.size>0 and y.size>0 and z.size>0:
		ax.scatter(x[:,0].tolist(),y[:,0].tolist(),z[:,0].tolist())
	ax.set_xlabel("x (m)")
	ax.set_ylabel("y (m)")
	ax.set_zlabel("z (m)")
	if title:
		ax.set_title(title)
	plt.show()