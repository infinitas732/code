import os
import shutil
import random

# 设置源文件夹路径
source_image_folder = r'C:\Users\admin\Desktop\wanglei\数据集\总数据集\images'  # 源图像文件夹
source_label_folder = r'C:\Users\admin\Desktop\wanglei\数据集\总数据集\labels'  # 源标签文件夹

# 设置目标文件夹路径
train_image_folder = r'D:\wl\mmcode\data\dataset_origin\water\images\training原始'  # 训练集图像文件夹
train_label_folder = r'D:\wl\mmcode\data\dataset_origin\water\annotations\training原始'  # 训练集标签文件夹
val_image_folder = r'D:\wl\mmcode\data\dataset_origin\water\images\validation原始'  # 验证集图像文件夹
val_label_folder = r'D:\wl\mmcode\data\dataset_origin\water\annotations\validation原始'  # 验证集标签文件夹

# 创建目标文件夹
os.makedirs(train_image_folder, exist_ok=True)
os.makedirs(train_label_folder, exist_ok=True)
os.makedirs(val_image_folder, exist_ok=True)
os.makedirs(val_label_folder, exist_ok=True)

# 获取所有图像和标签文件列表
image_files = sorted([f for f in os.listdir(source_image_folder) if f.endswith('.tif')])
label_files = sorted([f for f in os.listdir(source_label_folder) if f.endswith('.tif')])

# 确保图像和标签数量相等
assert len(image_files) == len(label_files), "图像文件和标签文件数量不匹配"

# 计算训练集和验证集的数量（7:3比例）
total_files = len(image_files)
train_size = int(total_files * 0.7)
val_size = total_files - train_size

# 随机打乱数据集
combined = list(zip(image_files, label_files))
random.shuffle(combined)
image_files, label_files = zip(*combined)

# 划分训练集和验证集
train_image_files = image_files[:train_size]
train_label_files = label_files[:train_size]
val_image_files = image_files[train_size:]
val_label_files = label_files[train_size:]

# 将文件复制到相应的训练集和验证集文件夹，并重新命名
train_image_count = 0
val_image_count = 0

# 处理训练集
for i, (img_file, lbl_file) in enumerate(zip(train_image_files, train_label_files)):
    train_image_count += 1
    new_img_name = f'image_{train_image_count}.tif'
    new_lbl_name = f'image_{train_image_count}.tif'
    shutil.copy(os.path.join(source_image_folder, img_file), os.path.join(train_image_folder, new_img_name))
    shutil.copy(os.path.join(source_label_folder, lbl_file), os.path.join(train_label_folder, new_lbl_name))

# 处理验证集
for i, (img_file, lbl_file) in enumerate(zip(val_image_files, val_label_files)):
    val_image_count += 1
    new_img_name = f'image_{val_image_count}.tif'
    new_lbl_name = f'image_{val_image_count}.tif'
    shutil.copy(os.path.join(source_image_folder, img_file), os.path.join(val_image_folder, new_img_name))
    shutil.copy(os.path.join(source_label_folder, lbl_file), os.path.join(val_label_folder, new_lbl_name))

# 打印划分结果
print(f"划分完成！训练集共生成了 {train_image_count} 张图像和标签，验证集共生成了 {val_image_count} 张图像和标签。")
