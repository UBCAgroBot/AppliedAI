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
from conf.conf import SEED, N_FOLDS, BATCH_SIZE, IMGSZ, EPOCHS, INIT_LR, NUM_WORKER, PATIENCE, MODEL_BASE, DATASET_DIR, IMAGE_DIR

####################################
TTA = 5
SAVE_NAME = 'convnext_base.fb_in22k'
####################################

def eval_model(train_data):
    os.makedirs('submission', exist_ok=True)

    test_df = pd.read_csv(f'{DATASET_DIR}/Test.csv')
    test_df['path'] = test_df['filename'].map(lambda x: f'{IMAGE_DIR}/{x}')

    ensemble = []
    for fold in range(N_FOLDS):
        dls = ImageDataLoaders.from_df(
                train_data, #pass in train DataFrame
                valid_pct=0.2, #80-20 train-validation random split
                seed=SEED, #seed
                fn_col='path', #filename/path is in the second column of the DataFrame
                label_col='target', #label is in the first column of the DataFrame
                label_delim=' ',
                y_block=MultiCategoryBlock, #The type of target
                bs=BATCH_SIZE, #pass in batch size
                num_workers=NUM_WORKER,
                item_tfms=Resize(IMGSZ), #pass in item_tfms
                batch_tfms=setup_aug_tfms([Brightness(), Contrast(), Flip(), Rotate()]))
        model = create_model(f'{MODEL_BASE}', pretrained=False, num_classes=dls.c)
        learn = Learner(dls, model, loss_func=CrossEntropyLossFlat(), metrics=AccumMetric(cross_entropy)).to_fp16()

        model = learn.load(f'{MODEL_BASE}_fold{fold}')
        test_df['target'] = [1]*len(test_df)

        test_dl = dls.test_dl(test_df)
        # What's the benefit of Test-time augmentation? Does this prevent me from thinking my model
        #        is super wrong, or that it is super coorect?
        preds, _ = learn.tta(dl=test_dl, n=TTA, beta=0)
        ensemble.append(preds.numpy())

    test_df = test_df.join(pd.DataFrame(np.mean(ensemble, axis=0), columns=dls.vocab))

    sample_submission_df = pd.read_csv(f"{DATASET_DIR}/SampleSubmission.csv")
    sample_submission_df = sample_submission_df['ID']
    sample_submission_df = pd.merge(sample_submission_df, test_df, on='ID')
    sample_submission_df = sample_submission_df[['ID']+dls.vocab]
    sample_submission_df.to_csv(f"submission/{MODEL_BASE}_tta_{TTA}.csv", index=False)

    sample_submission_df




