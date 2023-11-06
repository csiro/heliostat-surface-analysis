import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from stl.mesh import Mesh

def set_plot_font_size(ax,size,includeLegend=False,includeColorbar=False):
	items = [ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels(which="both") + ax.get_yticklabels(which="both")
	if includeLegend:
		items += ax.legend().get_texts()
	for item in items:
		item.set_fontsize(size)
	if includeColorbar:
		im = ax.images
		if len(im)>0:
			cb = im[-1].colorbar 
			cb.ax.tick_params(labelsize=size)

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
	
def plot_2d_surface(mesh : Mesh, values : np.ndarray, label : str, ax : plt.Axes = None, fontsize : int = None, cbxy = (3.5,0.29)):
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
	if fontsize==None:
		cbar = plt.colorbar(tpc,label=label)
	else:
		cbar = plt.colorbar(tpc)
		cbar.ax.set_title(label=label,fontsize=fontsize,rotation=90,x=cbxy[0],y=cbxy[1])
	#
	if fontsize!=None:
		cbar.ax.tick_params(labelsize=fontsize)
		set_plot_font_size(ax,fontsize)
	#
	if ax==None:
		plt.show()