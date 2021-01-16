# coding=utf-8

"""
该代码用于将手工筛选的txt文件名称与DOTA中的名称进行匹配
同时将图片和标记的txt文件存储到固定的文件夹中
"""

import argparse
from pathlib import Path
from collections import defaultdict
import os
import shutil
from tqdm import tqdm


class Rename:
    def __init__(self, dir_path, train_folder, val_folder, train_images_path, train_txt_path,
                 val_images_path, val_txt_path):
        self.get_name_path = dir_path
        self.train_folder = train_folder
        self.val_folder = val_folder
        self.train_images_path = train_images_path
        self.train_txt_path = train_txt_path
        self.val_images_path = val_images_path
        self.val_txt_path = val_txt_path

    def get_name(self) ->dict:
        self.default_dict = defaultdict(list)
        p = Path(self.get_name_path)
        txt_name = list(p.glob('*.txt'))
        with open(txt_name[0], 'r') as f:
            s = f.readlines()
            for line in s:
                line = line.strip()
                self.default_dict[txt_name[0].name.split('.')[0]].append(line)
        with open(txt_name[1], 'r') as f:
            s = f.readlines()
            for line in s:
                line = line.strip()
                self.default_dict[txt_name[1].name.split('.')[0]].append(line)
        print(f'get_name()输出:{self.default_dict}')
        return self.default_dict

    @staticmethod
    def rename(dicts) -> dict:
        keys = dicts.keys()
        keys = list(keys)
        train_list = dicts[keys[0]]
        # val_list = dicts[keys[1]]
        length = 4  # e.x. P0003.jpg
        for i in range(len(train_list)):
            name = train_list[i]
            zeros = length - len(name)
            train_list[i] = 'P' + str(0) * zeros + name

        # for i in range(len(val_list)):
        #     name = val_list[i]
        #     zeros = length - len(name)
        #     val_list[i] = 'P' + str(zeros * 0) + name + '.jpg'

        dicts['train'] = train_list
        # dicts['val'] = val_list
        return dicts

    def copy_images(self):
        # copy train images
        train_images = self.default_dict['train']
        for i in tqdm(range(len(train_images)), desc='copy train images', ncols=88):
            shutil.copy(os.path.join(self.train_images_path, (train_images[i] + '.png')),
                        self.train_folder + '\\images\\' + train_images[i] + '.jpg')

        # copy val images
        # val_images = self.default_dict['val']
        # for i in tqdm(range(len(val_images)), desc='copy val images', ncols=88):
        #     shutil.copy(os.path.join(self.val_images_path, (val_images[i] + '.png')),
        #                 self.val_folder + '\\images\\' + val_images[i] + '.jpg')

    def copy_txt(self):
        # copy train txt
        train_txt = self.default_dict['train']
        for i in tqdm(range(len(train_txt)), desc='copy train txt', ncols=88):
            shutil.copy(os.path.join(self.train_txt_path, (train_txt[i] + '.txt')),
                        self.train_folder + '\\labels\\' + train_txt[i] + '.txt')

        # copy val txt
        # val_txt = self.default_dict['val']
        # for i in tqdm(range(len(val_txt)), desc='copy val txt', ncols=88):
        #     shutil.copy(os.path.join(self.val_txt_path, (val_txt[i] + '.txt')),
        #                 self.val_folder + '\\labels\\' + val_txt[i] + '.txt')

    @staticmethod
    def path_connect(dir_path, path):
        return os.path.join(dir_path, path)

    def make_folder(self):
        path_list = []
        path_list.append(self.path_connect(self.train_folder, 'images'))
        path_list.append(self.path_connect(self.train_folder, 'labels'))
        path_list.append(self.path_connect(self.val_folder, 'images'))
        path_list.append(self.path_connect(self.val_folder, 'labels'))
        for i in range(len(path_list)):
            if not os.path.exists(path_list[i]):
                os.makedirs(path_list[i], exist_ok=True)
            else:
                print(f'文件夹{path_list[i]}已存在')


if __name__ == '__main__':
    images_path = r'images'
    txts_path = r'labels'
    parser = argparse.ArgumentParser()
    parser.add_argument('-dirpath', '--dirpath',
                        type=str,
                        default=r'D:\Bishe\毕设实验代码\code\手动筛选得到的train和val中的包含汽车的图片名称并进行rename\train_val_image_name_Byhands',
                        help='the name of the path which contains the train&val.txt')
    parser.add_argument('-output_train_folder', '--output_train_folder',
                        type=str,
                        default=r'D:\Bishe\手动挑出来的车辆数据集\train',
                        help='the path of copy train set folder')
    parser.add_argument('-output_val_folder', '--output_val_folder',
                        type=str,
                        default=r'D:\Bishe\手动挑出来的车辆数据集\val',
                        help='the path of the copy val set images')
    parser.add_argument('-DOTA_train_images_path', '--DOTA_train_images_path',
                        type=str,
                        default=r'D:\Bishe\遥感数据集\DOTA\train\images\images',
                        help='the path of the DOTA train images files')
    parser.add_argument('-DOTA_train_txt_path', '--DOTA_train_txt_path',
                        type=str,
                        default=r'D:\Bishe\遥感数据集\DOTA\train\labelTxt-v1.5',
                        help='the path of the DOTA train txt files')
    parser.add_argument('-DOTA_val_images_path', '--DOTA_val_images_path',
                        type=str,
                        default=r'D:\Bishe\遥感数据集\DOTA\val\images\images',
                        help='the path of the DOTA val images files')
    parser.add_argument('-DOTA_val_txt_path', '--DOTA_val_txt_path',
                        type=str,
                        default=r'D:\Bishe\遥感数据集\DOTA\val\labelTxt-v1.0\Val_Task2_gt\valset_reclabelTxt',
                        help='the path of the DOTA val txt files')
    args = parser.parse_args()

    c = Rename(args.dirpath, args.output_train_folder, args.output_val_folder,
               args.DOTA_train_images_path, args.DOTA_train_txt_path,
               args.DOTA_val_images_path, args.DOTA_val_txt_path)
    get_name_dicts = c.get_name()
    rename_dicts = c.rename(get_name_dicts)
    print(f'重命名文件名称：{rename_dicts}')
    c.make_folder()
    c.copy_images()
    c.copy_txt()
