# coding=utf8
# author=Han Wang


import os
import random

npy_data_folder = '/workspace/dataset/matrix_clean/tokens/qwen2/870_1000'
out_path = '/workspace/dataset/matrix_clean/data.txt'

res = []

def parse(npy_data_folder, file_name):
    ret = []
    with open(os.path.join(npy_data_folder, file_name), 'r') as f:
        for _ in f.readlines():
            _ = _.strip()
            if _:
                _ = _.split()
                ntokens = _[0]
                npy_data = os.path.join(npy_data_folder, file_name.split('.')[0])
                ret.append('{} {}'.format(ntokens, npy_data))
    return ret

# # 使用scandir()获取目录条目
# with os.scandir(npy_data_folder) as entries:
#     for entry in entries:
#         if entry.is_file() and entry.name.endswith('datalist'):
#             res += parse(npy_data_folder, entry.name)

def traverse_directory(dir_path):
    ret = []
    with os.scandir(dir_path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('datalist'):
                # 如果是文件，处理
                ret += parse(dir_path, entry.name)
            elif entry.is_dir():
                # 如果是目录，递归遍历该目录
                print(f"Entering directory: {entry.path}")
                ret += traverse_directory(entry.path)  # 递归调用遍历函数
    return ret

res = traverse_directory(npy_data_folder)
random.shuffle(res)

with open(out_path, 'w') as f:
    f.write('\n'.join(res))