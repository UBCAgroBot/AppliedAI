from fastai.vision.all import *
from conf.conf import SEED, N_FOLDS, BATCH_SIZE, IMGSZ, EPOCHS, INIT_LR, NUM_WORKER, PATIENCE, MODEL_BASE
from helpers.eval import cross_entropy
from timm import create_model

# Creates an ensemble of 3 models?
def train_model(data):
    df = data.copy()

    for fold in range(N_FOLDS):
        df['is_valid'] = (df['fold'] == fold)
        print(f'Training fold: {fold}')
        dls = ImageDataLoaders.from_df(
                df, #pass in train DataFrame
                valid_col='is_valid',
                seed=SEED, #seed
                fn_col='path', #filename/path is in the second column of the DataFrame
                label_col='target', #label is in the first column of the DataFrame
                label_delim=' ',
                y_block=MultiCategoryBlock, #The type of target
                bs=BATCH_SIZE, #pass in batch size
                num_workers=NUM_WORKER,
                item_tfms=Resize(IMGSZ), #pass in item_tfms
                batch_tfms=setup_aug_tfms([Brightness(), Contrast(), Flip(), Rotate()])) # TRY DIFFERENT TYPES OF AUGMENTATION

        model = create_model(f'{MODEL_BASE}', pretrained=True, num_classes=dls.c)
        """
        "dls" - DataLoader object
        """
        # Binary Cross Entropy? Isn't this multi-class classification?
        learn = Learner(dls, model, loss_func=BCEWithLogitsLossFlat(), metrics=AccumMetric(cross_entropy)).to_fp16()

        # Trains a model for "EPOCHS" number of epochs using 1cycle policy (poicy)
        #   https://arxiv.org/abs/1708.07120
        learn.fit_one_cycle(EPOCHS, INIT_LR, cbs=[SaveModelCallback(), EarlyStoppingCallback(monitor='cross_entropy', comp=np.less, patience=PATIENCE), CSVLogger(append=True)])

        # What inside the learner are you setting to be 32-bit floating point precision?
        learn = learn.to_fp32()
        learn.save(f'{MODEL_BASE}_fold{fold}', with_opt=False)
