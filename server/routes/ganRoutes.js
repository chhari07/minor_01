// ganRoutes.js
const express = require('express');
const axios = require('axios');
const router = express.Router();

// Start GAN training
router.post('/train-gan', async (req, res) => {
    try {
        const response = await axios.post('http://localhost:3000/train_gan');
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Generate GAN image
router.get('/create-post', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:3000/generate_image', {
            responseType: 'arraybuffer'
        });
        res.setHeader('Content-Type', 'image/png');
        res.send(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
