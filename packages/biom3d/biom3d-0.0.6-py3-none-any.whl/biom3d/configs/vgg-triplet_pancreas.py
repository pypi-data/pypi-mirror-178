#---------------------------------------------------------------------------
# configuration file
#---------------------------------------------------------------------------

############################################################################
# handy class for dictionary

from math import gamma

from biom3d.configs.unet_pancreas import NUM_CLASSES, NUM_WORKERS


class Dict(dict):
    def __init__(self, *args, **kwargs): super().__init__(*args, **kwargs)
    def __getattr__(self, name): return self[name]
    def __setattr__(self, name, value): self[name] = value
    def __delattr__(self, name): del self[name]

############################################################################

#---------------------------------------------------------------------------
# Logs configs

CSV_DIR = None

IMG_DIR = 'data/pancreas/tif_imagesTr'

LOG_DIR = 'logs/'

DESC = 'hrnet-triplet_pancreas'

#---------------------------------------------------------------------------
# training configs

SAVE_BEST = True # whether we save also the best model 

NB_EPOCHS = 500
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

PATCH_SIZE = [40,224,224]

# LOCAL_PATCH_SIZE = [40,128,128]
AUG_PATCH_SIZE = [40,263,263]

# OUT_DIM = 1024
# OUT_DIM = 65536

# MEDIAN_SPACING=[0.79492199, 0.79492199, 2.5]

USE_FP16 = True

NUM_WORKERS = 12

#---------------------------------------------------------------------------
# callback setup

SAVE_MODEL_EVERY_EPOCH = 1
VAL_EVERY_EPOCH = SAVE_MODEL_EVERY_EPOCH

USE_IMAGE_CLBK = False
SAVE_IMAGE_EVERY_EPOCH = SAVE_MODEL_EVERY_EPOCH

USE_FG_CLBK = False

USE_WD_CLBK = False
# INITIAL_WD = 0.04
# INITIAL_WD = 0.00003
# FINAL_WD = 0.04
# FINAL_WD = 0.00003

USE_MOMENTUM_CLBK = False
# INITIAL_MOMENTUM = 0.9996

USE_OVERLAP_CLBK = True

#---------------------------------------------------------------------------
# dataset configs

TRAIN_DATASET = Dict(
    fct="Triplet",
    kwargs=Dict(
        img_dir    = IMG_DIR,
        batch_size = BATCH_SIZE, 
        nbof_steps = 250,
        patch_size = PATCH_SIZE,
        folds_csv  = None, 
        fold       = 0, 
        val_split  = 0,
        train      = True,
        use_aug    = False,
        aug_patch_size = AUG_PATCH_SIZE,
    )
)

TRAIN_DATALOADER_KWARGS = Dict(
    batch_size  =BATCH_SIZE, 
    drop_last   =False, 
    shuffle     =True, 
    num_workers =NUM_WORKERS, 
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
    fct="HRNetMLP", 
    kwargs = Dict(
        patch_size=PATCH_SIZE,
        num_pools=NUM_POOLS, 
        num_classes=NUM_CLASSES, 
        factor=32,
        in_planes = 1,
    )
)

#---------------------------------------------------------------------------
# loss configs


TRAIN_LOSS = Dict(
    fct="Triplet",
    kwargs = Dict(
        name="train_loss",
        alpha=0.2,
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

#---------------------------------------------------------------------------
# metrics configs

#---------------------------------------------------------------------------
# trainers configs

TRAINER = Dict(
    fct="TripletTrain",
    kwargs=Dict(),
)

#---------------------------------------------------------------------------
# predictors configs

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
