import api from '../components/api';

const fetchProfileData = async (setUserData, setError, navigate) => {
    try {
        const response = await api.get('/profile');
        if (response.status === 200) {
            setUserData(response.data);
        } else {
            setError('Failed to fetch profile data.');
        }
    } catch (err) {
        if (err.response?.status === 401) {
            navigate('/login');
        } else {
            setError('An error occurred.');
        }
    }
};

export default fetchProfileData;
