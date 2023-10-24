import os

f = 27e3
rootDir = "../circular_paraboloid_peg/scans"
for item in os.listdir(rootDir):
	lines = open(os.path.join(rootDir,item),"r")
	nodes = []
	for line in lines:
		tks = line.split()
		x = float(tks[0])
		y = float(tks[1])
		z = ( x**2 + y**2 ) / 4. / f
		nodes.append([x,y,z])
	ofile = open("scans/%s"%item,"w")
	for node in nodes:
		ofile.write("%e\t%e\t%e\n"%(node[0],node[1],node[2]))
	ofile.close()
	if 1:
		ofile = open("csvs/%s"%item.replace(".txt",".csv"),"w")
		ofile.write("x,y,z\n")
		for node in nodes:
			ofile.write("%e,%e,%e\n"%(node[0]/1e3,node[1]/1e3,node[2]/1e3))
		ofile.close()
