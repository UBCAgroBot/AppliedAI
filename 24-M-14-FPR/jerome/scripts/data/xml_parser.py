class XMLParser:
    def __init__(self, xml: XML):
        self.xml = xml

class XML:
  def __init__(self):
     # TODO


# Since the number of input neurons to a network is fixed, I need the images 
# and their bounding boxes to all be resized to the correct size
# I need to extract the bounding boxes of each image

# boxes generated in masks_to_boxes func in dataset are in below format: 
# tensor([[227., 157., 369., 435.],
#       [ 38., 178., 114., 362.]])

# REQUIREMENTS:
# 1. All images must be resized to specified dimensions 
# 2. All bounding boxes must also be rescaled based on the resizing applied in 1. 
# 3. A 1:1 correspondence between the bounding box in question and its label
# .  should be maintained
