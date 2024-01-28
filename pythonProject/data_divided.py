import os
import random
import shutil

def create_dataset_structure(dataset_dir):
    # 创建images和labels文件夹
    os.makedirs(os.path.join(dataset_dir, 'images', 'train'), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, 'images', 'test'), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, 'labels', 'train'), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, 'labels', 'test'), exist_ok=True)

def split_dataset(image_dir, label_dir, train_ratio=0.8):
    # 获取所有图像和标签的文件名列表
    image_files = os.listdir(image_dir)
    label_files = os.listdir(label_dir)

    # 确保图像和标签文件名相对应
    image_files.sort()
    label_files.sort()

    # 随机打乱数据集
    combined_data = list(zip(image_files, label_files))
    random.shuffle(combined_data)
    image_files[:], label_files[:] = zip(*combined_data)

    # 计算分割点
    split_index = int(len(image_files) * train_ratio)

    # 将数据分配到训练集和测试集
    train_images = image_files[:split_index]
    test_images = image_files[split_index:]
    train_labels = label_files[:split_index]
    test_labels = label_files[split_index:]

    return train_images, test_images, train_labels, test_labels

def move_data(source_dir, destination_dir, file_list):
    for file_name in file_list:
        source_path = os.path.join(source_dir, file_name)
        destination_path = os.path.join(destination_dir, file_name)
        shutil.move(source_path, destination_path)

def main():
    # 请替换为你的图像和标签文件夹路径
    image_source_dir = r'F:\Target_detection\datasets\RPS_Dataset\images'
    label_source_dir = r'F:\Target_detection\datasets\RPS_Dataset\label'

    # 请替换为你的数据集目录
    dataset_dir = r'F:\Target_detection\datasets\car_with_color'

    # 创建目录结构
    create_dataset_structure(dataset_dir)

    # 划分数据集
    train_images, test_images, train_labels, test_labels = split_dataset(image_source_dir, label_source_dir)

    # 将数据移动到相应的文件夹
    move_data(image_source_dir, os.path.join(dataset_dir, 'images', 'train'), train_images)
    move_data(image_source_dir, os.path.join(dataset_dir, 'images', 'test'), test_images)
    move_data(label_source_dir, os.path.join(dataset_dir, 'labels', 'train'), train_labels)
    move_data(label_source_dir, os.path.join(dataset_dir, 'labels', 'test'), test_labels)

if __name__ == "__main__":
    main()
