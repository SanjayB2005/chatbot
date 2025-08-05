import React, { useState, useEffect } from 'react';
import { MessageSquare, Plus, Trash2, Clock } from 'lucide-react';
import { chatAPI } from '../services/api';

const Sidebar = ({ currentSessionId, onSessionSelect, onNewChat }) => {
    const [sessions, setSessions] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        loadSessions();
    }, []);

    const loadSessions = async () => {
        setIsLoading(true);
        try {
            const response = await chatAPI.getSessions();
            if (response.success) {
                setSessions(response.sessions);
            }
        } catch (error) {
            console.error('Error loading sessions:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleNewChat = async () => {
        try {
            const response = await chatAPI.createSession();
            if (response.success) {
                await loadSessions(); // Reload sessions
                onNewChat(response.sessionId);
            }
        } catch (error) {
            console.error('Error creating new chat:', error);
        }
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 1) return 'Today';
        if (diffDays === 2) return 'Yesterday';
        if (diffDays <= 7) return `${diffDays - 1} days ago`;
        return date.toLocaleDateString();
    };

    return (
        <div className="w-64 bg-gray-50 border-r border-gray-200 flex flex-col h-full">
            {/* Header */}
            <div className="p-4 border-b border-gray-200">
                <button
                    onClick={handleNewChat}
                    className="w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 flex items-center justify-center space-x-2 transition-colors"
                >
                    <Plus size={16} />
                    <span>New Chat</span>
                </button>
            </div>

            {/* Sessions List */}
            <div className="flex-1 overflow-y-auto">
                {isLoading ? (
                    <div className="p-4 text-center text-gray-500">
                        Loading sessions...
                    </div>
                ) : sessions.length === 0 ? (
                    <div className="p-4 text-center text-gray-500">
                        No chat sessions yet
                    </div>
                ) : (
                    <div className="space-y-1 p-2">
                        {sessions.map((session) => (
                            <div
                                key={session.sessionId}
                                onClick={() => onSessionSelect(session.sessionId)}
                                className={`p-3 rounded-lg cursor-pointer transition-colors group ${
                                    currentSessionId === session.sessionId
                                        ? 'bg-blue-100 border border-blue-200'
                                        : 'hover:bg-gray-100'
                                }`}
                            >
                                <div className="flex items-start justify-between">
                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center space-x-2 mb-1">
                                            <MessageSquare size={14} className="text-gray-400 flex-shrink-0" />
                                            <h3 className="text-sm font-medium text-gray-900 truncate">
                                                {session.title}
                                            </h3>
                                        </div>
                                        <div className="flex items-center space-x-4 text-xs text-gray-500">
                                            <div className="flex items-center space-x-1">
                                                <Clock size={12} />
                                                <span>{formatDate(session.lastActivity)}</span>
                                            </div>
                                            <span>{session.messageCount} messages</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-gray-200">
                <div className="text-xs text-gray-500 text-center">
                    <p>HackRx ChatBot v1.0</p>
                    <p>Powered by Gemini 2.0 Flash</p>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
