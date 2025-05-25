import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

export const fetchCollectionStats = async () => {
    try {
        const response = await axios.get(`${API_URL}/collection-stats/`);
        return response.data;
    } catch (error) {
        console.error('Error fetching collection stats:', error);
        throw error;
    }
};