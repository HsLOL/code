# coding=utf-8
"""step 1
该代码用于找到DOTA数据集(train和val)中包含有车辆的txt文件，由于txt文件名与图片名称相对应

参数说明：
folder_path:存放生成的分别保存训练集和测试集中包含汽车名称的txt文件
ori_path_train:表示DOTA数据集训练集存放路径
ori_path_val:表示DOTA数据集验证集存放路径
dst_path_train:表示生成的保存训练集中含有汽车的txt文件名称（image_name_train.txt)
dst_path_val:表示生成的保存验证集中含有汽车的txt文件名称（image_name_val.txt)
"""

import argparse
from pathlib import Path
from tqdm import tqdm
import os
import numpy as np


def find_index_in_given_path(path) -> list:
    # 用于找到符合条件的DOTA中训练集/验证集图片的索引
    img_name_lists = []

    p = Path(path)
    txt_lists = list(p.glob('*.txt'))
    print(f'the number of the image(s) is {len(txt_lists)}')
    for index, file_name in tqdm(enumerate(txt_lists), desc='find_index_in_given_path', ncols=88):
        # file_name e.x. --> D:\Bishe\遥感数据集\DOTA\train\labelTxt-v1.5\P0000.txt
        file_content = []
        with open(file_name, 'r') as f:
            s = f.readlines()
            body = s[2:]
            for line in body:
                line = line.strip().split(' ')
                file_content.append(line)
            for i in range(len(file_content)):
                if file_content[i][8] == 'large-vehicle' or file_content[i][8] == 'small-vehicle':
                    img_name_lists.append(Path(file_name).name)
                    break
    return img_name_lists


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def output_file(path, lists):
    arr = np.array(lists)
    arr = arr[np.newaxis, :]
    lists = list(arr)
    with open(path, 'w') as f:
        for i in range(len(lists)):
            f.write('\n'.join(lists[i]))


if __name__ == '__main__':
    folder_path = r'image_train_val'  # 存放生成的image_name_train.txt和image_name_val.txt文件的文件夹
    current_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(current_path)
    path = os.path.join(dir_path, folder_path)
    make_dir(path)

    parser = argparse.ArgumentParser()
    parser.add_argument('-ori_path_train', '--ori_path_train', type=str,
                        default=r'D:\Bishe\遥感数据集\DOTA\train\labelTxt-v1.5',
                        help='the path of the DOTA\'s training set path')
    parser.add_argument('-ori_path_val', '--ori_path_val',
                        type=str,
                        default=r'D:\Bishe\遥感数据集\DOTA\val\labelTxt-v1.0\Val_Task2_gt\valset_reclabelTxt',
                        help='the path of the DOTA\'s val set path')
    parser.add_argument('-dst_path_train', '--dst_path_train', type=str,
                        default=r'image_name_train.txt',
                        help='the name of the output txt file which contains the object in train set')
    parser.add_argument('-dst_path_val', '--dst_path_val', type=str,
                        default=r'image_name_val.txt',
                        help='the name of the output txt file which contains the object in val set')
    args = parser.parse_args()

    ori_path_train = args.ori_path_train
    ori_path_val = args.ori_path_val
    dst_path_train = args.dst_path_train
    dst_path_val = args.dst_path_val

    # 在训练集中寻找合适的txt文件（txt文件名与图片名称对应）
    train_img_name = find_index_in_given_path(ori_path_train)
    print(f'符合要求的txt文件名称(train)：{train_img_name}\n符合要求的文件个数为{len(train_img_name)}')
    output_file(os.path.join(path, dst_path_train), train_img_name)

    # 在验证集汇总寻找合适的txt文件（txt文件名与图片名称对应）
    val_img_name = find_index_in_given_path(ori_path_val)
    print(f'符合要求的txt文件名称(val)：{val_img_name}\n符合要求的文件个数为{len(val_img_name)}')
    output_file(os.path.join(path, dst_path_val), val_img_name)
