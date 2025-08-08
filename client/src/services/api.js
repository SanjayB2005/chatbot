import axios from 'axios';

// Use empty base URL to leverage Vite's proxy configuration
// Vite will proxy /api requests to http://localhost:3003
const API_BASE_URL = '';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor
apiClient.interceptors.request.use(
    (config) => {
        const fullUrl = `${window.location.origin}${config.url}`;
        console.log(`🚀 Making ${config.method?.toUpperCase()} request to: ${fullUrl}`);
        console.log('🔧 Request will be proxied to: http://localhost:3003' + config.url);
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor with better error handling
apiClient.interceptors.response.use(
    (response) => {
        console.log('✅ API Success:', response.config.url, response.data);
        return response.data;
    },
    (error) => {
        console.error('❌ API Error:', error.config?.url, error.response?.data || error.message);
        
        // Provide more specific error messages
        if (error.code === 'ERR_NETWORK') {
            console.error('Network Error: Unable to connect to backend server via Vite proxy');
            console.error('Make sure the backend server is running on port 3003');
            console.error('Vite proxy should forward /api requests to http://localhost:3003');
        }
        
        return Promise.reject(error.response?.data || error);
    }
);

export const chatAPI = {
    // Create a new chat session
    createSession: (title = 'New Chat') =>
        apiClient.post('/api/v1/chat/session', { title }),

    // Send a message
    sendMessage: (sessionId, message) => {
        console.log('🚀 API Call: sendMessage', { sessionId, message });
        const request = apiClient.post('/api/v1/chat/message', { sessionId, message });
        request.then(response => {
            console.log('🔄 API Response: sendMessage', response);
        }).catch(error => {
            console.error('❌ API Error: sendMessage', error);
        });
        return request;
    },

    // Get chat history
    getChatHistory: (sessionId, limit = 50, offset = 0) =>
        apiClient.get(`/api/v1/chat/history/${sessionId}`, {
            params: { limit, offset }
        }),

    // Get all sessions
    getSessions: () =>
        apiClient.get('/api/v1/chat/sessions'),

    // Process questions with document (HackRx endpoint)
    processQuestions: (documents, questions) =>
        apiClient.post('/api/v1/chat/hackrx/run', { documents, questions }),

    // Health check
    healthCheck: () =>
        apiClient.get('/api/v1/health')
};

export default apiClient;
