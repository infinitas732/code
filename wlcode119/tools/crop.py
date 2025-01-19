from PIL import Image
import os


def crop_image(image_path, output_dir, crop_size=256, overlap=30):
    # 增加最大像素限制
    Image.MAX_IMAGE_PIXELS = None

    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(image_path)
    img_width, img_height = img.size

    num = 0
    for top in range(0, img_height, crop_size - overlap):
        for left in range(0, img_width, crop_size - overlap):
            right = min(left + crop_size, img_width)
            bottom = min(top + crop_size, img_height)

            # 调整裁剪框以确保始终为 crop_size x crop_size
            if right - left != crop_size:
                left = img_width - crop_size
                right = img_width
            if bottom - top != crop_size:
                top = img_height - crop_size
                bottom = img_height

            box = (left, top, right, bottom)
            crop = img.crop(box)
            crop.save(os.path.join(output_dir, f"{num}.png"))
            num += 1


# 示例用法
crop_image('E:/下载/VV_VH_DEM_5Band_Image.tif', 'D:/rsimage_d/青藏高原/code/预测/输出')
