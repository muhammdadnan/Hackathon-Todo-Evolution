/**
 * Chat page (protected)
 *
 * AI chatbot interface for task management through natural language
 */

'use client';

import { useRequireAuth } from '@/lib/auth';
import { Button } from '@/components/ui/Button';
import { ChatWindow } from '@/components/chat/ChatWindow';
import Link from 'next/link';

export default function ChatPage() {
  const { user, isLoading } = useRequireAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  const handleSignOut = async () => {
    const { signOut } = await import('@/lib/auth');
    await signOut();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">AI Chat</h1>
              <p className="text-sm text-gray-600 mt-1">
                Manage your tasks with AI assistance
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Link href="/tasks">
                <Button variant="ghost">View Tasks</Button>
              </Link>
              <Button variant="ghost" onClick={handleSignOut}>
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="h-[calc(100vh-200px)]">
          {user && <ChatWindow userId={user.id} />}
        </div>

        {/* Info card */}
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="text-sm font-medium text-blue-800 mb-2">
            💡 Try these commands:
          </h4>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• "Create a task to buy groceries"</li>
            <li>• "Show my pending tasks"</li>
            <li>• "Mark task 1 as complete"</li>
            <li>• "What can you help me with?"</li>
          </ul>
        </div>
      </main>
    </div>
  );
}
