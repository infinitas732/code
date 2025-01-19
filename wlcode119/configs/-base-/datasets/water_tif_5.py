
# dataset settings
dataset_type = 'Water_TIF_Dataset'
data_root = 'data/dataset_origin/water'
img_scale = (256, 256)
crop_size = (256, 256)

# Updated train_pipeline without data augmentation
train_pipeline = [
    dict(type='LoadTiffImageFromFile'),  # Load the image from TIFF file
    dict(type='LoadAnnotations'),  # Load the annotations (ground truth labels)
    dict(type='PackSegInputs')  # Pack the input data for model
]

# Updated test_pipeline without any augmentations
test_pipeline = [
    dict(type='LoadTiffImageFromFile'),  # Load the image from TIFF file
    dict(type='LoadAnnotations'),  # Load the annotations (ground truth labels)
    dict(type='PackSegInputs')  # Pack the input data for model
]

# Removing augmentations from TTA (Test-Time Augmentation)
img_ratios = [1.0]  # No need for multiple scaling ratios


train_dataloader = dict(
    batch_size=4,
    num_workers=1,
    persistent_workers=True,
    sampler=dict(type='InfiniteSampler', shuffle=True),
    dataset=dict(
        type='RepeatDataset',
        # times=40000,
        times=1000,
        dataset=dict(
            type=dataset_type,
            data_root=data_root,
            data_prefix=dict(
                img_path='images/training',
                seg_map_path='annotations/training'),
            pipeline=train_pipeline))
)

val_dataloader = dict(
    batch_size=1,
    num_workers=1,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        data_prefix=dict(
            img_path='images/validation',
            seg_map_path='annotations/validation'),
        pipeline=test_pipeline)
)

test_dataloader = val_dataloader

val_evaluator = dict(type='IoUMetric', iou_metrics=['mIoU', 'mFscore'])
test_evaluator = val_evaluator



# # dataset settings
# dataset_type = 'Water_TIF_Dataset'
# data_root = 'data/dataset_origin/water'
# img_scale = (256, 256)
# crop_size = (256, 256)
#
# train_pipeline = [
#     dict(type='LoadTiffImageFromFile'),
#     dict(type='LoadAnnotations'),
#     dict(
#         type='RandomResize',
#         scale=img_scale,
#         # ratio_range=(0.5, 2.0),
#         ratio_range=(0.5, 2.0),
#         keep_ratio=True),
#     dict(type='RandomCrop', crop_size=crop_size, cat_max_ratio=0.75),
#     dict(type='RandomFlip', prob=0.5),
#     dict(type='PhotoMetricDistortion'),
#     dict(type='PackSegInputs')
# ]
#
# test_pipeline = [
#     dict(type='LoadTiffImageFromFile'),
#     dict(type='Resize', scale=img_scale, keep_ratio=True),
#     # add loading annotation after ``Resize`` because ground truth
#     # does not need to do resize data transform
#     dict(type='LoadAnnotations'),
#     dict(type='PackSegInputs')
# ]
# img_ratios = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75]
# # img_ratios = [0.75, 1.0, 1.25]
# tta_pipeline = [
#     dict(type='LoadTiffImageFromFile', backend_args=None),
#     dict(
#         type='TestTimeAug',
#         transforms=[
#             [
#                 dict(type='Resize', scale_factor=r, keep_ratio=True)
#                 for r in img_ratios
#             ],
#             [
#                 dict(type='RandomFlip', prob=0., direction='horizontal'),
#                 dict(type='RandomFlip', prob=1., direction='horizontal')
#             ], [dict(type='LoadAnnotations')], [dict(type='PackSegInputs')]
#         ])
# ]
# train_dataloader = dict(
#     batch_size=4,
#     num_workers=1,
#     persistent_workers=True,
#     sampler=dict(type='InfiniteSampler', shuffle=True),
#     # dataset=dict(
#     #     type='RepeatDataset',
#     #     # times=40000,
#     #     times=1000,
#     dataset=dict(
#             type=dataset_type,
#             data_root=data_root,
#             data_prefix=dict(
#                 img_path='images/training',
#                 seg_map_path='annotations/training'),
#             pipeline=train_pipeline))
# val_dataloader = dict(
#     batch_size=1,
#     num_workers=1,
#     persistent_workers=True,
#     sampler=dict(type='DefaultSampler', shuffle=False),
#     dataset=dict(
#         type=dataset_type,
#         data_root=data_root,
#         data_prefix=dict(
#             img_path='images/validation',
#             seg_map_path='annotations/validation'),
#         pipeline=test_pipeline))
# test_dataloader = val_dataloader
#
# val_evaluator = dict(type='IoUMetric', iou_metrics=['mIoU', 'mFscore'])
# test_evaluator = val_evaluator