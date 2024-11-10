import axios from 'axios';

export const generateImage = async () => {
    try {
        const response = await axios.get('/api/generate', { responseType: 'blob' });
        const imageUrl = URL.createObjectURL(response.data);
        return imageUrl;
    } catch (error) {
        console.error('Error generating image:', error);
        return null;
    }
};
