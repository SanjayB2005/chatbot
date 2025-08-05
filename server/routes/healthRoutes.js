const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const aiService = require('../services/aiService');

// Health check endpoint
router.get('/', async (req, res) => {
    try {
        // Check database connection
        const dbStatus = mongoose.connection.readyState === 1 ? 'connected' : 'disconnected';
        
        // Check AI service
        const aiStatus = await aiService.healthCheck();

        const healthStatus = {
            status: 'healthy',
            timestamp: new Date().toISOString(),
            services: {
                database: {
                    status: dbStatus,
                    name: 'MongoDB'
                },
                aiService: {
                    status: aiStatus.status || 'unknown',
                    name: 'AI Service'
                }
            },
            version: '1.0.0'
        };

        // Determine overall health
        const isHealthy = dbStatus === 'connected' && 
                         (aiStatus.status === 'healthy' || !aiStatus.error);

        res.status(isHealthy ? 200 : 503).json(healthStatus);

    } catch (error) {
        console.error('Health check error:', error);
        res.status(503).json({
            status: 'unhealthy',
            timestamp: new Date().toISOString(),
            error: error.message
        });
    }
});

module.exports = router;
