# std_msgs/Header header
# since ros messages can only be 1D arrays, the 2d array gets flattened

int32 BOX_WIDTH=4 #width of each box 
int32[] box  # [x1, y1, x2, y2] top left bottom right
float32[] scores # confidence score of each box
int32[] class_num # class number of each box