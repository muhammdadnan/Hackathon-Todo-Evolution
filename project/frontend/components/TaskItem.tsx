/**
 * TaskItem component
 *
 * Displays a single task with title, description, completion status.
 * Provides actions for marking complete, editing, and deleting (to be implemented in later user stories).
 */

'use client';

import { Task } from '@/lib/types';
import { Card, CardBody } from './ui/Card';

export interface TaskItemProps {
  task: Task;
  onToggleComplete?: (taskId: number) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: number) => void;
}

export function TaskItem({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
}: TaskItemProps) {
  const handleToggleComplete = () => {
    if (onToggleComplete) {
      onToggleComplete(task.id);
    }
  };

  const handleEdit = () => {
    if (onEdit) {
      onEdit(task);
    }
  };

  const handleDelete = () => {
    if (onDelete) {
      onDelete(task.id);
    }
  };

  return (
    <Card
      variant="bordered"
      className={`transition-all hover:shadow-md ${
        task.completed ? 'opacity-75' : ''
      }`}
    >
      <CardBody>
        <div className="flex items-start gap-4">
          {/* Completion checkbox */}
          <div className="flex-shrink-0 pt-1">
            <button
              onClick={handleToggleComplete}
              className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
                task.completed
                  ? 'bg-blue-600 border-blue-600'
                  : 'border-gray-300 hover:border-blue-600'
              }`}
              aria-label={
                task.completed ? 'Mark as incomplete' : 'Mark as complete'
              }
            >
              {task.completed && (
                <svg
                  className="w-3 h-3 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={3}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              )}
            </button>
          </div>

          {/* Task content */}
          <div className="flex-1 min-w-0">
            <h3
              className={`text-lg font-medium mb-1 ${
                task.completed
                  ? 'line-through text-gray-500'
                  : 'text-gray-900'
              }`}
            >
              {task.title}
            </h3>
            {task.description && (
              <p
                className={`text-sm mb-2 ${
                  task.completed ? 'text-gray-400' : 'text-gray-600'
                }`}
              >
                {task.description}
              </p>
            )}
            <div className="flex items-center gap-4 text-xs text-gray-500">
              <span>
                Created: {new Date(task.created_at).toLocaleDateString()}
              </span>
              {task.completed && (
                <span className="text-green-600 font-medium">✓ Completed</span>
              )}
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex-shrink-0 flex gap-2">
            {onEdit && (
              <button
                onClick={handleEdit}
                className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                aria-label="Edit task"
                title="Edit task"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                  />
                </svg>
              </button>
            )}
            {onDelete && (
              <button
                onClick={handleDelete}
                className="p-2 text-gray-400 hover:text-red-600 transition-colors"
                aria-label="Delete task"
                title="Delete task"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  />
                </svg>
              </button>
            )}
          </div>
        </div>
      </CardBody>
    </Card>
  );
}
