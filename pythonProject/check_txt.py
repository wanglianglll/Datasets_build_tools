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


def adjust_and_save_content(file_path, lines):
    try:
        with open(file_path, 'w') as file:
            for line in lines:
                values = line.strip().split()
                # Skip the line if the class label is '1'
                if values[0] == '1':
                    continue
                adjusted_values = [values[0]]  # Keeping the class label as it is
                for value in values[1:]:
                    adjusted_value = max(min(float(value), 1.0), 0.0)
                    adjusted_values.append(str(adjusted_value))
                file.write(" ".join(adjusted_values) + "\n")
            print(f"Adjust file :'{file_path}'")
    except Exception as e:
        print(f"Error while adjusting and saving content of '{file_path}': {e}")


def check_and_adjust_content(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            adjusted = False
            new_lines = []  # To store lines after adjustment and filtering
            for i, line in enumerate(lines):
                values = line.strip().split()
                for j, value in enumerate(values[1:]):  # Assuming values[0] is the class label
                    if not 0.0 <= float(value) <= 1.0:
                        adjusted = True
                        adjusted_value = max(min(float(value), 1.0), 0.0)
                        values[j + 1] = str(adjusted_value)  # Adjust the value
                new_lines.append(" ".join(values))  # Update the line with adjusted values
            if adjusted:
                adjust_and_save_content(file_path, new_lines)
    except Exception as e:
        print(f"Error while checking and adjusting content of '{file_path}': {e}")


def check_empty_txt(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            if is_empty_txt(file_path):
                print(f"The text file '{filename}' is empty.")
                delete_empty_txt(file_path)
            else:
                check_and_adjust_content(file_path)


if __name__ == "__main__":
    check_empty_txt(check_path)
