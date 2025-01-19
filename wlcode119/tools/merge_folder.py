import os
import shutil

# 设置源文件夹路径和目标文件夹路径
source_folders = [r'D:\rsimage_d\青藏高原\code\数据集\秋911130\at1_336',
                  r'D:\rsimage_d\青藏高原\code\数据集\秋911130\at2_70',
                  r'D:\rsimage_d\青藏高原\code\数据集\秋911130\at3_500\at3_1_323',
                  r'D:\rsimage_d\青藏高原\code\数据集\秋911130\at3_500\at3_2_114',
                  r'D:\rsimage_d\青藏高原\code\数据集\秋911130\at3_500\at3_3_32',
                  r'D:\rsimage_d\青藏高原\code\数据集\秋911130\at3_500\at3_4_27',
                  r'D:\rsimage_d\青藏高原\code\数据集\秋911130\at3_500\at3_5_4',
                  r'D:\rsimage_d\青藏高原\code\数据集\夏61831\t1_693\st1_1_60',
                  r'D:\rsimage_d\青藏高原\code\数据集\夏61831\t1_693\st1_2_105',
                  r'D:\rsimage_d\青藏高原\code\数据集\夏61831\t1_693\st1_3-390',
                  r'D:\rsimage_d\青藏高原\code\数据集\夏61831\t1_693\st1_4-138',
                  r'D:\rsimage_d\青藏高原\code\数据集\夏61831\t3_560',
                  r'D:\rsimage_d\青藏高原\code\数据集\夏61831\t4_414']  # 源文件夹列表
target_image_folder = r'D:\rsimage_d\青藏高原\code\数据集\总数据集\images'  # 目标图像文件夹
target_label_folder = r'D:\rsimage_d\青藏高原\code\数据集\总数据集\labels'  # 目标标签文件夹

# 创建目标文件夹
os.makedirs(target_image_folder, exist_ok=True)
os.makedirs(target_label_folder, exist_ok=True)

image_count = 0
label_count = 0

# 遍历每个源文件夹
for folder in source_folders:
    image_files = sorted(os.listdir(os.path.join(folder, 'images')))  # 确保按顺序处理
    label_files = sorted(os.listdir(os.path.join(folder, 'labels')))

    # 处理每个图像文件
    for img_file in image_files:
        if img_file.endswith('.tif') and img_file.startswith('image_'):  # 仅处理image_开头的.tif文件
            # 新命名格式
            image_count += 1
            new_img_name = f'image_{image_count}.tif'
            shutil.copy(os.path.join(folder, 'images', img_file), os.path.join(target_image_folder, new_img_name))

            # 查找与图片编号匹配的标签文件
            corresponding_label_name = img_file.replace('image_', 'image_')  # 替换文件名前缀
            if corresponding_label_name in label_files:
                label_count += 1
                new_label_name = f'image_{image_count}.tif'
                shutil.copy(os.path.join(folder, 'labels', corresponding_label_name), os.path.join(target_label_folder, new_label_name))
            else:
                # 调试输出：如果标签文件未找到
                print(f"未找到标签文件: {corresponding_label_name}")

# 打印生成的图片和标签数量
print(f"合并完成！共生成了 {image_count} 张图片和 {label_count} 张标签。")
