import os
from random import uniform

f = 29.
h = 2.44
w = 1.85
ns = [99,999,9999,99999]
alphabet = "abcdefghij"

for l,n in zip(alphabet,ns):
	ofile = open("scans/%s_n%d.txt"%(l.upper(),n),"w")
	for i in range(n):
		x = uniform(-0.5*w,0.5*w)
		y = uniform(-0.5*h,0.5*h)
		z = ( x**2 + y**2 ) / 4. / f
		ofile.write("%e\t%e\t%e\n"%(x,y,z))
	ofile.close()
