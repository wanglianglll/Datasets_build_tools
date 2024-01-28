import os
import xml.etree.ElementTree as ET

filedir = r'F:\Target_detection\datasets\RPS_Dataset\labels'
outdir = r'F:\Target_detection\datasets\RPS_Dataset\label'


def del_all_files(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            os.removedirs(c_path)
        else:
            os.remove(c_path)


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 和 / 符号
    path = path.rstrip("\\")
    path = path.rstrip("/")
    # 判断路径是否存在
    is_exist = os.path.exists(path)
    # 判断结果
    if not is_exist:
        os.makedirs(path)
    else:
        del_all_files(path)


def return_best_flag(x_expect, y_expect, armors):
    closest_armor = None
    min_distance = float('inf')  # 初始化为无限大

    for armor in armors:
        center_point = armor[1]
        x = center_point[0]
        y = center_point[1]
        distance = (x - x_expect)**2 + (y - y_expect)**2

        if distance < min_distance:
            min_distance = distance
            closest_armor = armor[0]

    return closest_armor


def xml_to_txt(in_dir, out_dir, mode):  # indir: xml文件路径 outdir: txt文件路径 mode:0 处理ROCO数据集 1 处理HEU/RPS数据集
    flag = 5
    parser = ET.XMLParser(encoding="utf-8")
    root = ET.parse(in_dir, parser=parser)
    root = root.getroot()

    f_w = open(out_dir, 'w')
    size_info = root.find("size")
    width = float(size_info.find("width").text)
    height = float(size_info.find("height").text)

    if mode == 0:  # 处理ROCO数据集
        cars = []
        armors = []
        # 找出所有的装甲板和车辆
        for obj in root.findall("object"):
            # error occurs when using func .find() specifically for string "armor_color"
            name = obj.find("name").text
            xmin = float(obj.find("bndbox").find("xmin").text)
            ymin = float(obj.find("bndbox").find("ymin").text)
            xmax = float(obj.find("bndbox").find("xmax").text)
            ymax = float(obj.find("bndbox").find("ymax").text)
            if name == 'armor':
                color = getattr(obj.find('armor_color'), 'text', None)
                x_center = (xmax + xmin) / 2
                y_center = (ymax + ymin) / 2
                center_point = [x_center, y_center]
                if color == 'red':
                    armors.append([0, center_point])
                elif color == 'blue':
                    armors.append([1, center_point])
                elif color == 'grey':
                    continue
                else:
                    print(f'color of armor is wrong:{in_dir}')
                    print(f'wrong color is: {color}')
            elif name == 'car':
                cars.append([xmin, ymin, xmax, ymax])
        # 将装甲板中心映射到车辆bndbox
        for car in cars:
            find_exception = 0
            last_flag = 6
            backup_armor = []
            for armor in armors:
                center_point = armor[1]
                x_coord = center_point[0]
                y_coord = center_point[1]
                if car[0] <= x_coord <= car[2] and car[1] <= y_coord <= car[3]:
                    backup_armor.append(armor)
                    flag = armor[0]
                    if last_flag != flag:
                        find_exception = find_exception + 1
                    last_flag = flag
            # 车辆颜色异常检查
            if find_exception == 0 or flag == 5:
                # print(f'car with no color,car:{car[0], car[1], car[2], car[3]};file: {indir}')
                continue
            elif find_exception > 1:
                # 预期装甲板位置
                x_armor = (car[0] + car[2]) / 2
                y_armor = car[1] + (car[3] - car[1])*0.75
                flag = return_best_flag(x_armor, y_armor, backup_armor)

            x_center = (car[0] + car[2]) / 2
            y_center = (car[1] + car[3]) / 2
            x = x_center / width
            y = y_center / height
            w = (car[2] - car[0]) / width
            h = (car[3] - car[1]) / height

            #  处理越界数据
            if x < 0:
                x = round(0, 6)
            elif x > 1:
                x = round(1, 6)
            if y < 0:
                y = round(0, 6)
            elif y > 1:
                y = round(1, 6)
            if w < 0:
                w = round(0, 6)
            elif w > 1:
                w = round(1, 6)
            if h < 0:
                h = round(0, 6)
            elif h > 1:
                h = round(1, 6)
            f_w.write("".join(
                [str(flag), ' ', str(round(x, 6)), ' ', str(round(y, 6)), ' ', str(round(w, 6)), ' ', str(round(h, 6)),
                 '\n']))

    elif mode == 1:
        for obj in root.findall("object"):
            name = obj.find("name").text
            xmin = float(obj.find("bndbox").find("xmin").text)
            ymin = float(obj.find("bndbox").find("ymin").text)
            xmax = float(obj.find("bndbox").find("xmax").text)
            ymax = float(obj.find("bndbox").find("ymax").text)
            x_center = (xmin + xmax) / 2
            y_center = (ymin + ymax) / 2
            x = x_center / width
            y = y_center / height
            w = (xmax - xmin) / width
            h = (ymax - ymin) / height
            if 'red' in name:
                # or name == 'hero_red'
                # or name == 'infantry_5_red'
                # # or name == 'ignore'
                # or name == 'sentry_red'):
                flag = 0
            elif 'blue' in name:
                # name == 'infantry_5_blue'):
                flag = 1
            if flag != 5:
                f_w.write("".join(
                    [str(flag), ' ', str(round(x, 6)), ' ', str(round(y, 6)), ' ', str(round(w, 6)), ' ',
                     str(round(h, 6)),
                     '\n']))
    f_w.close()


# # 小心xml文件路径关系,这个适用于ROCO数据集
# mkdir(outdir)  # 如果文件夹不存在则创建，如果存在则清空文件夹
# for dir in os.listdir(filedir):
#     if not os.path.isdir(os.path.join(filedir, dir)):
#         continue
#     for subdir in os.listdir(os.path.join(filedir, dir)):
#         if subdir == 'image_annotation':  # 仅处理image_annotation文件夹下的xml文件
#             print(os.path.join(filedir, dir, subdir))
#             for file in os.listdir(os.path.join(filedir, dir, subdir)):
#                 if file.endswith(".xml"):
#                     xml_to_txt(os.path.join(filedir, dir, subdir, file), os.path.join(outdir, file[:-4] + '.txt'))


# 这个适用于单纯一个文件夹，而不是在子文件夹下
mkdir(outdir)  # 如果文件夹不存在则创建，如果存在则清空文件夹

for file in os.listdir(filedir):
    if file.endswith(".xml"):
        xml_to_txt(os.path.join(filedir, file), os.path.join(outdir, file[:-4] + '.txt'), 1)
