/**
 * TaskForm component
 *
 * Form for creating and editing tasks.
 * Handles validation, submission, and error display.
 */

'use client';

import { useState } from 'react';
import { TaskCreate } from '@/lib/types';
import { taskApi, ApiClientError } from '@/lib/api';
import { Button } from './ui/Button';
import { Input, Textarea } from './ui/Input';

export interface TaskFormProps {
  userId: string;
  mode?: 'create' | 'edit';
  taskId?: number;
  initialData?: {
    title: string;
    description?: string;
  };
  onSuccess?: () => void;
  onCancel?: () => void;
}

interface FormErrors {
  title?: string;
  description?: string;
  general?: string;
}

export function TaskForm({
  userId,
  mode = 'create',
  taskId,
  initialData,
  onSuccess,
  onCancel,
}: TaskFormProps) {
  const [formData, setFormData] = useState<TaskCreate>({
    title: initialData?.title || '',
    description: initialData?.description || '',
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);

  // Validate form data
  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Title validation
    if (!formData.title || formData.title.trim().length === 0) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length > 200) {
      newErrors.title = 'Title must be 200 characters or less';
    }

    // Description validation
    if (formData.description && formData.description.length > 1000) {
      newErrors.description = 'Description must be 1000 characters or less';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Clear previous errors
    setErrors({});

    // Validate form
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      if (mode === 'create') {
        await taskApi.create(userId, {
          title: formData.title.trim(),
          description: formData.description?.trim() || undefined,
        });
      } else {
        // Edit mode - update existing task
        if (!taskId) {
          throw new Error('Task ID is required for edit mode');
        }
        await taskApi.update(userId, taskId, {
          title: formData.title.trim(),
          description: formData.description?.trim() || undefined,
        });
      }

      // Call success callback
      if (onSuccess) {
        onSuccess();
      }

      // Reset form only in create mode
      if (mode === 'create') {
        setFormData({ title: '', description: '' });
      }
    } catch (error) {
      if (error instanceof ApiClientError) {
        setErrors({
          general: error.detail || error.message,
        });
      } else {
        setErrors({
          general: mode === 'create'
            ? 'Failed to create task. Please try again.'
            : 'Failed to update task. Please try again.',
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Handle input changes
  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, title: e.target.value }));
    if (errors.title) {
      setErrors((prev) => ({ ...prev, title: undefined }));
    }
  };

  const handleDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setFormData((prev) => ({ ...prev, description: e.target.value }));
    if (errors.description) {
      setErrors((prev) => ({ ...prev, description: undefined }));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* General error message */}
      {errors.general && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{errors.general}</p>
        </div>
      )}

      {/* Title field */}
      <Input
        label="Title"
        type="text"
        id="task-title"
        value={formData.title}
        onChange={handleTitleChange}
        error={errors.title}
        placeholder="Enter task title"
        disabled={isLoading}
        required
        helperText={`${formData.title.length}/200 characters`}
      />

      {/* Description field */}
      <Textarea
        label="Description (optional)"
        id="task-description"
        value={formData.description || ''}
        onChange={handleDescriptionChange}
        error={errors.description}
        placeholder="Enter task description"
        disabled={isLoading}
        rows={4}
        helperText={`${formData.description?.length || 0}/1000 characters`}
      />

      {/* Action buttons */}
      <div className="flex justify-end gap-3 pt-2">
        {onCancel && (
          <Button
            type="button"
            variant="ghost"
            onClick={onCancel}
            disabled={isLoading}
          >
            Cancel
          </Button>
        )}
        <Button
          type="submit"
          variant="primary"
          isLoading={isLoading}
        >
          {mode === 'create' ? 'Create Task' : 'Save Changes'}
        </Button>
      </div>
    </form>
  );
}
