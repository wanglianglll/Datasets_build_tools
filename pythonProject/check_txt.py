import os

# 待检测文件夹
check_path = r'F:\Target_detection\datasets\RPS_Dataset\label'


def is_empty_txt(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return not content.strip()  # 判断内容是否为空或只包含空白字符
    except IOError:
        # 文件无法打开，可能是不存在或者其他问题
        return True


def delete_empty_txt(file_path):
    try:
        os.remove(file_path)
        print(f"The text file '{file_path}' is empty and has been deleted.")
    except Exception as e:
        print(f"Failed to delete the empty text file '{file_path}': {e}")


def check_empty_txt(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            if is_empty_txt(file_path):
                print(f"The text file '{filename}' is empty.")
                delete_empty_txt(file_path)


if __name__ == "__main__":
    check_empty_txt(check_path)
