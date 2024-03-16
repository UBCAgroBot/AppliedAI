import os, glob, sys, shutil as su, numpy as np

datapath = ''
trainpath = ''
testpath = ''
ratio = 1.

try:
	datapath = sys.argv[1]
	if datapath[-1] != '/':
		datapath = f'{datapath}/'
	trainpath = sys.argv[2]
	if trainpath[-1] != '/':
		trainpath = f'{trainpath}/'
	testpath = sys.argv[3]
	if testpath[-1] != '/':
		testpath = f'{testpath}/'
	ratio = float(sys.argv[4])
except:
	print(f'Error: One or more of the required paths\n(or training set size ratio) is missing.')
	
try:
	os.mkdir(trainpath)
except:
	pass

try:
	os.mkdir(testpath)
except:
	pass

imgs = glob.glob(f'{datapath}*.jpg')
ntrain = int(ratio*len(imgs))
ntest = len(imgs)-ntrain

split = np.concatenate((np.ones(ntest, dtype="int"),
                        np.zeros(ntrain, dtype="int")))

np.random.shuffle(split)

asn = [{0: trainpath, 1: testpath}[i] for i in split]

for i in range(len(imgs)):
    su.copy(imgs[i], asn[i])