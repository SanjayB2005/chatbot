const axios = require('axios');

class AIService {
    constructor() {
        this.baseURL = process.env.AI_SERVICE_URL || 'http://localhost:8000';
        this.apiKey = process.env.AI_SERVICE_API_KEY || 'your-api-key';
        
        if (this.apiKey === 'your-api-key') {
            console.warn('⚠️ AI_SERVICE_API_KEY not set in environment variables');
        }
    }

    async processQuestions(documentsUrl, questions) {
        try {
            const response = await axios.post(
                `${this.baseURL}/api/v1/hackrx/run`,
                {
                    documents: documentsUrl,
                    questions: questions
                },
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.apiKey}`
                    },
                    timeout: 60000 // 60 seconds timeout
                }
            );

            return response.data;
        } catch (error) {
            console.error('Error calling AI service:', error.message);
            throw error;
        }
    }

    async chatResponse(message) {
        try {
            const response = await axios.post(
                `${this.baseURL}/api/v1/chat`,
                {
                    message: message,
                    timestamp: new Date().toISOString()
                },
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.apiKey}`
                    },
                    timeout: 30000 // 30 seconds timeout
                }
            );

            return response.data;
        } catch (error) {
            console.error('Error calling AI chat service:', error.message);
            throw error;
        }
    }

    async healthCheck() {
        try {
            const response = await axios.get(`${this.baseURL}/api/v1/health`, {
                timeout: 5000
            });
            return response.data;
        } catch (error) {
            console.error('AI service health check failed:', error.message);
            return { status: 'unhealthy', error: error.message };
        }
    }
}

module.exports = new AIService();
