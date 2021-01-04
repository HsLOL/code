# coding=utf-8
import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

"""step 3
该脚本将xml文件转换为对应的txt文件

参数说明：
1、ori_file_name_path:存储带有汽车的不带扩展名的图片名称
2、xml_path:VOC数据集中Annotations路径
3、将xml转化为txt文件夹的路径
"""

ori_file_name_path = r'ori_file_name.txt'
xml_path = r'D:\keshe\voc2007\VOCdevkit\VOC2007\Annotations'
txt_folder_path = r'D:\keshe\preprocess\txtfolder'


def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.' % (name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.' % (name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars


def get(root, name):
    return root.findall(name)


ori_file_name_list = []
with open(ori_file_name_path, 'r') as f:
    for line in f.readlines():
        line = line.strip()
        ori_file_name_list.append(line)

xml_file_list = [] # D:\keshe\voc2007\VOCdevkit\VOC2007\Annotations\000004.xml
for i in range(len(ori_file_name_list)):
    xml_file_path = xml_path + f'\\{ori_file_name_list[i]}' + '.xml'
    xml_file_list.append(xml_file_path)


# 137文件里面有person
for i in tqdm(range(len(xml_file_list)), desc='transforing', ncols=88):
    tree = ET.parse(xml_file_list[i])
    root = tree.getroot()
    size = get_and_check(root, 'size', 1)
    width = int(get_and_check(size, 'width', 1).text)
    height = int(get_and_check(size, 'height', 1).text)
    ####
    count_num = 0
    for obj in get(root, 'object'):
        obj_name = get_and_check(obj, 'name', 1).text
        if obj_name == 'car':
            count_num = count_num + 1
        else:
            continue
    ####

    tmp = 0
    for obj in get(root, 'object'):

        write_content = []

        # get object name
        obj_name = get_and_check(obj, 'name', 1).text

        if obj_name == 'car':
            flag = 1
            tmp = tmp + 1
            bndbox = get_and_check(obj, 'bndbox', 1)

            xmin = int(float(get_and_check(bndbox, 'xmin', 1).text))
            ymin = int(float(get_and_check(bndbox, 'ymin', 1).text))
            xmax = int(float(get_and_check(bndbox, 'xmax', 1).text))
            ymax = int(float(get_and_check(bndbox, 'ymax', 1).text))

            # get object's width , height, x_centre, y_centre
            obj_width = xmax - xmin
            obj_height = ymax - ymin
            x_centre = float(xmin + obj_width / 2)
            y_centre = float(ymin + obj_height / 2)

            # Normalize
            width_Nor = round(obj_width / width, 6)
            height_Nor = round(obj_height / height, 6)
            x_centre_Nor = round(x_centre / width, 6)
            y_centre_Nor = round(y_centre / height, 6)

            # list[0, width_Nor, height_Nor, x_centre_Nor, y_centre_Nor]
            write_content.append(0)
            write_content.append(x_centre_Nor)
            write_content.append(y_centre_Nor)
            write_content.append(width_Nor)
            write_content.append(height_Nor)
        if flag == 1:
            name_tmp = os.path.split(xml_file_list[i])[-1]
            real_name_tmp = os.path.splitext(name_tmp)[0]
            with open(txt_folder_path + f'\{real_name_tmp}' + '.txt', 'a') as f:
                length = 0
                for j in range(len(write_content)):
                    length = length + 1
                    f.write(str(write_content[j]))
                    if j != len(write_content) - 1:
                        f.write(' ')
                    else:
                        if length == 5 and tmp < count_num:
                            f.write('\n')
                            length = 0
                        elif tmp == count_num:
                            continue
