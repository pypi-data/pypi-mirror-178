#---------------------------------------------------------------------------
# configuration file
#---------------------------------------------------------------------------

############################################################################
# handy class for dictionary


from biom3d.configs.unet_pancreas import NUM_CLASSES, NUM_WORKERS


class Dict(dict):
    def __init__(self, *args, **kwargs): super().__init__(*args, **kwargs)
    def __getattr__(self, name): return self[name]
    def __setattr__(self, name, value): self[name] = value
    def __delattr__(self, name): del self[name]

############################################################################

#---------------------------------------------------------------------------
# Logs configs

CSV_DIR = 'data/pancreas/folds_pancreas.csv'

IMG_DIR = 'data/pancreas/tif_imagesTr'

MSK_DIR = 'data/pancreas/tif_labelsTr_small'

LOG_DIR = 'logs/'

DESC = 'nnet-triplet_pancreas'

#---------------------------------------------------------------------------
# training configs

SAVE_BEST = True # whether we save also the best model 

NB_EPOCHS = 1000
BATCH_SIZE = 2
LR_START = 1e-2 # comment if need to reload learning rate after training interruption
# LR_START = 5e-4 # comment if need to reload learning rate after training interruption
# LR_MILESTONES = [100, NB_EPOCHS//2, NB_EPOCHS-100]
# LR_T_MAX = NB_EPOCHS
WEIGHT_DECAY = 3e-5

USE_DEEP_SUPERVISION = False
NUM_POOLS = [3,5,5]
# NUM_POOLS = [3,4,4]
# NUM_POOLS = [4,5,5]

NUM_CLASSES = 2

PATCH_SIZE = [40,224,224]

# LOCAL_PATCH_SIZE = [40,128,128]
AUG_PATCH_SIZE = [48,263,263]

# OUT_DIM = 1024
# OUT_DIM = 65536

# MEDIAN_SPACING=[0.79492199, 0.79492199, 2.5]

USE_FP16 = True

USE_SOFTMAX = False

MEDIAN_SPACING=[0.79492199, 0.79492199, 2.5]

NUM_WORKERS=4

#---------------------------------------------------------------------------
# callback setup

SAVE_MODEL_EVERY_EPOCH = 1

VAL_EVERY_EPOCH = SAVE_MODEL_EVERY_EPOCH

USE_IMAGE_CLBK = True
SAVE_IMAGE_EVERY_EPOCH = SAVE_MODEL_EVERY_EPOCH

USE_FG_CLBK = True

# USE_WD_CLBK = False
# INITIAL_WD = 0.04
# INITIAL_WD = 0.00003
# FINAL_WD = 0.04
# FINAL_WD = 0.00003

USE_MOMENTUM_CLBK = False
# INITIAL_MOMENTUM = 0.9996

USE_OVERLAP_CLBK = True

#---------------------------------------------------------------------------
# dataset configs

TRAIN_DATALOADER = Dict(
    fct="TripletSeg",
    kwargs=Dict(
        img_dir    = IMG_DIR,
        msk_dir    = MSK_DIR,
        batch_size = BATCH_SIZE, 
        nbof_steps = 250,
        patch_size = PATCH_SIZE,
        folds_csv  = CSV_DIR, 
        fold       = 0, 
        val_split  = 0,
        train      = True,
        use_aug    = True,
        aug_patch_size = AUG_PATCH_SIZE,
        fg_rate = 0.33, # if > 0, force the use of foreground, needs to run some pre-computations (note: better use the foreground scheduler)
        crop_scale = 1.0, # if > 1, then use random_crop_resize instead of random_crop_pad
        use_softmax = USE_SOFTMAX, # if true, means that the output is one_hot encoded for softmax use
        num_workers=NUM_WORKERS,
    )
)

# TRAIN_DATALOADER_KWARGS = Dict(
#     batch_size  =BATCH_SIZE, 
#     drop_last   =False, 
#     shuffle     =True, 
#     num_workers =6, 
#     pin_memory  =True,
# )          


