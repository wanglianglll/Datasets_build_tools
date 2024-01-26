# Datasets-build tools
## Fils：
### 1.Chinese_to_pinyin.py
### 2.xml_to_txt.py
### 3.check_txt.py
### 4.detect_name.py
### 5.data_divided.py
## Introduction:
### 1:To convert the Chinese names of all files in the folder to Pinyin (including subfolders)
### 2:To convert xml tags in the folder to txt tags (yolo format)
### 3:To detect whether the txt file in a specific folder has an empty folder or whether the label parameter is out of bounds (less than 0 or greater than 1) ,delete all empty files and reset exception parameters
### 4:To detect whether the prefix names in the image folder and label folder are the same, and force them to be deleted into the intersection of the two
### 5:To proportionally divide the image folder and labels folder into yolo format datasets
