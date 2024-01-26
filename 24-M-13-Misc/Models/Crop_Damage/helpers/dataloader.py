from conf.conf import SWITCHES, REDUCED_TRAINING_SIZE

def prepare_train_data(data, kfold, image_dir):    # df is type pandas.DataFrame
    """
    Helper function to get the data ready
    """
    df = data.copy()
    if SWITCHES['REDUCED_TRAINING_SET']:
      df = df.head(REDUCED_TRAINING_SIZE)

    df['image_id'] = df['filename'].apply(lambda x: x.split('.')[0])
    df = df.drop_duplicates(subset='image_id', keep='first')

    df['target'] = df['damage']

    df['fold'] = -1
    for i, (train_idx, val_idx) in enumerate(kfold.split(df, df['target'])):
        df.loc[val_idx, 'fold'] = i

    print(df.groupby(['fold', 'target']).size())

    df['path'] = df['filename'].apply(lambda x: f'{image_dir}/{x}')
    df['fold'] = df['fold'].astype('int')

    return df
