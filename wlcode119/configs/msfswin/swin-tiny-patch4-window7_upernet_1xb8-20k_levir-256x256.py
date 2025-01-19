_base_ = [
    '../_base_/models/upernet_swin.py', '../_base_/datasets/water_tif_5.py',
    '../_base_/default_runtime.py', '../_base_/schedules/my_schedule.py'
]
crop_size = (256, 256)
norm_cfg = dict(type='BN', requires_grad=True)
data_preprocessor = dict(
    size=crop_size,
    type='SegDataPreProcessor',
    # mean=[-15.387361,  -26.211157,  -15.564406 , -26.09502 , 4940.449 ],
    # std=[4.9407945 ,  6.5085716 ,  5.4602036 ,  6.539861 , 355.92834],
    bgr_to_rgb=False)

model = dict(
    data_preprocessor=data_preprocessor,
    backbone=dict(
        in_channels=5,
        embed_dims=96,
        depths=[2, 2, 6, 2],
        num_heads=[3, 6, 12, 24],
        window_size=7,
        use_abs_pos_embed=False,
        drop_path_rate=0.3,
        patch_norm=True),
    decode_head=dict(in_channels=[96, 192, 384, 256], num_classes=2),
    # decode_head=dict(in_channels=[512, 512, 512, 512], num_classes=2),
    auxiliary_head=dict(in_channels=384, num_classes=2))
    # decode_head=dict(in_channels=[96, 192, 384, 768], num_classes=2),
    # auxiliary_head=dict(in_channels=384, num_classes=2))

# AdamW optimizer, no weight decay for position embedding & layer norm
# in backbone
optim_wrapper = dict(
    _delete_=True,
    type='OptimWrapper',
    optimizer=dict(
        type='AdamW', lr=0.00001, betas=(0.9, 0.999), weight_decay=0.01),
    paramwise_cfg=dict(
        custom_keys={
            'absolute_pos_embed': dict(decay_mult=0.),
            'relative_position_bias_table': dict(decay_mult=0.),
            'norm': dict(decay_mult=0.)
        }))

param_scheduler = [
    dict(
        type='LinearLR', start_factor=1e-6, by_epoch=False, begin=0, end=1500),
    dict(
        type='PolyLR',
        eta_min=0.0,
        power=1.0,
        begin=1500,
        end=40000,
        by_epoch=False,
    )
]

train_dataloader = dict(batch_size=4)
val_dataloader = dict(batch_size=1)
test_dataloader = val_dataloader
