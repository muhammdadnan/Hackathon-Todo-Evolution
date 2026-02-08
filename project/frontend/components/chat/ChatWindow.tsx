/**
 * ChatWindow component
 *
 * Main chat interface container with message list and input
 */

'use client';

import { useState } from 'react';
import { ChatMessage, generateAIResponse, getGreetingMessage } from '@/lib/mockAI';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';

export interface ChatWindowProps {
  userId: string;
}

export function ChatWindow({ userId }: ChatWindowProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      role: 'assistant',
      content: getGreetingMessage(),
      timestamp: new Date(),
    },
  ]);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSendMessage = async (content: string) => {
    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsProcessing(true);

    try {
      // Generate AI response
      const aiResponse = await generateAIResponse(content, userId);

      // Add AI message
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: aiResponse,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error generating AI response:', error);

      // Add error message
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "I'm sorry, I encountered an error. Please try again.",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Chat header */}
      <div className="border-b border-gray-200 px-6 py-4 bg-gradient-to-r from-blue-50 to-indigo-50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold">
            AI
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">
              AI Task Assistant
            </h2>
            <p className="text-sm text-gray-600">
              {isProcessing ? 'Typing...' : 'Online'}
            </p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <MessageList messages={messages} />

      {/* Input */}
      <MessageInput onSendMessage={handleSendMessage} disabled={isProcessing} />
    </div>
  );
}
