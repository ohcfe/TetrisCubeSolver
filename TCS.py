#!/opt/local/bin/python
import os
import itertools
import time
import numpy as np
from pieces import piece

#get the pieces from the file
pieces = {}
for i in os.listdir('.'):
	if i.count('piece') and i.count('dat'):
		pieces[int(i.split('piece')[1].split('.dat')[0])]={'p0':piece(filename=i)}

#Compute all possible orientations for each piece
print "Calculating orientations"
for i in pieces:
	pieces[i]['ori'] = []
	#rotate about axis 1 to access all four faces
	for j in [0,90,180,270]:
		P=pieces[i]['p0'].rotate(1,j)
		for k in [0,90,180,270]:
			pieces[i]['ori'].append(P.rotate(0,k))
	for j in [90,270]:
		P=pieces[i]['p0'].rotate(2,j)
		for k in [0,90,180,270]:
			pieces[i]['ori'].append(P.rotate(0,k))

#compute all possible solutions
print "padding with zeros"
for i in pieces:
	pieces[i]['confs'] = []
	for j in pieces[i]['ori']:
		pieces[i]['confs'].extend(j.PadWithZeros())

print "finding solutions"
pool = []
for i in pieces:
	pool.append(pieces[i]['confs'])
SolCount = 0
for i in itertools.product(*pool):
	S = piece()
	for j in i:
		S=S+j
	if (S.shape.min() == 1 and S.shape.max() == 1):
		Sout=np.zeros((4,4,4),int)
		print "Solution #%d"%(SolCount)
		for n,i in enumerate(pieces):
			Sout = Sout + i*pieces[i]['confs'][count[n]].shape
		SolCount = SolCount + 1
		print Sout
