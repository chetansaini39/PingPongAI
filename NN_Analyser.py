import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class NN_Analyser:
    'Class for Neural Net'
    fileToRead=''
    def __init__(self, fileToRead):
        self.fileToRead=fileToRead

    def readFile(self):
        fileRead=open(self.fileToRead,'r',1)
        for line in fileRead:
            print line

dataFrame= pd.read_csv('dataSet.csv')
dataNP=np.array(dataFrame)#store dataframe into np

print 'rows, cols', dataNP.shape  # row and cols
print 'dataNP.ndim', dataNP.ndim  # number of axes /dimesnion
print 'data type', dataNP.dtype
X=dataNP[:,0:19]
Y=dataNP[:,19]
plt.figure()
plt.plot(X[1] )
plt.show()
