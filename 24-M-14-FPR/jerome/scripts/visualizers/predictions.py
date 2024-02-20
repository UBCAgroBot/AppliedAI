import matplotlib.pyplot as plt
import torch

from torchvision.utils import draw_bounding_boxes
from torchvision.io import read_image
from aug import get_transform
from models.mask_rcnn import get_model_instance_segementation

image = read_image("data/PNGImages/FudanPed00046.png")
eval_transform = get_transform(train=False)
device = torch.device('cpu')
num_classes = 2

# load model
model = get_model_instance_segementation(num_classes)
model.to(device)
model.load_state_dict(torch.load('./saved_models/model_mask_rcnn.pth'))

model.eval()
with torch.no_grad():
    x = eval_transform(image)
    x = x[:3, ...].to(device)
    predictions = model([x, ])
    pred = predictions[0]

# (image - image.min()) / (image.max() - image.min()) regularizies all 
# values of the image to between 0 and 1 inclusive (max == 1, min == 0)
# Multiplying by 255 gives us a newly generated image whose pixel values 
# range from 0 to 255 (which is conventional for many image formats)
image = (255.0 * (image - image.min()) / (image.max() - image.min())).to(torch.uint8)

pred_boxes = pred["boxes"].long()
pred_labels = [f"pedestrian: {score: .3f}" for label, score in \
               zip(pred["labels"], pred["scores"])]
output_image = draw_bounding_boxes(image, pred_boxes, pred_labels, colors="green")

plt.figure(figsize=(12, 12))
plt.imshow(output_image.permute(1, 2, 0))
plt.show()


