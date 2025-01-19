import os
import shutil


def merge_and_rename_folders(image_folder1, image_folder2, label_folder1, label_folder2, output_image_folder,
                             output_label_folder):
    # 创建输出文件夹
    os.makedirs(output_image_folder, exist_ok=True)
    os.makedirs(output_label_folder, exist_ok=True)

    # 获取文件列表
    image_files1 = sorted(os.listdir(image_folder1))
    image_files2 = sorted(os.listdir(image_folder2))
    label_files1 = sorted(os.listdir(label_folder1))
    label_files2 = sorted(os.listdir(label_folder2))

    # 合并第一个文件夹的内容
    for idx, (img_file, label_file) in enumerate(zip(image_files1, label_files1), start=1):
        img_src = os.path.join(image_folder1, img_file)
        label_src = os.path.join(label_folder1, label_file)

        img_dst = os.path.join(output_image_folder, f"image_{idx:04d}.tif")
        label_dst = os.path.join(output_label_folder, f"label_{idx:04d}.tif")

        shutil.copy(img_src, img_dst)
        shutil.copy(label_src, label_dst)

    # 合并第二个文件夹的内容
    start_idx = len(image_files1) + 1  # 接着之前的编号
    for idx, (img_file, label_file) in enumerate(zip(image_files2, label_files2), start=start_idx):
        img_src = os.path.join(image_folder2, img_file)
        label_src = os.path.join(label_folder2, label_file)

        img_dst = os.path.join(output_image_folder, f"image_{idx:04d}.tif")
        label_dst = os.path.join(output_label_folder, f"label_{idx:04d}.tif")

        shutil.copy(img_src, img_dst)
        shutil.copy(label_src, label_dst)

    print(f"合并完成！影像保存到 {output_image_folder}，标签保存到 {output_label_folder}")


# 输入影像和标签文件夹路径
image_folder1 = "D:/rsimage_d/青藏高原/code/output_images"
image_folder2 = "D:/rsimage_d/青藏高原/code/output_images1"
label_folder1 = "D:/rsimage_d/青藏高原/code/output_labels"
label_folder2 = "D:/rsimage_d/青藏高原/code/output_labels1"

# 输出合并后的影像和标签文件夹
output_image_folder = "D:/rsimage_d/青藏高原/code/join_image"
output_label_folder = "D:/rsimage_d/青藏高原/code/join_label"

# 调用合并函数
merge_and_rename_folders(image_folder1, image_folder2, label_folder1, label_folder2, output_image_folder,
                         output_label_folder)
