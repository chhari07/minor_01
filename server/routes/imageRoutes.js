const express = require('express');
const tf = require('@tensorflow/tfjs-node');
const router = express.Router();
const path = require('path');

let generator;

// Load the GAN model
(async () => {
    try {
        generator = await tf.loadLayersModel(`file://${path.join(__dirname, '../models/generator_model.h5')}`);
        console.log('GAN model loaded successfully.');
    } catch (error) {
        console.error('Error loading GAN model:', error);
    }
})();

// Route to generate an image
router.get('/', async (req, res) => {
    try {
        if (!generator) {
            return res.status(500).json({ error: 'Model is not loaded yet' });
        }

        // Generate a random noise vector
        const noise = tf.randomNormal([1, 100]);

        // Generate the image from the noise vector
        const generatedImage = generator.predict(noise);

        // Process and send the image
        const imageBuffer = await tf.node.encodeJpeg(
            generatedImage.mul(127.5).add(127.5).cast('int32')
        );
        res.set('Content-Type', 'image/jpeg');
        res.send(imageBuffer);
    } catch (error) {
        console.error('Error generating image:', error);
        res.status(500).send('Error generating image');
    }
});

module.exports = router;
