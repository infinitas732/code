
import os
import numpy as np
import rasterio
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import joblib
from tqdm import tqdm  # 引入进度条

# 读取影像和标签
def read_tif(file_path):
    """
    读取TIFF文件，返回数据和profile信息。
    """
    with rasterio.open(file_path) as src:
        image = src.read()
    return image

# 获取文件路径列表
def get_file_list(image_dir, label_dir):
    """
    获取影像和标签的文件路径列表。
    """
    image_files = sorted([os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.tif')])
    label_files = sorted([os.path.join(label_dir, f) for f in os.listdir(label_dir) if f.endswith('.tif')])
    return image_files, label_files

# 重塑数据为2D
def reshape_data(image, labels):
    """
    将影像数据和标签展平为2D数组。
    """
    n_bands, n_rows, n_cols = image.shape
    image_reshaped = image.reshape((n_bands, n_rows * n_cols)).T
    labels_reshaped = labels.flatten()
    return image_reshaped, labels_reshaped

# 数据路径
train_image_dir = r'D:\wl\mmcode\data\dataset_origin\water\images\training'  # 训练集影像文件夹
train_label_dir = r'D:\wl\mmcode\data\dataset_origin\water\annotations\training' # 训练集标签文件夹

# 获取训练数据文件列表
train_images, train_labels = get_file_list(train_image_dir, train_label_dir)

# 初始化存储训练数据
all_images = []
all_labels = []

# 读取训练数据并重塑（添加进度条）
print("正在加载训练数据...")
for image_path, label_path in tqdm(zip(train_images, train_labels), total=len(train_images), desc="加载数据"):
    image = read_tif(image_path)
    labels = read_tif(label_path)
    image_reshaped, labels_reshaped = reshape_data(image, labels)
    all_images.append(image_reshaped)
    all_labels.append(labels_reshaped)

# 合并所有数据
all_images = np.vstack(all_images)
all_labels = np.hstack(all_labels)

# 标准化数据
print("正在标准化数据...")
scaler = StandardScaler()
all_images_scaled = scaler.fit_transform(all_images)

# 训练KNN模型
print("正在训练模型...")
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(all_images_scaled, all_labels)

# 保存模型和标准化器
joblib.dump(knn_model, 'knn_model.joblib')
joblib.dump(scaler, 'knn_scaler.joblib')

print("训练完成，模型已保存！")
