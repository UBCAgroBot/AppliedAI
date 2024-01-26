####################################
SEED = 1032
N_FOLDS = 3
BATCH_SIZE = 16
IMGSZ = 384                                         ## ?
EPOCHS = 1
INIT_LR = 2e-4
NUM_WORKER = 8
PATIENCE = 3                                        ## For early stopping - how does this fit in with early stopping?
MODEL_BASE = 'convnext_base.fb_in22k'               ## Change this to change what pretrained model you want to use - KEEP THIS
DATASET_DIR = '../../Dataset/Zindi_Crop_Damage'
IMAGE_DIR = DATASET_DIR + '/images'

SWITCHES = {
  'REDUCED_TRAINING_SET': True,
  "TRAINING": True,
  "TESTING": False 
}

REDUCED_TRAINING_SIZE = 100
