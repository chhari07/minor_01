// index.js
const express = require('express');
const app = express();
const ganRoutes = require('./routes/ganRoutes');

app.use(express.json());

// Use GAN routes
app.use('/api/gan', ganRoutes);
const PORT = process.env.PORT || 3001; // Change 3000 to another port, like 3001
app.listen(PORT, () => {
    console.log(`Node.js server running on port ${PORT}`);
});
