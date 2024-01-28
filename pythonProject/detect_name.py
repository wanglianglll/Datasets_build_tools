import os

# 图像文件夹
image_path = r'F:\Target_detection\datasets\HEU_Month1\images'
# 标签文件夹
label_path = r'F:\Target_detection\datasets\HEU_Month1\label'

def compare_and_keep_intersection(large, small):
    for large_file in os.listdir(large):
        large_file_name = os.path.splitext(large_file)[0]  # 获取文件名（去掉扩展名）
        found = False

        for small_file in os.listdir(small):
            small_file_name = os.path.splitext(small_file)[0]

            if large_file_name == small_file_name:
                found = True
                break

        if not found:
            file_to_remove = os.path.join(large, large_file)
            print(f"Removing file: {file_to_remove}")
            os.remove(file_to_remove)

# 1. 判断文件个数
count1 = len([f for f in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, f))])
count2 = len([f for f in os.listdir(label_path) if os.path.isfile(os.path.join(label_path, f))])

if count1 > count2:
    large_folder = image_path
    small_folder = label_path
else:
    large_folder = label_path
    small_folder = image_path

# 2. 从大文件中检测并删除
compare_and_keep_intersection(large_folder, small_folder)
