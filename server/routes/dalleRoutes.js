const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');

router.post('/generate-image', (req, res) => {
    const prompt = req.body.prompt;

    // Call the Python script
    const pythonProcess = spawn('python3', ['ml_model/image_gen.py', JSON.stringify({ prompt })]);

    pythonProcess.stdout.on('data', (data) => {
        const result = JSON.parse(data.toString());
        res.json({ success: true, image: result.image_data });
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
        res.status(500).json({ success: false, error: 'Image generation failed' });
    });
});

module.exports = router;
