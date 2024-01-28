import os
import shutil

# source_folder_path = f'F:/Target_detection/yolov5/yolov5-master/runs/detect/images'
# save_folder_name = f'image_5'

source_folder_path = f'F:/Target_detection/yolov5/yolov5-master/runs/detect/labels'
save_folder_name = f'labels'

target_folder_path = f'F:/Target_detection/yolov5/yolov5-master/runs/1'
match_keyword = f'36_frame'


def copy_matching_files_startswith(source_folder, target_folder, match_start, save_folder):
    target_subfolder = os.path.join(target_folder, save_folder)

    # 确保目标子文件夹存在
    os.makedirs(target_subfolder, exist_ok=True)

    # 遍历源文件夹中的所有文件
    copied_files_count = 0
    for file in os.listdir(source_folder):
        # 检查文件名是否以指定的字符串开头
        if file.startswith(match_start):
            source_file_path = os.path.join(source_folder, file)
            target_file_path = os.path.join(target_subfolder, file)

            # 复制文件
            shutil.copy2(source_file_path, target_file_path)
            copied_files_count += 1

    if copied_files_count > 0:
        print(f"Copied {copied_files_count} files to '{target_subfolder}'.")
    else:
        print("No matching files found to copy.")


if __name__ == "__main__":
    copy_matching_files_startswith(source_folder_path, target_folder_path, match_keyword, save_folder_name)
