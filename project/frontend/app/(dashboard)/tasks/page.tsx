/**
 * Tasks page (protected)
 *
 * Displays user's task list with filtering and management capabilities.
 * Requires authentication.
 */

'use client';

import { useState } from 'react';
import { useRequireAuth } from '@/lib/auth';
import { Button } from '@/components/ui/Button';
import { Card, CardBody, CardHeader } from '@/components/ui/Card';
import { Modal } from '@/components/ui/Modal';
import { TaskList } from '@/components/TaskList';
import { TaskForm } from '@/components/TaskForm';
import { Task } from '@/lib/types';
import { taskApi, ApiClientError } from '@/lib/api';
import Link from 'next/link';

export default function TasksPage() {
  const { user, isLoading } = useRequireAuth();
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deletingTaskId, setDeletingTaskId] = useState<number | null>(null);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

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

  const handleAddTask = () => {
    setIsAddModalOpen(true);
  };

  const handleTaskCreated = () => {
    setIsAddModalOpen(false);
    // Trigger task list refresh by changing key
    setRefreshKey((prev) => prev + 1);
  };

  const handleTaskUpdated = () => {
    setIsEditModalOpen(false);
    setEditingTask(null);
    // Trigger task list refresh by changing key
    setRefreshKey((prev) => prev + 1);
  };

  // Note: TaskList handles toggle completion internally with optimistic updates
  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setIsEditModalOpen(true);
  };

  const handleDelete = (taskId: number) => {
    setDeletingTaskId(taskId);
    setDeleteError(null);
    setIsDeleteModalOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (!user || !deletingTaskId) return;

    setIsDeleting(true);
    setDeleteError(null);

    try {
      await taskApi.delete(user.id, deletingTaskId);

      // Close modal and refresh list
      setIsDeleteModalOpen(false);
      setDeletingTaskId(null);
      setRefreshKey((prev) => prev + 1);
    } catch (error) {
      if (error instanceof ApiClientError) {
        setDeleteError(error.detail || error.message);
      } else {
        setDeleteError('Failed to delete task. Please try again.');
      }
    } finally {
      setIsDeleting(false);
    }
  };

  const handleCancelDelete = () => {
    setIsDeleteModalOpen(false);
    setDeletingTaskId(null);
    setDeleteError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
              <p className="text-sm text-gray-600 mt-1">
                Welcome back, {user?.name || user?.email}!
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Link href="/chat">
                <Button variant="ghost">AI Chat</Button>
              </Link>
              <Button variant="primary" onClick={handleAddTask}>
                Add Task
              </Button>
              <Button variant="ghost" onClick={handleSignOut}>
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card variant="elevated">
          <CardHeader>
            <h2 className="text-xl font-semibold text-gray-900">Task List</h2>
          </CardHeader>
          <CardBody>
            {user && (
              <TaskList
                key={refreshKey}
                userId={user.id}
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            )}
          </CardBody>
        </Card>

        {/* Development info */}
        <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-4">
          <h4 className="text-sm font-medium text-green-800 mb-2">
            User Story 6: Delete Task - Complete ✓
          </h4>
          <ul className="text-sm text-green-700 space-y-1">
            <li>✓ User Story 1: Authentication</li>
            <li>✓ User Story 2: View Task List</li>
            <li>✓ User Story 3: Add Task</li>
            <li>✓ User Story 4: Mark Complete</li>
            <li>✓ User Story 5: Update Task</li>
            <li>✓ User Story 6: Delete Task</li>
          </ul>
          <p className="text-sm text-green-700 mt-2 font-medium">
            All 6 User Stories Complete! Full CRUD functionality implemented.
          </p>
        </div>
      </main>

      {/* Add Task Modal */}
      <Modal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        title="Add New Task"
        size="md"
      >
        {user && (
          <TaskForm
            userId={user.id}
            mode="create"
            onSuccess={handleTaskCreated}
            onCancel={() => setIsAddModalOpen(false)}
          />
        )}
      </Modal>

      {/* Edit Task Modal */}
      <Modal
        isOpen={isEditModalOpen}
        onClose={() => {
          setIsEditModalOpen(false);
          setEditingTask(null);
        }}
        title="Edit Task"
        size="md"
      >
        {user && editingTask && (
          <TaskForm
            userId={user.id}
            mode="edit"
            taskId={editingTask.id}
            initialData={{
              title: editingTask.title,
              description: editingTask.description || undefined,
            }}
            onSuccess={handleTaskUpdated}
            onCancel={() => {
              setIsEditModalOpen(false);
              setEditingTask(null);
            }}
          />
        )}
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={isDeleteModalOpen}
        onClose={handleCancelDelete}
        title="Delete Task"
        size="sm"
      >
        <div className="space-y-4">
          {/* Warning message */}
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 text-red-600">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>
            <div>
              <p className="text-sm text-gray-900 font-medium">
                Are you sure you want to delete this task?
              </p>
              <p className="text-sm text-gray-600 mt-1">
                This action cannot be undone.
              </p>
            </div>
          </div>

          {/* Error message */}
          {deleteError && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-600">{deleteError}</p>
            </div>
          )}

          {/* Action buttons */}
          <div className="flex justify-end gap-3 pt-2">
            <Button
              type="button"
              variant="ghost"
              onClick={handleCancelDelete}
              disabled={isDeleting}
            >
              Cancel
            </Button>
            <Button
              type="button"
              variant="danger"
              onClick={handleConfirmDelete}
              isLoading={isDeleting}
            >
              Delete Task
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
