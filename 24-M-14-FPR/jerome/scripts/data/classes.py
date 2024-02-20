import xml.etree.ElementTree as ET
import os
from tqdm import tqdm

classes = []
containing_half_name = []
containing_half_annotations = []

'object', 'half', 'json'

def parse_xml(xml_file_path):
    image_path = xml_file_path[:-3] + 'jpg'
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    annotations = { "boxes": [], "labels": [] }
    filename = root.find('filename').text
    annotations["filename"] = filename

    contains_half = False

    for obj in root.findall('object'):
        xmin = float(obj.find('bndbox').find('xmin').text)
        xmax = float(obj.find('bndbox').find('xmax').text)
        ymin = float(obj.find('bndbox').find('ymin').text)
        ymax = float(obj.find('bndbox').find('ymax').text)
        label = obj.find('name').text.lower()
        if label == 'half':
            annotations["boxes"].append([xmin, ymin, xmax, ymax])
        if label == 'half':
            annotations["labels"].append(label)
        if label not in classes:
            classes.append(label)
        if label == 'half':
            contains_half = True
            containing_half_name.append(image_path)
    if contains_half:
      containing_half_annotations.append(annotations)
    return annotations

images_and_xml = list(sorted(os.listdir('../../data/blueberries/all_data')))

for idx in tqdm(range(0, len(images_and_xml), 1)):
   xml_path = '../../data/blueberries/all_data' + '/' + images_and_xml[idx]
   if xml_path.endswith('.xml'):
      parse_xml(xml_path)

print("CLASSES")
print(classes)
