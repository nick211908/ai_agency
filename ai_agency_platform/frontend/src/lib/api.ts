import axios from 'axios';

const AUTH_API_URL = process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8001/api/v1';
const PIPELINE_API_URL = process.env.NEXT_PUBLIC_PIPELINE_API_URL || 'http://localhost:8002';

const authApi = axios.create({
    baseURL: AUTH_API_URL,
});

const pipelineApi = axios.create({
    baseURL: PIPELINE_API_URL,
});

// Interceptor to add token to requests
authApi.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const api = {
    auth: {
        login: async (username: string, password: string) => {
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);
            return authApi.post('/login/access-token', formData);
        },
        me: async () => {
            return authApi.get('/users/me');
        }
    },
    agency: {
        run: async (prompt: string, type: string) => {
            return pipelineApi.post('/run-agency', { prompt, agency_type: type });
        },
        ingest: async (file: File) => {
            const formData = new FormData();
            formData.append('file', file);
            return pipelineApi.post('/ingest', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
        }
    }
};
