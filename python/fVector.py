from matplotlib import pylab
from pylab import *
from PIL import Image
from scipy.stats import kurtosis, skew

def getBits(n):
	return bin(n)[2:].zfill(6)

def getData():
	root = "../database/S"
	data = np.empty([360,5])
	pos = 0

	for i in range(1,41):
		path = root + str(i) + "/"
		label = getBits(int(i))
		for j in range(1,10):
			file = path + str(j) + ".bmp"
			mat = array(Image.open(file)).flatten()
		
			data[pos][0] = np.median(mat)
			data[pos][1] = np.mean(mat)
			data[pos][2] = np.var(mat)
			data[pos][3] = skew(mat)
			data[pos][4] = kurtosis(mat)
			pos += 1
	return data

def normalize(mat):
	matT = matrix.transpose(mat)
	m,n = matT.shape
	
	arr = np.empty([n,m])
	
	for i in range(0,m):
		high = max(matT[i])
		low  = min(matT[i])
		for j in range(0,n):
			arr[j][i] = (matT[i][j] - low) / (high - low)
	return arr

def writeData(mat):
	data = open("training.data", "w+")

	n,m = mat.shape

	subject = 0
	for i in range(0,n):
		data.write(str.format('{0:.4f}', mat[i][0]) + ", ")
		data.write(str.format('{0:.4f}', mat[i][1]) + ", ")
		data.write(str.format('{0:.4f}', mat[i][2]) + ", ")
		data.write(str.format('{0:.4f}', mat[i][3]) + ", ")
		data.write(str.format('{0:.4f}', mat[i][4]) + "  ")
		if(i % 9 == 0):
			subject += 1
		label = getBits(subject)
		for j in range(0,6):
			data.write(label[j] + ".0")
			if j != 6: 
				data.write(" ")
		data.write("\n")


writeData(normalize(getData()))


			