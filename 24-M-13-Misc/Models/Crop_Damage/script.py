from fastai.vision.all import *
from timm import create_model
import pandas as pd
import os
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import StratifiedKFold ## Used for divvying up our data. STRATIFIED k-fold ensures that for any specific class, that class is represented in each fold
                                                     #          in the same relative proportions (e.g., class 1 constitutes 1/3 of fold 1, and class 1 constitutues 1/3 of fold)
from sklearn.metrics import log_loss
from helpers.dataloader import prepare_train_data
from helpers.eval import cross_entropy
from helpers.trainer import train_model
from conf.conf import SEED, N_FOLDS, BATCH_SIZE, IMGSZ, EPOCHS, INIT_LR, NUM_WORKER, PATIENCE, MODEL_BASE, DATASET_DIR, IMAGE_DIR, SWITCHES
from helpers.tester import eval_model

set_seed(SEED, reproducible=True)

train = pd.read_csv(f'{DATASET_DIR}/Train.csv')
skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
train_data = prepare_train_data(train, skf, IMAGE_DIR)

if SWITCHES['TRAINING']:
    train_model(train_data)

if SWITCHES['TESTING']:
    eval_model(train_data)

