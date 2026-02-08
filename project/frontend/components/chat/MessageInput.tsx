/**
 * MessageInput component
 *
 * Input field for sending chat messages
 */

'use client';

import { useState, KeyboardEvent } from 'react';
import { Button } from '../ui/Button';

export interface MessageInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export function MessageInput({ onSendMessage, disabled }: MessageInputProps) {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      <div className="flex gap-2">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message... (Press Enter to send)"
          disabled={disabled}
          rows={1}
          className="flex-1 resize-none rounded-lg border border-gray-300 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
        />
        <Button
          onClick={handleSend}
          disabled={!message.trim() || disabled}
          variant="primary"
          className="px-6"
        >
          Send
        </Button>
      </div>
      <p className="text-xs text-gray-500 mt-2">
        Try: "Create a task to buy groceries" or "Show my tasks"
      </p>
    </div>
  );
}
