from matplotlib import pylab
from pylab import * #pip install numpy matpoltlib scipy
from PIL import Image #pip install pillow
from scipy.stats import kurtosis, skew #pip install scipy

def getBits(n): #takes a number and returns a binary string of 6 digits with leading zeros if the binary string has less then 6 digits
	return bin(n)[2:].zfill(6)

def getData(): #Using the current file hiarchy I have created for this project, it reads through the first 9 training examples of each subject and returns an matrix containing each image's feature vector
	root = "../database/S"
	data = np.empty([360,5])
	pos = 0 #Kepts track of which row to place the vectors on

	for i in range(1,41):
		path = root + str(i) + "/"
		label = getBits(int(i))
		for j in range(1,10):
			file = path + str(j) + ".bmp"
			mat = array(Image.open(file)).flatten() #data flattened to play nice with skew and kurtosis. also simply easier to work with
		
			data[pos][0] = np.median(mat)
			data[pos][1] = np.mean(mat)
			data[pos][2] = np.var(mat)
			data[pos][3] = skew(mat)
			data[pos][4] = kurtosis(mat)
			pos += 1 
	return data

def normalize(mat): #takes a matrix (the matrix of feature vectors) and normalizes the data in relation to its columns (by feature). Returns the normalized matrix
	matT = matrix.transpose(mat) #Transposing the matrix makes it shorter for me to write this function (barring any python tricks Im not aware of)
	m,n = matT.shape #size of transposed matrix.
	
	arr = np.empty([n,m]) #this is the array that will be retuned, I comment this because Im making it the same size as the original matrix mat
	
	#This forloop normalizes the value of in the transposed matrix matT and place them in their proper spot in the matrix that will be returned
	for i in range(0,m): 
		high = max(matT[i]) #max of row i
		low  = min(matT[i]) #min of row i
		for j in range(0,n):
			arr[j][i] = (matT[i][j] - low) / (high - low)
	return arr

def writeData(mat): #Takes a matrix and writes its contents to a file, with subject labeling
	data = open("training.data", "w+") #opens file with write access to that file

	n,m = mat.shape 

	subject = 0 #kepts track of what subject we are on 

	#prints all the information to file with proper formating and 4 leading zeros
	for i in range(0,n):
		data.write(str.format('{0:.4f}', mat[i][0]) + ", ")
		data.write(str.format('{0:.4f}', mat[i][1]) + ", ")
		data.write(str.format('{0:.4f}', mat[i][2]) + ", ")
		data.write(str.format('{0:.4f}', mat[i][3]) + ", ")
		data.write(str.format('{0:.4f}', mat[i][4]) + "  ")
		if(i % 9 == 0): #This always runs on the first loop. I could have skiped the single always run if statement but I felt this was more readable
			subject += 1
		label = getBits(subject) #returns binary string of subject
		for j in range(0,6):
			data.write(label[j] + ".0") #the ".0" is just for formating
			if j != 6: 
				data.write(" ") #also just for formatting so that each part of the 'label' has a space inbetween it
		data.write("\n") #formatting so each image is on its own line


writeData(normalize(getData()))


			