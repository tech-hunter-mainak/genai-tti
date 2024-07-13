import gradio as gr
import tensorflow as tf

# Load a pre-trained model (for example, a TensorFlow model)
model = tf.keras.applications.MobileNetV2(weights='imagenet')

def classify_image(img):
    img = tf.image.resize(img, (224, 224))
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    preds = model.predict(tf.expand_dims(img, axis=0))
    decoded_preds = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=5)[0]
    return {label: float(score) for (_, label, score) in decoded_preds}

# Define the interface
iface = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(type="numpy"),  # Use type="numpy" to ensure the image is passed as a numpy array
    outputs=gr.Label(num_top_classes=5),
    title="Image Classifier",
    description="Upload an image to classify it using MobileNetV2."
)

# Launch the interface
iface.launch()
