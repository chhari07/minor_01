const mongoose = require('mongoose');

const connectDB = async () => {
    try {
        if (!process.env.MONGO_URI) {
            throw new Error("Missing MONGO_URI environment variable");
        }

        console.log("Connecting to MongoDB...");

        await mongoose.connect(process.env.MONGO_URI, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });

        console.log('MongoDB connected successfully');
    } catch (error) {
        console.error('MongoDB connection error:', error.message || error);
        process.exit(1); // Exit process with failure
    }
};

module.exports = connectDB;
