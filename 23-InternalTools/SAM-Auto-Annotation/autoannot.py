from ultralytics.data.annotator import auto_annotate
import torch, numpy as np, pandas as pd
import glob, os, sys

imdir = f'{sys.argv[1]}/'.replace("\\","/") # make sure this points to where your images are
    # RELATIVE TO WHERE THIS NOTEBOOK IS
outdir = f'{sys.argv[2]}/'.replace("\\","/") # can be anything, really. I suggest pointing to someplace
    # inside imdir because it's just nicely organised that way.
if len(sys.argv)>3 and sys.argv[3].lower()=="true":
	outdir = f'{imdir}{outdir}'
	
try:
	os.mkdir(outdir) # spares you the trouble of creating outdir yourself.
except:
	None
auto_annotate(imdir,
              'yolov8x.pt',
              'sam_l.pt',
              output_dir=outdir) # where the magic begins.

for path in glob.glob(f'{outdir}/*.txt'):
	path = path.replace("\\","/")
	try:
		labels = pd.read_table(path, sep='|', header=None) # Reads in annotations as a 1-by-n DataFrame
        # where each detected object (i.e. row in the .txt file) appears as one long string on a
        # separate row.
	except:
		print(f'Note: \"{path}\" is an empty file or does not exist.')
		continue
	labels = [np.array(labels[0][i].split(' ')).astype(np.double)[1:].reshape(-1,2) for i in range(labels.shape[0])] # Uses string operations to turn the DataFrame into
                # a list of numpy arrays where each array corresponds to a detected object 
                # (i.e. row in the .txt file). Each array is reshaped to n-by-2 as the floats appear
                # in (x, y) pairs in the .txt file.
	labels = np.array([[i.min(0), i.max(0)] for i in labels]) # Extracts the minimum and maximum x
                # and y values in each numpy array and turns the previous list into a list of these
                # mins and maxes
    
    # Finds the centre of each bounding box, as well as the width and height of the box.
	pcs = np.array([[i.mean(0)] for i in labels]).reshape(-1,2)
	ws = np.array([[i[1,0]-i[0,0]] for i in labels]).reshape(-1)
	hs = np.array([[i[1,1]-i[0,1]] for i in labels]).reshape(-1)
    
    # Writes the values found above as a line in a new .txt file. If the original annotation
    # had multiple objects, a separate line is written in for each object.
	out = path.split("/")[-1] # String operation on the supplied path to extract the file name.
	rootdir = path.split(out)[0] # String operation on the supplied path to extract the directory
        # the image resides in.
	try:
		os.mkdir(f'{rootdir}YOLO') # Creates the YOLO subfolder if it doesn't already exist.
	except:
		None
	with open(f'{rootdir}YOLO/{out}', 'w') as f: 
		'''CHANGE LINES 48 AND 51 if you want to use a different structure with your directories. Of course, you can add functionality to be able to specify any output directory if you feel like that's more useful.'''
		for i in range(len(pcs)): # Ensures every object gets a line in the YOLO-formatted .txt
			f.write(f'0 {pcs[i][0]} {pcs[i][1]} {ws[i]} {hs[i]}\n') # Prints "0" as an arbitrary
                # class label, followed by the YOLO-formatted bounding box.

annots = glob.glob(f'{outdir}YOLO/*.txt')
if "\\" in annots[0]:
	for i in range(len(annots)):
		annots[i] = annots[i].replace("\\", "/")
				
for i in glob.glob(f'{imdir}*.jpg'):
	path = i.replace("\\","/")
	imname = path.split("/")[-1][:-4]
	if not (f'{outdir}YOLO/{imname}.txt'
            in annots):
		with open(f'{outdir}YOLO/{imname}.txt', 'w') as f:
			f.write('')
		with open(f'{outdir}{imname}.txt', 'w') as f:
			f.write('')