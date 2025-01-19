import os
import torch
import torch.nn.functional as F
from mmseg.apis import inference_model, init_model
import rasterio
import numpy as np

# 定义路径
config_file = r'D:\wl\mmcode2\configs\swin\swin-tiny-patch4-window7_upernet_1xb8-20k_levir-256x256.py'
checkpoint_file = r'D:\wl\mmcode2\work_dirs\swin-tiny-patch4-window7_upernet_1xb8-20k_levir-256x256\iter_64000.pth'
input_folder = r'C:\Users\admin\Desktop\wanglei\预测\input_test11'
output_folder = r'C:\Users\admin\Desktop\wanglei\预测\output_test11'

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 初始化模型
model = init_model(config_file, checkpoint_file, device='cuda:0')

# 设置阈值
threshold = 0.62

# 定义填充函数
def pad_to_multiple(img, divisor=16):
    """
    填充输入图像，使其宽高为 divisor 的倍数。
    :param img: 输入图像，形状为 (H, W, C)
    :param divisor: 要求的倍数
    :return: 填充后的图像，以及填充前的尺寸信息
    """
    h, w, c = img.shape
    new_h = ((h + divisor - 1) // divisor) * divisor
    new_w = ((w + divisor - 1) // divisor) * divisor
    padded_img = np.zeros((new_h, new_w, c), dtype=img.dtype)
    padded_img[:h, :w, :] = img
    return padded_img, (h, w)

# 获取输入图像列表
input_images = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if
                file.endswith(('.tif', '.tiff'))]

# 推理并保存结果
for img_path in input_images:
    img_name = os.path.basename(img_path)

    # 使用 rasterio 读取多通道图像
    with rasterio.open(img_path) as src:
        img = src.read()  # 读取所有通道，返回形状为 (channels, height, width) 的数组
        profile = src.profile  # 获取输入文件的元数据信息

    # 转换为 (height, width, channels) 格式
    img = np.transpose(img, (1, 2, 0))

    # 填充图像
    padded_img, original_size = pad_to_multiple(img, divisor=16)

    print(f"Processing image: {img_name}, original shape: {img.shape}, padded shape: {padded_img.shape}")

    # 推理
    with torch.no_grad():
        result = inference_model(model, padded_img)

        # 提取预测的语义分割结果
        pred_mask = result.pred_sem_seg.data[0].cpu().numpy()

        # 恢复到原始图像的大小
        pred_mask = pred_mask[:original_size[0], :original_size[1]]

        # 将预测结果通过 sigmoid 函数
        pred_mask_tensor = torch.tensor(pred_mask)
        pred_mask_sigmoid = F.sigmoid(pred_mask_tensor)

        # 应用阈值
        binary_result = (pred_mask_sigmoid > threshold).float().numpy()

        # 转换为 0-255 的二值化结果
        binary_result_uint8 = (binary_result * 255).astype(np.uint8)

        # 更新 profile 信息，设定保存成单通道
        profile.update(
            dtype=rasterio.uint8,  # 保存为 8-bit 无符号整数格式
            count=1,               # 单通道
            compress='lzw'         # 压缩方式，可选
        )

        # 保存二值化后的结果图像为 .tif 文件
        output_path = os.path.join(output_folder, img_name.replace('.tif', '.tif'))
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(binary_result_uint8, 1)  # 写入第一通道

        print(f"Saving binary result for {img_name} to {output_path}")

    print(f"Finished processing {img_name}")
