import numpy as np
import rasterio
import os


def load_tif(filepath):
    with rasterio.open(filepath) as src:
        return src.read(1), src.width, src.height


def check_dimensions_and_values(pred_files, gt_file):
    # Load ground truth image
    gt, gt_width, gt_height = load_tif(gt_file)
    if not np.all(np.isin(gt, [0, 1])):
        raise ValueError("Ground truth image contains values other than 0 and 1.")

    results = {}
    for file in pred_files:
        pred, pred_width, pred_height = load_tif(file)
        if pred_width != gt_width or pred_height != gt_height:
            raise ValueError(f"Prediction image {file} dimensions do not match ground truth.")

        # Ensure the prediction values are binary (0 or 1)
        if not np.all(np.isin(pred, [0, 1])):
            print(f"Warning: Prediction image {file} contains values other than 0 and 1. Thresholding values...")
            pred = np.where(pred > 0.5, 1, 0)  # Convert to binary

        results[file] = pred

    return gt, results


def calculate_metrics(gt, predictions):
    metrics = {}
    for name, pred in predictions.items():
        tp = np.sum((gt == 1) & (pred == 1))
        fp = np.sum((gt == 0) & (pred == 1))
        fn = np.sum((gt == 1) & (pred == 0))
        tn = np.sum((gt == 0) & (pred == 0))

        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
        iou = tp / (tp + fp + fn) if tp + fp + fn > 0 else 0

        metrics[name] = {
            "IoU": iou,
            "F1": f1,
            "Precision": precision,
            "Recall": recall
        }
    return metrics



def main():
    # File paths
    pred_files = [
        r"C:\Users\admin\Desktop\wanglei\预测\predict_test5vv0.tif",
        r"C:\Users\admin\Desktop\wanglei\预测\predict_test5vv2.tif",
        r"C:\Users\admin\Desktop\wanglei\预测\predict_test5vvvh01.tif",
        r"C:\Users\admin\Desktop\wanglei\预测\predict_test5vvvh23.tif",
        r"C:\Users\admin\Desktop\wanglei\预测\predict_test5vvvh0123.tif",
        r"C:\Users\admin\Desktop\wanglei\预测\predict_test5vvvhdem01234.tif"
    ]
    gt_file = r"C:\Users\admin\Desktop\wanglei\预测\test_region\1\新建文件夹\新建文件夹\label55.tif"


    # Check dimensions and values
    gt, predictions = check_dimensions_and_values(pred_files, gt_file)

    # Calculate metrics
    metrics = calculate_metrics(gt, predictions)

    # Print results
    for name, metric in metrics.items():
        print(f"Metrics for {name}:")
        for key, value in metric.items():
            print(f"  {key}: {value:.4f}")


if __name__ == "__main__":
    main()
