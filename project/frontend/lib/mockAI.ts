/**
 * Mock AI service for chatbot
 *
 * Provides intelligent responses and task management through natural language
 */

import { Task, TaskCreate } from './types';
import { taskApi } from './api';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

/**
 * Parse user intent from message
 */
function parseIntent(message: string): {
  intent: 'create' | 'list' | 'complete' | 'delete' | 'help' | 'unknown';
  params?: any;
} {
  const lower = message.toLowerCase();

  // Create task patterns
  if (
    lower.includes('create') ||
    lower.includes('add') ||
    lower.includes('new task')
  ) {
    // Extract task title
    const patterns = [
      /create (?:a )?task (?:to |for )?(.+)/i,
      /add (?:a )?task (?:to |for )?(.+)/i,
      /new task[: ](.+)/i,
    ];

    for (const pattern of patterns) {
      const match = message.match(pattern);
      if (match) {
        return {
          intent: 'create',
          params: { title: match[1].trim() },
        };
      }
    }

    return { intent: 'create', params: { title: message } };
  }

  // List tasks patterns
  if (
    lower.includes('show') ||
    lower.includes('list') ||
    lower.includes('what are') ||
    lower.includes('my tasks')
  ) {
    const isPending = lower.includes('pending') || lower.includes('incomplete');
    const isCompleted = lower.includes('completed') || lower.includes('done');

    return {
      intent: 'list',
      params: {
        filter: isPending ? 'pending' : isCompleted ? 'completed' : 'all',
      },
    };
  }

  // Complete task patterns
  if (
    lower.includes('complete') ||
    lower.includes('finish') ||
    lower.includes('done') ||
    lower.includes('mark')
  ) {
    // Try to extract task ID or title
    const idMatch = message.match(/task (\d+)/i);
    if (idMatch) {
      return {
        intent: 'complete',
        params: { taskId: parseInt(idMatch[1]) },
      };
    }

    return { intent: 'complete', params: {} };
  }

  // Delete task patterns
  if (lower.includes('delete') || lower.includes('remove')) {
    const idMatch = message.match(/task (\d+)/i);
    if (idMatch) {
      return {
        intent: 'delete',
        params: { taskId: parseInt(idMatch[1]) },
      };
    }

    return { intent: 'delete', params: {} };
  }

  // Help patterns
  if (
    lower.includes('help') ||
    lower.includes('what can you') ||
    lower.includes('how do')
  ) {
    return { intent: 'help' };
  }

  return { intent: 'unknown' };
}

/**
 * Generate AI response based on intent
 */
export async function generateAIResponse(
  userMessage: string,
  userId: string
): Promise<string> {
  const { intent, params } = parseIntent(userMessage);

  try {
    switch (intent) {
      case 'create': {
        if (!params?.title) {
          return "I'd be happy to create a task for you! Please tell me what you'd like to do. For example: 'Create a task to buy groceries'";
        }

        const task = await taskApi.create(userId, {
          title: params.title,
        });

        return `✅ I've created a new task: "${task.title}". You can view it in your task list!`;
      }

      case 'list': {
        const tasks = await taskApi.list(userId);
        const filter = params?.filter || 'all';

        let filteredTasks = tasks;
        if (filter === 'pending') {
          filteredTasks = tasks.filter((t) => !t.completed);
        } else if (filter === 'completed') {
          filteredTasks = tasks.filter((t) => t.completed);
        }

        if (filteredTasks.length === 0) {
          return filter === 'pending'
            ? "🎉 Great news! You don't have any pending tasks."
            : filter === 'completed'
            ? "You haven't completed any tasks yet. Keep going!"
            : "You don't have any tasks yet. Create one to get started!";
        }

        const taskList = filteredTasks
          .map((t, i) => {
            const status = t.completed ? '✅' : '⭕';
            return `${i + 1}. ${status} ${t.title}`;
          })
          .join('\n');

        const header =
          filter === 'pending'
            ? `📋 You have ${filteredTasks.length} pending task${filteredTasks.length > 1 ? 's' : ''}:`
            : filter === 'completed'
            ? `✅ You've completed ${filteredTasks.length} task${filteredTasks.length > 1 ? 's' : ''}:`
            : `📋 You have ${filteredTasks.length} task${filteredTasks.length > 1 ? 's' : ''}:`;

        return `${header}\n\n${taskList}`;
      }

      case 'complete': {
        if (!params?.taskId) {
          return "Which task would you like to mark as complete? You can say 'Mark task 1 as complete' or tell me the task name.";
        }

        const task = await taskApi.toggleComplete(userId, params.taskId);

        return task.completed
          ? `✅ Awesome! I've marked "${task.title}" as complete. Keep up the great work!`
          : `⭕ I've marked "${task.title}" as incomplete.`;
      }

      case 'delete': {
        if (!params?.taskId) {
          return "Which task would you like to delete? You can say 'Delete task 1' or tell me the task name.";
        }

        await taskApi.delete(userId, params.taskId);

        return `🗑️ Task deleted successfully!`;
      }

      case 'help': {
        return `👋 Hi! I'm your AI task assistant. Here's what I can help you with:

📝 **Create tasks**: "Create a task to buy groceries"
📋 **View tasks**: "Show my pending tasks" or "What are my tasks?"
✅ **Complete tasks**: "Mark task 1 as complete"
🗑️ **Delete tasks**: "Delete task 2"

Just tell me what you need, and I'll help you manage your tasks!`;
      }

      default: {
        return `I'm not sure I understood that. I can help you create, view, complete, and delete tasks. Try saying "help" to see what I can do!`;
      }
    }
  } catch (error) {
    console.error('AI response error:', error);
    return "Sorry, I encountered an error while processing your request. Please try again.";
  }
}

/**
 * Generate greeting message
 */
export function getGreetingMessage(): string {
  const hour = new Date().getHours();
  let greeting = 'Hello';

  if (hour < 12) greeting = 'Good morning';
  else if (hour < 18) greeting = 'Good afternoon';
  else greeting = 'Good evening';

  return `${greeting}! 👋 I'm your AI task assistant. I can help you create, manage, and organize your tasks. What would you like to do today?`;
}
