#---------------------------------------------------------------------------
# configuration file
#---------------------------------------------------------------------------

############################################################################
# handy class for dictionary

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

DESC = 'vgg-dino_pancreas'

#---------------------------------------------------------------------------
# training configs

SAVE_BEST = True # whether we save also the best model 

NB_EPOCHS = 50
BATCH_SIZE = 4
LR_START = 1e-2 # comment if need to reload learning rate after training interruption
# LR_START = 5e-4 # comment if need to reload learning rate after training interruption
# LR_MILESTONES = [100, NB_EPOCHS//2, NB_EPOCHS-100]
# LR_T_MAX = NB_EPOCHS

USE_DEEP_SUPERVISION = False
NUM_POOLS = [3,5,5]
# NUM_POOLS = [3,4,4]
# NUM_POOLS = [4,5,5]

GLOBAL_PATCH_SIZE = [40,224,224]

# LOCAL_PATCH_SIZE = [40,128,128]
LOCAL_PATCH_SIZE = [40,96,96]

OUT_DIM = 1024
# OUT_DIM = 65536

# MEDIAN_SPACING=[0.79492199, 0.79492199, 2.5]

USE_FP16 = True

#---------------------------------------------------------------------------
# callback setup

SAVE_MODEL_EVERY_EPOCH = 1

VAL_EVERY_EPOCH = SAVE_MODEL_EVERY_EPOCH

USE_IMAGE_CLBK = False
SAVE_IMAGE_EVERY_EPOCH = SAVE_MODEL_EVERY_EPOCH

USE_FG_CLBK = False

USE_WD_CLBK = True
INITIAL_WD = 0.04
# INITIAL_WD = 0.00003
FINAL_WD = 0.04
# FINAL_WD = 0.00003

USE_MOMENTUM_CLBK = True
INITIAL_MOMENTUM = 0.9996

#---------------------------------------------------------------------------
# dataset configs

NB_GLOBAL_PATCH = 3
NB_LOCAL_PATCH = 0

TRAIN_DATASET = Dict(
    fct="Dino",
    kwargs=Dict(
        img_dir    = IMG_DIR,
        batch_size = BATCH_SIZE, 
        nbof_steps = 250,
        global_patch_size = GLOBAL_PATCH_SIZE,
        local_patch_size = LOCAL_PATCH_SIZE,
        nbof_global_patch = NB_GLOBAL_PATCH,
        nbof_local_patch = NB_LOCAL_PATCH,
        folds_csv  = CSV_DIR, 
        fold       = 0, 
        val_split  = 0,
        train      = True,
        use_aug    = True,
    )
)

TRAIN_DATALOADER_KWARGS = Dict(
    batch_size  =BATCH_SIZE, 
    drop_last   =True, 
    shuffle     =True, 
    num_workers =6, 
    pin_memory  =True,
)          

#---------------------------------------------------------------------------
# model configs

MODEL = Dict(
    fct="SelfDino", # from the register
    kwargs = Dict(
        num_pools=NUM_POOLS,
        emb_dim=320,
        out_dim=OUT_DIM,
        factor=32,
    )
)

#---------------------------------------------------------------------------
# loss configs

WARMUP_TEACHER_TEMP = 0.04
TEACHER_TEMP = 0.04
WARMUP_TEACHER_TEMP_EPOCHS = 0
STUDENT_TEMP = 0.1
CENTER_MOMENTUM = 0.9


TRAIN_LOSS = Dict(
    fct="Dino",
    kwargs = Dict(
        name="train_loss",
        out_dim=OUT_DIM,
        nbof_global_crops=NB_GLOBAL_PATCH,
        nbof_local_crops=NB_LOCAL_PATCH,
        warmup_teacher_temp=WARMUP_TEACHER_TEMP,
        teacher_temp=TEACHER_TEMP,
        warmup_teacher_temp_epochs=WARMUP_TEACHER_TEMP_EPOCHS,
        student_temp=STUDENT_TEMP,
        center_momentum=CENTER_MOMENTUM,
        nepochs=NB_EPOCHS,
    )
)

#---------------------------------------------------------------------------
# metrics configs

TRAIN_METRICS = Dict(
    train_kldiv=Dict(
        fct="KLDiv",
        kwargs = Dict(name="train_kldiv", 
            out_dim=OUT_DIM,
            nbof_global_crops=NB_GLOBAL_PATCH,
            nbof_local_crops=NB_LOCAL_PATCH,
            warmup_teacher_temp=WARMUP_TEACHER_TEMP,
            teacher_temp=TEACHER_TEMP,
            warmup_teacher_temp_epochs=WARMUP_TEACHER_TEMP_EPOCHS,
            student_temp=STUDENT_TEMP,
            center_momentum=CENTER_MOMENTUM,
            nepochs=NB_EPOCHS,)),
    train_entropy=Dict(
        fct="Entropy",
        kwargs = Dict(name="train_entropy", 
            out_dim=OUT_DIM,
            nbof_global_crops=NB_GLOBAL_PATCH,
            nbof_local_crops=NB_LOCAL_PATCH,
            warmup_teacher_temp=WARMUP_TEACHER_TEMP,
            teacher_temp=TEACHER_TEMP,
            warmup_teacher_temp_epochs=WARMUP_TEACHER_TEMP_EPOCHS,
            student_temp=STUDENT_TEMP,
            center_momentum=CENTER_MOMENTUM,
            nepochs=NB_EPOCHS,)),
)

#---------------------------------------------------------------------------
# trainers configs

TRAINER = Dict(
    fct="DinoTrain",
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
