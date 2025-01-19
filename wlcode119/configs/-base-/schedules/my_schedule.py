iters=80000
# optimizer
# optimizer = dict(type='AdamW', lr=0.001, weight_decay=0.0005)  # 使用AdamW优化器，学习率可根据需要调整
optimizer = dict(type='AdamW', lr=0.00001, weight_decay=1e-4)  # 使用AdamW优化器，学习率可根据需要调整
optim_wrapper = dict(type='OptimWrapper', optimizer=optimizer, clip_grad=None)

# learning policy
param_scheduler = [
    dict(
        type='PolyLR',
        eta_min=1e-6,
        power=0.9,
        begin=0,
        end=80000,
        by_epoch=False)
]

# training schedule for 40k
train_cfg = dict(type='IterBasedTrainLoop', max_iters=80000, val_interval=iters//10)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')

default_hooks = dict(
    timer=dict(type='IterTimerHook'),
    logger=dict(type='LoggerHook', interval=500, log_metric_by_epoch=False),
    param_scheduler=dict(type='ParamSchedulerHook'),
    checkpoint=dict(type='CheckpointHook', by_epoch=False, interval=iters//10),
    sampler_seed=dict(type='DistSamplerSeedHook'),
    visualization=dict(type='SegVisualizationHook'))
