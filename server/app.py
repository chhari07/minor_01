import os
import threading
import io
import numpy as np
from flask import Flask, jsonify, send_file
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Reshape, Flatten, LeakyReLU
import kagglehub
from PIL import Image
import tensorflow as tf

app = Flask(__name__)

# Download the dataset using KaggleHub (updated dataset reference)
def download_dataset():
    # Use the specified dataset reference
    path = kagglehub.dataset_download("nikbearbrown/dalle-art-march-2023")
    return path

# Load and preprocess images (resize to 64x64 and normalize to [-1, 1])
def load_and_preprocess_images(path, img_size=(64, 64)):
    images = []
    for filename in os.listdir(path):
        if filename.endswith(('.jpg', '.png')):
            img_path = os.path.join(path, filename)
            img = Image.open(img_path).convert('RGB')
            img = img.resize(img_size)
            img = np.array(img)

            if img.shape == (img_size[0], img_size[1], 3):  # Ensure RGB format
                images.append(img)

    images = np.array(images)
    images = (images.astype(np.float32) - 127.5) / 127.5  # Normalize for GAN
    return images

# Generator model
def build_generator():
    model = Sequential([
        Dense(128, input_dim=100),
        LeakyReLU(0.2),
        Dense(256),
        LeakyReLU(0.2),
        Dense(512),
        LeakyReLU(0.2),
        Dense(1024),
        LeakyReLU(0.2),
        Dense(64 * 64 * 3, activation='tanh'),
        Reshape((64, 64, 3))
    ])
    return model

# Discriminator model
def build_discriminator():
    model = Sequential([
        Flatten(input_shape=(64, 64, 3)),
        Dense(512),
        LeakyReLU(0.2),
        Dense(256),
        LeakyReLU(0.2),
        Dense(1, activation='sigmoid')
    ])
    return model

# Training the GAN
def train_gan(x_train, epochs=10000, batch_size=128):
    generator = build_generator()
    discriminator = build_discriminator()

    discriminator.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    gan = Sequential([generator, discriminator])
    discriminator.trainable = False
    gan.compile(optimizer='adam', loss='binary_crossentropy')

    half_batch = batch_size // 2

    for epoch in range(epochs):
        idx = np.random.randint(0, x_train.shape[0], half_batch)
        real_images = x_train[idx]

        noise = np.random.normal(0, 1, (half_batch, 100))
        fake_images = generator.predict(noise)

        d_loss_real = discriminator.train_on_batch(real_images, np.ones((half_batch, 1)))
        d_loss_fake = discriminator.train_on_batch(fake_images, np.zeros((half_batch, 1)))
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

        noise = np.random.normal(0, 1, (batch_size, 100))
        g_loss = gan.train_on_batch(noise, np.ones((batch_size, 1)))

        print(f"{epoch}/{epochs} [D loss: {d_loss[0]}, acc.: {100 * d_loss[1]}] [G loss: {g_loss}]")

# Generate an image
def generate_image(generator):
    noise = np.random.normal(0, 1, (1, 100))
    generated_image = generator.predict(noise)
    generated_image = (generated_image[0] * 127.5 + 127.5).astype(np.uint8)

    pil_image = Image.fromarray(generated_image)
    img_io = io.BytesIO()
    pil_image.save(img_io, 'PNG')
    img_io.seek(0)

    return img_io

# Start GAN training
@app.route('/train_gan', methods=['POST'])
def start_training():
    dataset_path = download_dataset()
    x_train = load_and_preprocess_images(dataset_path)

    threading.Thread(target=train_gan, args=(x_train, 10000, 64)).start()
    return jsonify({"message": "Training started!"}), 202

# Generate image endpoint
@app.route('/generate_image', methods=['GET'])
def generate_image_route():
    generator = build_generator()
    generated_image = generate_image(generator)

    return send_file(generated_image, mimetype='image/png')

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
