import cv2
import xml.etree.ElementTree as ET
import os

# Navigate three parent directories up
parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))

# Step 1: Parse the XML File
tree = ET.parse(os.path.join(parent_directory, 'Hermos', 'Images', 'IMG_8165.xml'))  # Edit to your XML file
root = tree.getroot()

# Step 2: Read the Image
image = cv2.imread(os.path.join(parent_directory, 'Hermos', 'Images', 'IMG_8165.jpg')) # Change to your image file

# Step 3: Extract Annotation Data
for annotation in root.findall('.//object'):
    xmin = int(annotation.find('.//xmin').text)
    ymin = int(annotation.find('.//ymin').text)
    xmax = int(annotation.find('.//xmax').text)
    ymax = int(annotation.find('.//ymax').text)
    name = annotation.find('.//name').text  # Extract the name

    # Step 4: Overlay Annotations
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)  # Draw a green rectangle

    # Step 5: Overlay the Name
    cv2.putText(image, name, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)  # Draw the name in red text



# Step 6: Display or Save the Image
cv2.imshow('Image with Annotations', image)
cv2.waitKey(0)
cv2.destroyAllWindows()