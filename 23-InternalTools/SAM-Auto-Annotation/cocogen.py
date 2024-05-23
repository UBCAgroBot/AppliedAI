import pandas as pd, numpy as np, json, glob, os, sys

anpt = sys.argv[1]
if anpt[-1] != "/":
	anpt = f'{anpt}/'

masks = glob.glob(f'{anpt}*.txt')
for i in range(len(masks)):
	masks[i] = masks[i].replace("\\","/")

imcounter = 1
ancounter = 1
imgid = 1
jsimgs = {"images": [], "annotations": [], "categories": [{"id": 1, "name": "Grape Bunch"}]}
for i in masks:
	filename = i.split("/")[-1][:-3]
	imdict = {"file_name": f'{filename}jpg, "height": 500, "width": 500, "id": imcounter}
	imcounter += 1
	jsimgs['images'].append(imdict)
	
	try:
		labels = pd.read_table(i, sep='|', header=None)
	except:
		continue
	labels = [(np.array(labels[0][i].split(' ')
                           ).astype(np.double)[1:]
                  ).reshape(-1,2)
                 for i in range(labels.shape[0])]
	for j in labels:
		andict = {"id": ancounter, "image_id": imgid, "segmentation": [[float(k) for k in 500*j.reshape(-1)]],
                  "bbox": [500.*float(k) for k in [*np.min(j, axis=0),
                                            *np.abs(np.max(j, axis=0)
                                                    -np.min(j, axis=0))]],
                  "category_id": 1, "iscrowd": 0}
		jsimgs['annotations'].append(andict)
		ancounter += 1
	imgid += 1
	
with open(f'{anpt}annotations.json', 'w') as f:
    f.write(json.dumps(jsimgs))
