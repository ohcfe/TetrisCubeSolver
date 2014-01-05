#!/opt/local/bin/python
import os
import numpy as np

class piece:
	#initialize the piece from a file
	def __init__(self, **kwargs):
		"""
		Initializes the parts shape from the datafile and
		trims any excess zeros from the end of each axis
		The final trimmed array is stored in self.shape
		"""
		if kwargs.keys().count('filename'):
			filename = kwargs['filename']
			infile = open(filename,'r')
			#A is a 4x4x4 array with indicies i,j,and k
			# the .dat files are a 4x4x4 matrix of 0 or 1
			A=np.zeros((4,4,4), int)
			#each line of the file reads in one row(i) of A
			j = 0
			k = 0
			for l in infile.readlines():
				try:
					a = map(int,l.strip().split(' '))
					for i,x in enumerate(a):
						A[k,j,i] = x
					j += 1
					if j > 3:
						j = 0
						k += 1
				#file may contain empty lines which throw ValueError
				except ValueError:
					pass # do nothing for empty lines
			A = self.TrimZeros(A,0)
			A = self.TrimZeros(A,1)
			A = self.TrimZeros(A,2)
			self.shape = A
		if kwargs.keys().count('shape'):
			self.shape = kwargs['shape']
		
	def TrimZeros(self, A, axis):
		"""
		Trims the zeros off of the end of the axis of a 3d array
		"""
		if axis == 0:
			if np.any(A[-1,:,:]):
				return A
			else:
				return self.TrimZeros(A[:-1,:,:],0)
		elif axis == 1:
			if np.any(A[:,-1,:]):
				return A
			else:
				return self.TrimZeros(A[:,:-1,:],1)
		elif axis == 2:
			if np.any(A[:,:,-1]):
				return A
			else:
				return self.TrimZeros(A[:,:,:-1],2)
		else:
			raise ValueError("axis must be 0, 1 or 2")


	def __str__(self):
		s = self.shape.shape
		A = self.shape
		string = "%5s %5s\n"%("Top", "side")
		for i in np.arange(0,s[1]):
			topstr = ''
			sidestr = ''
			for j in np.arange(0,s[2]):
				 topstr=topstr+"%d"%(A[:,i,j].max())
			for j in np.arange(0,s[0]):
				sidestr=sidestr+"%d"%(A[j,i,:].max())
			string = string + "%5s %5s\n"%(topstr,sidestr)
		string = string+"%5s"%("Front\n")	
		for i in np.arange(0,s[0]):
			frontstr = ''
			for j in np.arange(0,s[2]):
				frontstr = frontstr+"%d"%(A[i,:,j].max())
			string = string + "%5s\n"%(frontstr)
		return string

	def rotate(self, axis, degree):
		"""
		Rotates the shape by 90, 180, or 270 degrees around
		axis 0, 1, or 2
		returns the rotated piece

		Parameters: 
			degree: 0	 90deg rotation
				1	180deg rotation	
				2	270deg rotation

			axis:	0	around z
				1	around x
				2	around y
		"""
		if axis == 0:
			if degree == 90:
				return piece(shape=self.shape.transpose(0,1,2)[:,:,::-1])
			elif degree == 180:
				return piece(shape=self.shape.transpose(0,1,2)[:,:,::-1].transpose(0,1,2)[:,:,::-1])
			elif degree == 270:
				return piece(shape=self.shape.transpose(0,1,2)[:,::-1,:])
			else:
				raise ValueError("only rotations of 90, 180, or 270 degrees are allowed")
		elif axis == 1:
			return self.shape #placeholder
		elif axis == 2:
			return self.shape #placeholder
		else:
			raise ValueError("axis must be 0, 1, or 2")

	

#p12 = piece(filename="piece12.dat")
#print p12
#print p12.rotate(0,1)