VAL_DATASET = Dict(
    fct="SegPatchFast",
    kwargs = Dict(
        img_dir    = IMG_DIR,
        msk_dir    = MSK_DIR, 
        batch_size = BATCH_SIZE, 
        patch_size = PATCH_SIZE,
        nbof_steps = 50,
        folds_csv  = CSV_DIR, 
        fold       = 0, 
        val_split  = 0.20,
        train      = False,
        use_aug    = False,
        use_softmax  = USE_SOFTMAX,
        fg_rate    = 0.33,
    )
)

VAL_DATALOADER_KWARGS = Dict(
    batch_size  =BATCH_SIZE, # TODO: change it in the final version
    drop_last   =False, 
    shuffle     =False, 
    num_workers =NUM_WORKERS, 
    # num_workers =0, 
    pin_memory  =True,
)


#---------------------------------------------------------------------------
# model configs

# MODEL = Dict(
#     fct="VGG3D", 
#     kwargs = Dict(
#         num_pools=NUM_POOLS,
#         use_emb=True,
#         emb_dim=320,
#         factor=32,
#         use_head=True,
#     )
# )

# MODEL = Dict(
#     fct="VGG3DMLP", 
#     kwargs = Dict(
#         num_pools=NUM_POOLS,
#         emb_dim=320,
#         out_dim=320,
#         factor=32,
#     )
# )


# MODEL = Dict(
#     fct="NNet", 
#     kwargs = Dict(
#         num_pools=NUM_POOLS,
#         num_classes=2, 
#         factor=32,
        
#         # encoder parameters
#         emb_dim=320,
#         out_dim=320,
#     )
# )

MODEL = Dict(
    fct="CotUNet", # from the register
    kwargs = Dict(
        patch_size=PATCH_SIZE,
        num_pools=NUM_POOLS,
        num_classes=NUM_CLASSES,
        factor = 32,
    )
)

#---------------------------------------------------------------------------
# loss configs


TRAIN_LOSS = Dict(
    fct="TripletSeg",
    kwargs = Dict(
        name="train_loss",
        alpha=0.2,
        use_softmax = USE_SOFTMAX,
    )
)

# TRAIN_LOSS = Dict(
#     fct="FocalLoss",
#     kwargs = Dict(
#         name="train_loss",
#         # num_classes=320,
#         gamma=2,
#     )
# )

VAL_LOSS = Dict(
    fct="DiceBCE",
    kwargs = Dict(name="val_loss", use_softmax=USE_SOFTMAX)
)

#---------------------------------------------------------------------------
# metrics configs

VAL_METRICS = Dict(
    val_iou=Dict(
        fct="IoU",
        kwargs = Dict(name="val_iou", use_softmax=USE_SOFTMAX)),
    val_dice=Dict(
        fct="Dice",
        kwargs=Dict(name="val_dice", use_softmax=USE_SOFTMAX)),
)

#---------------------------------------------------------------------------
# trainers configs

TRAINER = Dict(
    fct="TripletSegTrain",
    kwargs=Dict(),
)

VALIDATER = Dict(
    fct="SegVal",
    kwargs=Dict(),
)

#---------------------------------------------------------------------------
# predictors configs

PREDICTOR = Dict(
    fct="SegPatch",
    kwargs=Dict(patch_size=PATCH_SIZE, tta=True, median_spacing=MEDIAN_SPACING, use_softmax=USE_SOFTMAX),
)

############################################################################
# end of config file
# do not write anything in or below this field

CONFIG = Dict(**globals().copy()) # stores all variables in one Dict

to_remove = ['__name__', '__doc__', '__package__',
    '__loader__' , '__spec__', '__annotations__',
    '__builtins__', '__file__', '__cached__', 'Dict']

for k in to_remove: 
    if (k in CONFIG.keys()): del CONFIG[k] 

############################################################################
