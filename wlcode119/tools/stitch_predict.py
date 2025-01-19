import os
import rasterio
import numpy as np


def stitch_image(input_dir, output_image_path, original_image_path, crop_size=256, overlap=30):
    with rasterio.open(original_image_path) as src:
        img_width = src.width
        img_height = src.height

        # 创建一个空数组，用于存储拼接结果
        stitched_image = np.zeros((img_height, img_width), dtype='float32')

        num = 0
        for top in range(0, img_height, crop_size - overlap):
            for left in range(0, img_width, crop_size - overlap):
                right = min(left + crop_size, img_width)
                bottom = min(top + crop_size, img_height)

                crop_path = os.path.join(input_dir, f"{num}.tif")
                if os.path.exists(crop_path):
                    with rasterio.open(crop_path) as crop:
                        crop_data = crop.read(1)  # 读取单通道预测结果
                        crop_data = crop_data.astype('float32')

                        # 确保形状匹配
                        stitched_image[top:bottom, left:right] = crop_data[:(bottom - top), :(right - left)]

                num += 1

        # 更新输出图像的元数据
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "count": 1,
            "height": img_height,
            "width": img_width,
            "dtype": 'float32',
            "transform": src.transform
        })

        # 保存拼接后的预测结果图像
        with rasterio.open(output_image_path, 'w', **out_meta) as dest:
            dest.write(stitched_image, 1)


# 示例用法
stitch_image(
    r'C:\Users\admin\Desktop\wanglei\预测\output_test11',
    r'C:\Users\admin\Desktop\wanglei\预测\predict_test11.tif',
r'C:\Users\admin\Desktop\wanglei\预测\test_region\test11.tif',
    crop_size=256,
    overlap=30
)
