const axios = require('axios');

app.post('/train-gan', async (req, res) => {
    try {
        const response = await axios.post('http://localhost:5000/train_gan');
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/generate-image', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/generate_image', {
            responseType: 'arraybuffer'
        });
        res.setHeader('Content-Type', 'image/png');
        res.send(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});
