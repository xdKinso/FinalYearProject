import api from '../components/api';

const handleSubmitStats = async (e, username, setStats, setFortniteStats, setError) => {
    e.preventDefault();
    setError('');
    setStats(null);
    try {
        const response = await api.get(`/Fnstats?username=${username}`);
        if (response.data) {
            setStats(response.data);
            setFortniteStats(response.data);
        }
    } catch (err) {
        setError('Failed to fetch Fortnite stats. Please ensure the username is correct.');
    }
};

export default handleSubmitStats;
