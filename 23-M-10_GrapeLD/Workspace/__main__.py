import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import json
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras import Model
from tensorflow.keras import layers
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import CSVLogger

BATCH_SIZE = 64
VALIDATION_SPLIT = 0.1
SEED = 123


def load_data():
    """
    Importing the dataset into the model
    """

    # Image batch: (64, 256, 256, 3)
    # Labels batch: (64, 10)

    # train
    train_ds = tf.keras.utils.image_dataset_from_directory(
        "data/concatenated_datasets",
        validation_split=VALIDATION_SPLIT,
        subset="training",
        seed=SEED,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
    )

    # dev
    dev_ds = tf.keras.utils.image_dataset_from_directory(
        "data/concatenated_datasets",
        validation_split=VALIDATION_SPLIT,
        subset="validation",
        seed=SEED,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
    )

    normalization_layer = layers.Rescaling(1.0 / 255)
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    dev_ds = dev_ds.map(lambda x, y: (normalization_layer(x), y))

    return train_ds, dev_ds


def callbacks():
    """
    Adding a bunch of callbacks just to make sure there's information on the training process
    """
    tensorboard_callback = TensorBoard(log_dir="./logs")
    csv_logger = CSVLogger("./logs/training.log")

    checkpoint_path = "training/cp-{epoch:04d}.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        verbose=1,
        save_weights_only=True,
        save_freq=5 * BATCH_SIZE,
    )

    return csv_logger, tensorboard_callback, cp_callback


def init_model(data, callbacks):
    """
    Making the actual model
    """
    csv_logger, tensorboard_callback, cp_callback = callbacks
    train_ds, dev_ds = data

    weights_path = "/scratch/st-sielmann-1/agrobot/grape-ld/pretrained_weights/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5"
    pre_trained_model = InceptionV3(
        input_shape=(256, 256, 3), include_top=False, weights=weights_path
    )

    for layer in pre_trained_model.layers:
        layer.trainable = False

    x = layers.Flatten()(pre_trained_model.output)
    x = layers.Dense(1024, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(1024, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(10, activation="softmax")(x)

    model = Model(pre_trained_model.input, x)
    model.compile(
        optimizer=RMSprop(learning_rate=0.0001),
        loss="categorical_crossentropy",
        metrics=["acc"],
    )

    return model


if __name__ == "__main__":
    data = load_data()
    print("FINISHED LOADING DATA")
    callbacks = callbacks()
    print("FINISHED INITIALIZING CALLBACKS")
    model = init_model(data, callbacks)
    print("FINISHED COMPILING MODEL")

    train_ds, dev_ds = data
    csv_logger, tensorboard_callback, cp_callback = callbacks

    history = model.fit(
        train_ds,
        validation_data=dev_ds,
        epochs=120,
        batch_size=BATCH_SIZE,
        verbose=2,
        callbacks=[csv_logger, tensorboard_callback, cp_callback],
    )
    print("FINISHED TRAINING MODEL")

    model.save_weights("./checkpoints/model")
    history_dict = history.history
    json.dump(history_dict, open("./history.json", "w"))
    print("MODEL SAVED")
