import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import rasterio
import numpy as np


# 自定义数据集类
class CustomTIFDataset(Dataset):
    def __init__(self, image_dir, mask_dir, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        self.image_files = [f for f in os.listdir(image_dir) if f.startswith('image_') and f.endswith('.tif')]

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        # 读取影像文件路径
        image_file = self.image_files[idx]
        image_path = os.path.join(self.image_dir, image_file)

        # 构造对应的标签文件名并获取路径
        label_file = image_file.replace('image_', 'label_')
        mask_path = os.path.join(self.mask_dir, label_file)

        # 检查标签文件是否存在
        if not os.path.exists(mask_path):
            raise FileNotFoundError(f"Mask file {mask_path} does not exist.")

        # 读取影像
        with rasterio.open(image_path) as src:
            image = src.read().astype(np.float32)  # 读取五通道影像，形状为 (channels, height, width)

        # 读取标签
        with rasterio.open(mask_path) as src:
            mask = src.read(1).astype(np.float32)  # 读取单通道标签

        # 标签二值化为0和1
        mask[mask == 255] = 1

        # 影像现在是 NumPy 数组，形状为 (channels, height, width)，不用转换为 tensor 直接传递给 transform
        if self.transform:
            # 将影像的通道维度移到最后，变成 (height, width, channels)，符合 PIL Image 的格式要求
            image = np.moveaxis(image, 0, -1)
            image = self.transform(image)  # 应用 transform，之后会转换为 Tensor 并且通道会重新回到第一维

            mask = torch.from_numpy(mask).unsqueeze(0)  # 增加一个通道维度

        return image, mask


# 数据增强的转换
data_transforms = transforms.Compose([
    transforms.ToTensor(),  # 将 NumPy 转换为 Tensor
])

# 加载数据集
train_image_dir = "C:/Users/admin/Desktop/code/数据集/测试数据集/总合并/t_images"
train_mask_dir = "C:/Users/admin/Desktop/code/数据集/测试数据集/总合并/t_labels"
val_image_dir = "C:/Users/admin/Desktop/code/数据集/测试数据集/总合并/v_images"
val_mask_dir = "C:/Users/admin/Desktop/code/数据集/测试数据集/总合并/v_labels"

train_dataset = CustomTIFDataset(train_image_dir, train_mask_dir, transform=data_transforms)
val_dataset = CustomTIFDataset(val_image_dir, val_mask_dir, transform=data_transforms)

# 数据加载器
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# 测试代码
for images, masks in train_loader:
    print(f"Images batch shape: {images.shape}")  # 输出形状应为 (batch_size, channels, height, width)
    print(f"Masks batch shape: {masks.shape}")  # 输出形状应为 (batch_size, 1, height, width)
    break
# 打印训练和验证集样本数量
print(f"Number of training samples: {len(train_dataset)}")
print(f"Number of validation samples: {len(val_dataset)}")