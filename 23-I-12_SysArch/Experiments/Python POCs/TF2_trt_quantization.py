import tensorflow as tf

from tensorflow import keras
# Define a simple sequential model
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10)
])

model.compile(optimizer='adam',
  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
  metrics=['accuracy'])

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
x_train = tf.cast(x_train, dtype=tf.float32)
y_train = tf.cast(y_train, dtype=tf.float32)
x_test = tf.cast(x_test, dtype=tf.float32)
y_test = tf.cast(y_test, dtype=tf.float32)


# Train the model
#model.fit(x_train, y_train, epochs=1)

# Evaluate your model accuracy
#model.evaluate(x_test,  y_test, verbose=2)

# Save model in the saved_model format
SAVED_MODEL_DIR="./models/native_saved_model"
model.save(SAVED_MODEL_DIR)

from tensorflow.python.compiler.tensorrt import trt_convert as trt

# Instantiate the TF-TRT converter
converter = trt.TrtGraphConverterV2(
    input_saved_model_dir=SAVED_MODEL_DIR,
    precision_mode=trt.TrtPrecisionMode.INT8,
    use_calibration=True
)

# Use data from the test/validation set to perform INT8 calibration
BATCH_SIZE=32
NUM_CALIB_BATCHES=10
def calibration_input_fn():
    for i in range(NUM_CALIB_BATCHES):
        start_idx = i * BATCH_SIZE
        end_idx = (i + 1) * BATCH_SIZE
        x = x_test[start_idx:end_idx, :]
        yield [x]

# Convert the model and build the engine with valid calibration data
func = converter.convert(calibration_input_fn=calibration_input_fn)
converter.build(calibration_input_fn)

OUTPUT_SAVED_MODEL_DIR="./models/tftrt_saved_model"
converter.save(output_saved_model_dir=OUTPUT_SAVED_MODEL_DIR)

converter.summary()

# Run some inferences!
for step in range(10):
    start_idx = step * BATCH_SIZE
    end_idx   = (step + 1) * BATCH_SIZE

    print(f"Step: {step}")
    x = x_test[start_idx:end_idx, :]
    func(x)