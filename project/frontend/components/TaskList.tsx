/**
 * TaskList component
 *
 * Displays a list of tasks with filtering options.
 * Fetches tasks from the API and handles loading/error states.
 */

'use client';

import { useEffect, useState } from 'react';
import { Task } from '@/lib/types';
import { taskApi, ApiClientError } from '@/lib/api';
import { TaskItem } from './TaskItem';
import { Button } from './ui/Button';

export interface TaskListProps {
  userId: string;
  onToggleComplete?: (taskId: number) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: number) => void;
}

type FilterType = 'all' | 'pending' | 'completed';

export function TaskList({
  userId,
  onToggleComplete,
  onEdit,
  onDelete,
}: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<FilterType>('all');

  // Fetch tasks from API
  const fetchTasks = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const allTasks = await taskApi.list(userId);
      setTasks(allTasks);
    } catch (err) {
      if (err instanceof ApiClientError) {
        setError(err.detail || err.message);
      } else {
        setError('Failed to load tasks. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Handle toggle completion with optimistic UI update
  const handleToggleComplete = async (taskId: number) => {
    // Find the task
    const task = tasks.find((t) => t.id === taskId);
    if (!task) return;

    // Optimistic update: update UI immediately
    const previousTasks = [...tasks];
    setTasks((prevTasks) =>
      prevTasks.map((t) =>
        t.id === taskId ? { ...t, completed: !t.completed } : t
      )
    );

    try {
      // Call API to toggle completion
      const updatedTask = await taskApi.toggleComplete(userId, taskId);

      // Update with server response
      setTasks((prevTasks) =>
        prevTasks.map((t) => (t.id === taskId ? updatedTask : t))
      );

      // Call parent handler if provided
      if (onToggleComplete) {
        onToggleComplete(taskId);
      }
    } catch (err) {
      // Rollback on error
      setTasks(previousTasks);

      if (err instanceof ApiClientError) {
        setError(err.detail || err.message);
      } else {
        setError('Failed to update task. Please try again.');
      }
    }
  };

  // Fetch tasks on mount
  useEffect(() => {
    fetchTasks();
  }, [userId]);

  // Filter tasks based on selected filter
  const filteredTasks = tasks.filter((task) => {
    if (filter === 'pending') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true; // 'all'
  });

  // Loading state
  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading tasks...</p>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 text-5xl mb-4">⚠️</div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          Failed to Load Tasks
        </h3>
        <p className="text-gray-600 mb-4">{error}</p>
        <Button onClick={fetchTasks} variant="primary">
          Try Again
        </Button>
      </div>
    );
  }

  // Empty state
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📝</div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          No tasks yet
        </h3>
        <p className="text-gray-600 mb-6">
          Create your first task to get started!
        </p>
        <Button variant="primary">Add Task</Button>
      </div>
    );
  }

  return (
    <div>
      {/* Filter buttons */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All ({tasks.length})
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === 'pending'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Pending ({tasks.filter((t) => !t.completed).length})
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === 'completed'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Completed ({tasks.filter((t) => t.completed).length})
          </button>
        </div>

        {/* Refresh button */}
        <Button variant="ghost" onClick={fetchTasks} size="sm">
          <svg
            className="w-4 h-4 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            />
          </svg>
          Refresh
        </Button>
      </div>

      {/* Task list */}
      {filteredTasks.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-600">
            No {filter === 'all' ? '' : filter} tasks found.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredTasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggleComplete={handleToggleComplete}
              onEdit={onEdit}
              onDelete={onDelete}
            />
          ))}
        </div>
      )}

      {/* Task count summary */}
      <div className="mt-6 text-center text-sm text-gray-500">
        Showing {filteredTasks.length} of {tasks.length} tasks
      </div>
    </div>
  );
}
