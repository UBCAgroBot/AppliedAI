import torch
import os
from scripts.config.config import CLASSES
from torch.utils.data import Dataset
from torchvision.io import read_image
import xml.etree.ElementTree as ET

class XMLDatasetPyTorch(Dataset):
    def __init__(self, image_dir, transforms=None):
        self.image_dir = image_dir
        self.transforms = transforms

        images_and_xml = list(sorted(os.listdir(image_dir)))[:10] # TODO - remove

        self.images = []
        self.xml = []
        for idx in range(0, len(images_and_xml), 2):
          self.images.append(images_and_xml[idx])
          self.xml.append(images_and_xml[idx+1])

    def __len__(self):
        return len(self.xml)

    def __getitem__(self, idx):
        img_path = self.image_dir + '/' + self.images[idx]
        xml_path = self.image_dir + '/' + self.xml[idx]

        image = read_image(img_path)
        annotations = self.parse_xml(xml_path)

        if self.transforms:
          image = self.transforms(image)
        
        target = {}
        target["boxes"] = torch.tensor(annotations['boxes'], dtype=torch.float32)
        target["labels"] = torch.tensor(annotations['labels'], dtype=torch.int64)
        
        return image, target

    def parse_xml(self, xml_file_path):
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        annotations = { "boxes": [], "labels": [] }
        filename = root.find('filename').text
        annotations["filename"] = filename

        for obj in root.findall('object'):
            xmin = float(obj.find('bndbox').find('xmin').text)
            xmax = float(obj.find('bndbox').find('xmax').text)
            ymin = float(obj.find('bndbox').find('ymin').text)
            ymax = float(obj.find('bndbox').find('ymax').text)
            annotations["boxes"].append([xmin, ymin, xmax, ymax])
            annotations["labels"].append(CLASSES[obj.find('name').text.lower()])
        return annotations

# TODO - XML Dataset tensorflow after successful PyTorch workflow