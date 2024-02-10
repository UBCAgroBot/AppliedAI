import os

def change_class_yolo_annotation(annotation_file, new_class):
    with open(annotation_file, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        line = line.strip().split()
        if line:
            line[0] = str(new_class)
            new_lines.append(' '.join(line))

    with open(annotation_file, 'w') as file:
        file.write('\n'.join(new_lines))

def change_class_in_folder(folder_path, new_class):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            annotation_file = os.path.join(folder_path, file_name)
            change_class_yolo_annotation(annotation_file, new_class)


folder_path = '/path/to/your/folder'
new_class = 1  # The new class you want to assign
change_class_in_folder(folder_path, new_class)
