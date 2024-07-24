# coding=utf8
# author=Han Wang


import os
import pdb
import shutil

npy_data_folders = ['/public/home/wangcheng/home/hanwang/data/tokens/ArabicText2022_without_cc100/qwen2/361_1000', '/public/home/wangcheng/home/hanwang/data/tokens/mC4/ar/361_1000']
flags = ['ArabicText2022_without_cc100/qwen2/361_1000', 'mC4/ar/361_1000']
MAX_NUMs = [27541383235, 56000000000-27541383235]
dst_dir = '/public/home/wangcheng/public/datasets/multiLang/ar'

import random

assert len(npy_data_folders) == len(flags)
assert len(npy_data_folders) == len(MAX_NUMs)

res = []

flag = 'ArabicText2022'

def parse(npy_data_folder, file_name):
    with open(os.path.join(npy_data_folder, file_name), 'r') as f:
        for _ in f.readlines():
            _ = _.strip()
            if _:
                _ = _.split()
                ntokens = _[0]
                ntokens = int(ntokens)
                npy_data_path = os.path.join(npy_data_folder, file_name.split('.')[0])
    return ntokens, npy_data_path
    
def get_ntoken(dir_path):
    ntoken = 0
    with os.scandir(dir_path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('datalist'):
                # 如果是文件，处理
                ntoken += parse(dir_path, entry.name)[0]
            elif entry.is_dir():
                # 如果是目录，递归遍历该目录
                print(f"Entering directory: {entry.path}")
                ntoken += get_ntoken(entry.path)  # 递归调用遍历函数
    print(f"Entering directory: {dir_path} num: {ntoken}")
    return ntoken

def traverse_directory(dir_path, max_num, cur_num):
    ret = []
    with os.scandir(dir_path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('datalist'):
                # 如果是文件，处理
                file_num = parse(dir_path, entry.name)[0]
                ret.append(os.path.join(dir_path, entry.name))
                cur_num+=file_num
                if cur_num>=max_num:
                    return ret
            elif entry.is_dir():
                # 如果是目录，递归遍历该目录
                print(f"Entering directory: {entry.path}")
                ret += traverse_directory(entry.path, max_num, cur_num)  # 递归调用遍历函数
    return ret
    
def copy_file(src, dst_dir, flag, relative_dir):
    if len(flag)>0:
        dst_dir = os.path.join(dst_dir, flag)
    # 目录结构也要保留    
    if len(relative_dir)>0:
        dst_dir = os.path.join(dst_dir, relative_dir)
    # 确保目标目录存在
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    
    # 目标文件路径，通常是在目标目录下使用源文件的名称
    dst = os.path.join(dst_dir, os.path.basename(src))
    
    # 复制文件
    try:
        shutil.copy(src, dst)
        print(f"文件已复制到 {dst}")
    except IOError as e:
        print(f"无法复制文件. {e}")
        
random.shuffle(npy_data_folders)

# 假设dir_path是你的目录路径
for i, npy_data_folder in enumerate(npy_data_folders):
    res = traverse_directory(npy_data_folder, MAX_NUMs[i], 0)
    add_strs = ['.idx', '.npy', '.npy.datalist', '.npy.metadata']
    for datalist_path in res:
        with open(datalist_path, 'r') as f:
            for _ in f.readlines():
                _ = _.strip()
                if _:
                    _ = _.split()
                    cur_path = _[1]
                    relative_dir = os.path.dirname(cur_path)[len(npy_data_folder)+1:]
                    for elem in add_strs:
                        copy_file(cur_path+elem, dst_dir, flags[i], relative_dir)