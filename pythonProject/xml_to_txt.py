import os
import sys
import xml.etree.ElementTree as ET

filedir = r'F:\Target_detection\datasets\DJI ROCO'
outdir = r'F:\Target_detection\datasets\DJI ROCO\label'


def del_all_files(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            os.removedir(c_path)
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


def xml_to_txt(indir, outdir):  # indir: xml文件路径 outdir: txt文件路径
    parser = ET.XMLParser(encoding="utf-8")
    root = ET.parse(indir, parser=parser)
    root = root.getroot()

    f_w = open(outdir, 'w')
    size_info = root.find("size")
    width = float(size_info.find("width").text)
    height = float(size_info.find("height").text)
    for obj in root.findall("object"):
        # error occurs when using func .find() specifically for string "armor_color"
        color = getattr(obj.find('armor_color'), 'text', None)
        name = obj.find("name").text
        xmin = float(obj.find("bndbox").find("xmin").text)
        ymin = float(obj.find("bndbox").find("ymin").text)
        xmax = float(obj.find("bndbox").find("xmax").text)
        ymax = float(obj.find("bndbox").find("ymax").text)
        x_center = (xmax + xmin) / 2
        y_center = (ymax + ymin) / 2
        x = x_center / width
        y = y_center / height
        w = (xmax - xmin) / width
        h = (ymax - ymin) / height
        flag = 5
        # if name == 'car':
        #     flag = 0
        # elif name == 'armor':
        #     if color == 'blue':
        #         flag = 1
        #     elif color == 'red':
        #         flag = 2
        # elif name == 'base':
        #     flag = 3
        # elif name == 'watcher':
        #     flag = 4
        if (name == 'hero_red'
                or name == 'infantry_5_red'
                or name == 'infantry_5_blue'
                or name == 'ignore'
                or name == 'sentry_red'
                or name == 'car'
        ):  # car标签为0
            flag = 0
        elif name == 'base':  # base标签为1
            flag = 1
        if flag != 5:
            f_w.write("".join(
                [str(flag), ' ', str(round(x, 6)), ' ', str(round(y, 6)), ' ', str(round(w, 6)), ' ', str(round(h, 6)),
                 '\n']))
    f_w.close()


# 小心xml文件路径关系,这个适用于ROCO数据集
mkdir(outdir)  # 如果文件夹不存在则创建，如果存在则清空文件夹
for dir in os.listdir(filedir):
    if not os.path.isdir(os.path.join(filedir, dir)):
        continue
    for subdir in os.listdir(os.path.join(filedir, dir)):
        if subdir == 'image_annotation':  # 仅处理image_annotation文件夹下的xml文件
            print(os.path.join(filedir, dir, subdir))
            for file in os.listdir(os.path.join(filedir, dir, subdir)):
                if file.endswith(".xml"):
                    xml_to_txt(os.path.join(filedir, dir, subdir, file), os.path.join(outdir, file[:-4] + '.txt'))



# # 这个适用于单纯一个文件夹，而不是在子文件夹下
# mkdir(outdir)  # 如果文件夹不存在则创建，如果存在则清空文件夹

# for file in os.listdir(filedir):
#     if file.endswith(".xml"):
#         xml_to_txt(os.path.join(filedir,file), os.path.join(outdir, file[:-4] + '.txt'))
