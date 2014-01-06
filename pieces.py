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
		elif kwargs.keys().count('shape'):
			self.shape = kwargs['shape']
		else:
			self.shape = np.zeros((4,4),int)

		
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
		return string+'\n'

	def __add__(self, other):
		return piece(shape=self.shape+other.shape)

	def rot90(self,axis):
		"""
		returns a copy of the called piece rotated by 90 degrees around axis.
		"""
		if axis == 0:
			return piece(shape=self.shape.transpose(0,2,1)[:,:,::-1])
		elif axis == 1:
			return piece(shape=self.shape.transpose(1,0,2)[::-1,:,:])
		elif axis == 2:
			return piece(shape=self.shape.transpose(2,1,0)[::-1,:,:])
		else:
			raise ValueError("axis must be 0, 1, or 2")

	def rotate(self, axis, degree):
		"""
		Rotates the shape by 90, 180, or 270 degrees around
		axis 0, 1, or 2
		returns the rotated piece

		Parameters: 
			axis:	0	around z
				1	around x
				2	around y

			degree: 90	 90deg rotation
				180	180deg rotation	
				270	270deg rotation

		"""
		if axis == 0:
			if degree == 0:
				return self
			if degree == 90:
				return self.rot90(0)
			elif degree == 180:
				return self.rotate(0,90).rotate(0,90)
			elif degree == 270:
				return self.rotate(0,90).rotate(0,90).rotate(0,90)
			else:
				raise ValueError("only rotations of 90, 180, or 270 degrees are allowed")
		if axis == 1:
			if degree == 0:
				return self
			if degree == 90:
				return self.rot90(1)
			elif degree == 180:
				return self.rotate(1,90).rotate(1,90)
			elif degree == 270:
				return self.rotate(1,90).rotate(1,90).rotate(1,90)
			else:
				raise ValueError("only rotations of 90, 180, or 270 degrees are allowed")
		if axis == 2:
			if degree == 0:
				return self
			if degree == 90:
				return self.rot90(2)
			elif degree == 180:
				return self.rotate(2,90).rotate(2,90)
			elif degree == 270:
				return self.rotate(2,90).rotate(2,90).rotate(2,90)
			else:
				raise ValueError("only rotations of 90, 180, or 270 degrees are allowed")
		else:
			raise ValueError("axis must be 0, 1, or 2")

	def PadWithZeros(self):
		L = []
		for i in range(4-self.shape.shape[0]+1):
			for j in range(4-self.shape.shape[1]+1):
				for k in range(4-self.shape.shape[2]+1):
					A = np.zeros((4,4,4),int)
					for l in range(self.shape.shape[0]):
						for m in range(self.shape.shape[1]):
							for n in range (self.shape.shape[2]):
								A[i+l,j+m,k+n]=self.shape[l,m,n]
					L.append(piece(shape=A))
		return L
