import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:5000', // Point to the Flask API
});

// Add a request interceptor
api.interceptors.request.use(config => {
    const token = sessionStorage.getItem('token');
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

// Add a response interceptor
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            // Check if the request was for the home page
            const isHomePage = error.config.url.includes('/'); 

            if (!isHomePage) {
                // Handle token expiry 
                sessionStorage.removeItem('token');
                window.location.href = '/login';
            }
            // Do not redirect if it's the home page
        }
        return Promise.reject(error);
    }
);

export default api;
