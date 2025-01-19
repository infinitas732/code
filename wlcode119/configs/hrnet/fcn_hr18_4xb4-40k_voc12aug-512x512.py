_base_ = [
    '../_base_/models/fcn_hr18.py', '../_base_/datasets/water_tif_5.py',
    '../_base_/default_runtime.py', '../_base_/schedules/my_schedule.py'
]
crop_size = (256, 256)
data_preprocessor = dict(size=crop_size)
model = dict(
    data_preprocessor=data_preprocessor, decode_head=dict(num_classes=2))
