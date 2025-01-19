import os
import glob


def rename_images_in_folder(folder_path, prefix='image'):
    # 获取文件夹内所有的图片文件
    image_files = glob.glob(os.path.join(folder_path, '*'))

    for index, file_path in enumerate(image_files, start=0):
        # 获取文件扩展名
        ext = os.path.splitext(file_path)[1]
        # 生成新的文件名
        new_file_name = f"{prefix}_{index}{ext}"
        new_file_path = os.path.join(folder_path, new_file_name)

        # 重命名文件
        os.rename(file_path, new_file_path)
        print(f"重命名: {file_path} -> {new_file_path}")


# 示例用法
image_folder = r'C:\Users\admin\Desktop\wanglei\数据集\夏61831\st_8\imagess'  # 替换为你的图像文件夹路径
label_folder = r'C:\Users\admin\Desktop\wanglei\数据集\夏61831\st_8\labelss'  # 替换为你的标签文件夹路径

rename_images_in_folder(image_folder, prefix='image')
rename_images_in_folder(label_folder, prefix='image')
