import os
import numpy as np
import rasterio
from tqdm import tqdm
import joblib

# 读取TIFF文件
def read_tif(file_path):
    """
    读取TIFF文件，返回数据和profile信息。
    """
    with rasterio.open(file_path) as src:
        image = src.read()
        profile = src.profile
    return image, profile

# 重塑数据为2D
def reshape_data(image):
    """
    将影像数据展平为2D数组。
    """
    n_bands, n_rows, n_cols = image.shape
    image_reshaped = image.reshape((n_bands, n_rows * n_cols)).T
    return image_reshaped, (n_rows, n_cols)

# 输入单张影像路径
input_image_path = r'C:\Users\admin\Desktop\wanglei\预测\test_region\1\新建文件夹\1.tif'  # 输入影像文件路径
output_dir = r'C:\Users\admin\Desktop\wanglei\预测\test_region\1\新建文件夹\新建文件夹'  # 保存预测结果的文件夹
os.makedirs(output_dir, exist_ok=True)

# 加载训练好的模型和标准化器
knn_model = joblib.load(r'D:\wl\unet1\knn_model.joblib')  # 训练好的KNN模型
scaler = joblib.load(r'D:\wl\unet1\knn_scaler.joblib')  # 标准化器

# 读取影像
image, profile = read_tif(input_image_path)
image_reshaped, (n_rows, n_cols) = reshape_data(image)

# 标准化数据
image_scaled = scaler.transform(image_reshaped)

# 进行预测
preds = knn_model.predict(image_scaled)

# 重塑为影像大小
preds_image = preds.reshape((n_rows, n_cols))

# 保存预测结果为TIFF
output_path = os.path.join(output_dir, os.path.basename(input_image_path))
with rasterio.open(output_path, 'w', **profile) as dst:
    dst.write(preds_image.astype(rasterio.uint8), 1)

print(f"预测完成！结果已保存至：{output_path}")
