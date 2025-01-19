from PIL import Image
import os


def stitch_image(input_dir, output_image_path, original_size=(13867, 13514), crop_size=256, overlap=30):
    img_width, img_height = original_size
    stitched_image = Image.new('RGB', (img_width, img_height))

    num = 0
    for top in range(0, img_height, crop_size - overlap):
        for left in range(0, img_width, crop_size - overlap):
            right = min(left + crop_size, img_width)
            bottom = min(top + crop_size, img_height)

            # Adjust position to ensure correct placement
            if right - left != crop_size:
                left = img_width - crop_size
            if bottom - top != crop_size:
                top = img_height - crop_size

            try:
                crop = Image.open(os.path.join(input_dir, f"{num}.png"))
                stitched_image.paste(crop, (left, top))
                num += 1
            except FileNotFoundError:
                continue

    stitched_image.save(output_image_path)


# Example usage
stitch_image('D:/rsimage_d/predict_image/鄱阳湖/1', 'D:/rsimage_d/predict_image/鄱阳湖/predict.png')
