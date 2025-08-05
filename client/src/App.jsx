import React, { useState } from 'react';
import { MessageSquare, Bot, Settings, Plus } from 'lucide-react';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  const [currentSessionId, setCurrentSessionId] = useState(null);

  const handleNewChat = (sessionId) => {
    setCurrentSessionId(sessionId);
  };

  const startNewChat = () => {
    setCurrentSessionId(null);
  };

  return (
    <div className="h-screen w-screen bg-gray-50 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Bot className="text-blue-500" size={28} />
            <div>
              <h1 className="text-xl font-bold text-gray-900">HackRx AI Assistant</h1>
              <p className="text-sm text-gray-500">Powered by your trained knowledge base</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-medium">
              ● Discovery Engine Active
            </div>
            <button
              onClick={startNewChat}
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors flex items-center space-x-2"
            >
              <Plus size={16} />
              <span>New Chat</span>
            </button>
          </div>
        </div>
      </div>

      {/* Chat Interface - Full Screen */}
      <div className="flex-1 overflow-hidden">
        <ChatInterface
          sessionId={currentSessionId}
          onNewSession={handleNewChat}
        />
      </div>
    </div>
  );
}

export default App;
