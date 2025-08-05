const express = require('express');
const router = express.Router();
const { v4: uuidv4 } = require('uuid');
const ChatMessage = require('../models/ChatMessage');
const ChatSession = require('../models/ChatSession');
const aiService = require('../services/aiService');

// Create a new chat session
router.post('/session', async (req, res) => {
    try {
        const sessionId = uuidv4();
        const session = new ChatSession({
            sessionId,
            title: req.body.title || 'New Chat'
        });

        await session.save();

        res.status(201).json({
            success: true,
            sessionId: sessionId,
            message: 'Chat session created successfully'
        });
    } catch (error) {
        console.error('Error creating chat session:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to create chat session'
        });
    }
});

// Send a message in a chat session
router.post('/message', async (req, res) => {
    try {
        const { sessionId, message } = req.body;

        if (!sessionId || !message) {
            return res.status(400).json({
                success: false,
                error: 'SessionId and message are required'
            });
        }

        // Find or create session
        let session = await ChatSession.findOne({ sessionId });
        if (!session) {
            session = new ChatSession({ sessionId });
            await session.save();
        }

        // Get AI response
        console.log('🤖 Calling AI Service with message:', message);
        const aiResponse = await aiService.chatResponse(message);
        console.log('🧠 AI Service Response:', aiResponse);

        // Save message to database
        const chatMessage = new ChatMessage({
            sessionId,
            message,
            response: aiResponse.response || aiResponse,
            metadata: {
                timestamp: new Date().toISOString()
            }
        });

        await chatMessage.save();
        console.log('💾 Message saved to database:', { sessionId, message: message.substring(0, 50) + '...' });

        // Update session
        session.messageCount += 1;
        session.lastActivity = new Date();
        await session.save();

        const responseData = {
            success: true,
            response: aiResponse.response || aiResponse,
            sessionId: sessionId,
            timestamp: chatMessage.timestamp
        };
        
        console.log('✅ Sending response to client:', responseData);
        res.json(responseData);

    } catch (error) {
        console.error('Error processing message:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to process message',
            details: error.message
        });
    }
});

// Get chat history for a session
router.get('/history/:sessionId', async (req, res) => {
    try {
        const { sessionId } = req.params;
        const { limit = 50, offset = 0 } = req.query;

        const messages = await ChatMessage.find({ sessionId })
            .sort({ createdAt: -1 })
            .limit(parseInt(limit))
            .skip(parseInt(offset))
            .select('message response timestamp createdAt');

        const session = await ChatSession.findOne({ sessionId });

        res.json({
            success: true,
            session: session || { sessionId, title: 'Unknown Session' },
            messages: messages.reverse(), // Reverse to show oldest first
            total: await ChatMessage.countDocuments({ sessionId })
        });

    } catch (error) {
        console.error('Error fetching chat history:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to fetch chat history'
        });
    }
});

// Get all chat sessions
router.get('/sessions', async (req, res) => {
    try {
        const sessions = await ChatSession.find({ isActive: true })
            .sort({ lastActivity: -1 })
            .limit(50);

        res.json({
            success: true,
            sessions: sessions
        });

    } catch (error) {
        console.error('Error fetching sessions:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to fetch sessions'
        });
    }
});

// Process questions based on document (HackRx specific endpoint)
router.post('/hackrx/run', async (req, res) => {
    try {
        const { documents, questions } = req.body;

        if (!documents || !questions || !Array.isArray(questions)) {
            return res.status(400).json({
                success: false,
                error: 'Documents URL and questions array are required'
            });
        }

        // Call AI service
        const result = await aiService.processQuestions(documents, questions);

        res.json({
            success: true,
            answers: result.answers || result
        });

    } catch (error) {
        console.error('Error processing questions:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to process questions',
            details: error.message
        });
    }
});

module.exports = router;
