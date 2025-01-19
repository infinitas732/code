import os
import rasterio
from rasterio.windows import Window

def crop_image(image_path, output_dir, crop_size=256, overlap=30):
    os.makedirs(output_dir, exist_ok=True)

    with rasterio.open(image_path) as src:
        img_width = src.width
        img_height = src.height

        num = 0
        for top in range(0, img_height, crop_size - overlap):
            for left in range(0, img_width, crop_size - overlap):
                right = min(left + crop_size, img_width)
                bottom = min(top + crop_size, img_height)

                # 定义裁剪窗口
                window = Window(left, top, right - left, bottom - top)

                # 读取窗口内的影像数据
                crop = src.read(window=window)

                # 保存裁剪后的图像
                out_meta = src.meta.copy()
                out_meta.update({
                    "driver": "GTiff",
                    "height": crop.shape[1],  # 使用裁剪后的高度
                    "width": crop.shape[2],    # 使用裁剪后的宽度
                    "transform": rasterio.windows.transform(window, src.transform)
                })
                with rasterio.open(os.path.join(output_dir, f"{num}.tif"), 'w', **out_meta) as dest:
                    dest.write(crop)

                num += 1

# 示例用法
crop_image(r'C:\Users\admin\Desktop\wanglei\预测\test_region\test27.tif', r'C:\Users\admin\Desktop\wanglei\预测\input_test27')
