import rasterio
import numpy as np
import glob

# 假设你的影像存储在一个文件夹中
image_paths = glob.glob(r'D:\wl\mmcode\data\dataset_origin\water\images\training/*.tif')

# 用于存储每个通道的数据
channels_data = []

for img_path in image_paths:
    with rasterio.open(img_path) as src:
        # 读取所有通道数据
        img_array = src.read()  # shape: (channels, height, width)
        channels_data.append(img_array)

# 转换为 NumPy 数组并计算均值和标准差
channels_data = np.array(channels_data)  # shape: (num_images, channels, height, width)

# 计算每个通道的均值和标准差
mean = np.mean(channels_data, axis=(0, 2, 3))  # 对每个通道计算均值
std = np.std(channels_data, axis=(0, 2, 3))    # 对每个通道计算标准差

print("Mean:", mean)
print("Std:", std)
