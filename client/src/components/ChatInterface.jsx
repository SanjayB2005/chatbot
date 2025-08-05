import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Brain } from 'lucide-react';
import { chatAPI } from '../services/api';

const ChatInterface = ({ sessionId, onNewSession }) => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isLoadingHistory, setIsLoadingHistory] = useState(true);
    const messagesEndRef = useRef(null);

    // Load chat history when sessionId changes
    useEffect(() => {
        if (sessionId) {
            loadChatHistory();
        } else {
            setMessages([]);
            setIsLoadingHistory(false);
        }
    }, [sessionId]);

    // Auto scroll to bottom when new messages arrive
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const loadChatHistory = async () => {
        setIsLoadingHistory(true);
        try {
            const response = await chatAPI.getChatHistory(sessionId);
            if (response.success) {
                const formattedMessages = response.messages.map(msg => [
                    { type: 'user', content: msg.message, timestamp: msg.timestamp },
                    { type: 'bot', content: msg.response, timestamp: msg.timestamp }
                ]).flat();
                setMessages(formattedMessages);
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        } finally {
            setIsLoadingHistory(false);
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputMessage.trim() || isLoading) return;

        const userMessage = inputMessage.trim();
        setInputMessage('');
        setIsLoading(true);

        // Add user message immediately
        const userMsg = {
            type: 'user',
            content: userMessage,
            timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, userMsg]);

        try {
            let currentSessionId = sessionId;

            // Create session if none exists
            if (!currentSessionId) {
                const sessionResponse = await chatAPI.createSession();
                if (sessionResponse.success) {
                    currentSessionId = sessionResponse.sessionId;
                    onNewSession(currentSessionId);
                }
            }

            // Send message
            const response = await chatAPI.sendMessage(currentSessionId, userMessage);
            
            // Console log the response for debugging
            console.log('📤 Sent message:', userMessage);
            console.log('📥 Received response:', response);
            
            if (response.success) {
                const botMsg = {
                    type: 'bot',
                    content: response.response,
                    timestamp: response.timestamp
                };
                console.log('✅ Bot response:', botMsg.content);
                setMessages(prev => [...prev, botMsg]);
            } else {
                console.error('❌ Response error:', response.error);
                throw new Error(response.error || 'Failed to get response');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMsg = {
                type: 'bot',
                content: 'Sorry, I encountered an error. Please try again.',
                timestamp: new Date().toISOString(),
                isError: true
            };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setIsLoading(false);
        }
    };

    if (isLoadingHistory) {
        return (
            <div className="flex-1 flex items-center justify-center h-full">
                <div className="flex items-center space-x-2">
                    <Bot className="animate-spin" size={24} />
                    <span>Loading chat history...</span>
                </div>
            </div>
        );
    }

    return (
        <div className="flex-1 flex flex-col h-full">
            {/* Messages Container - Full Height */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {messages.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-full text-center max-w-2xl mx-auto">
                        <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-6 rounded-full mb-8">
                            <Brain size={64} className="text-white" />
                        </div>
                        <h2 className="text-4xl font-bold text-gray-900 mb-6">
                            Welcome to your AI Assistant
                        </h2>
                        <div className="bg-blue-50 border border-blue-200 rounded-xl p-8 mb-8 w-full max-w-4xl">
                            <h3 className="text-xl font-semibold text-blue-900 mb-3">
                                🧠 Powered by Your Trained Knowledge Base
                            </h3>
                            <p className="text-blue-700 text-base leading-relaxed">
                                Your AI assistant has been trained on your custom dataset stored in Google Cloud Discovery Engine. 
                                Ask any questions related to your documents and get intelligent, context-aware responses powered by Gemini 2.0 Flash.
                            </p>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
                            <div className="bg-gray-50 rounded-lg p-4">
                                <h4 className="font-medium text-gray-900 mb-2">💡 Smart Search</h4>
                                <p className="text-gray-600 text-sm">Ask questions and get answers from your trained dataset</p>
                            </div>
                            <div className="bg-gray-50 rounded-lg p-4">
                                <h4 className="font-medium text-gray-900 mb-2">🔍 Context Aware</h4>
                                <p className="text-gray-600 text-sm">Responses are based on your specific documents and data</p>
                            </div>
                            <div className="bg-gray-50 rounded-lg p-4">
                                <h4 className="font-medium text-gray-900 mb-2">💬 Natural Chat</h4>
                                <p className="text-gray-600 text-sm">Have natural conversations about your content</p>
                            </div>
                            <div className="bg-gray-50 rounded-lg p-4">
                                <h4 className="font-medium text-gray-900 mb-2">📝 Session History</h4>
                                <p className="text-gray-600 text-sm">All conversations are saved and can be resumed</p>
                            </div>
                        </div>
                        <p className="text-gray-500 mt-6">
                            Start by asking a question about your documents...
                        </p>
                    </div>
                ) : (
                    messages.map((message, index) => (
                        <div
                            key={index}
                            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`flex max-w-[80%] ${
                                    message.type === 'user' ? 'flex-row-reverse' : 'flex-row'
                                }`}
                            >
                                <div
                                    className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                                        message.type === 'user'
                                            ? 'bg-blue-500 text-white ml-3'
                                            : 'bg-gradient-to-br from-purple-500 to-blue-600 text-white mr-3'
                                    }`}
                                >
                                    {message.type === 'user' ? <User size={18} /> : <Brain size={18} />}
                                </div>
                                <div
                                    className={`rounded-2xl px-4 py-3 max-w-full ${
                                        message.type === 'user'
                                            ? 'bg-blue-500 text-white'
                                            : message.isError
                                            ? 'bg-red-100 text-red-800 border border-red-200'
                                            : 'bg-gray-100 text-gray-800 border border-gray-200'
                                    }`}
                                >
                                    <p className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</p>
                                    <p className="text-xs opacity-70 mt-2">
                                        {new Date(message.timestamp).toLocaleTimeString()}
                                    </p>
                                </div>
                            </div>
                        </div>
                    ))
                )}
                
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="flex flex-row">
                            <div className="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center bg-gradient-to-br from-purple-500 to-blue-600 text-white mr-3">
                                <Brain size={18} />
                            </div>
                            <div className="bg-gray-100 rounded-2xl px-4 py-3 border border-gray-200">
                                <div className="flex space-x-1">
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
                
                <div ref={messagesEndRef} />
            </div>

            {/* Input Form - Fixed at Bottom */}
            <div className="border-t bg-white p-4 flex-shrink-0">
                <form onSubmit={handleSendMessage} className="flex space-x-3 max-w-4xl mx-auto">
                    <input
                        type="text"
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        placeholder="Ask anything about your knowledge base..."
                        className="flex-1 border border-gray-300 rounded-full px-5 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={isLoading || !inputMessage.trim()}
                        className="bg-blue-500 text-white px-6 py-3 rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center transition-colors"
                    >
                        <Send size={18} />
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ChatInterface;
