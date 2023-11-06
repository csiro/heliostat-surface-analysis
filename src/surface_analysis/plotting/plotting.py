import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from stl.mesh import Mesh

def plot_points_3d(raw_x: np.ndarray,
				   raw_y: np.ndarray,
				   raw_z: np.ndarray,
				   x: np.ndarray = np.ndarray(shape=(0,0)),
				   y: np.ndarray = np.ndarray(shape=(0,0)),
				   z: np.ndarray = np.ndarray(shape=(0,0)),
				   title: str = None):
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
	
def plot_2d_surface(mesh : Mesh, values : np.ndarray, label : str, ax : plt.Axes = None):
	xs = []
	ys = []
	simplices = []
	for j,triPoints in enumerate(mesh.points):
		simplex = []
		for i in range(3):
			xs.append(triPoints[i*3])
			ys.append(triPoints[i*3+1])
			simplex.append(j*3+i)
		simplices.append(simplex)
	#
	if ax==None:
		f,ax = plt.subplots()
	tpc = ax.tripcolor(xs, ys, simplices, facecolors=np.ravel(values), edgecolors='k')
	#
	ax.set_xlabel("x (m)")
	ax.set_ylabel("y (m)")
	#
	cbar = plt.colorbar(tpc, label=label)
	#
	if ax==None:
		plt.show()