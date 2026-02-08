/**
 * API client for backend communication.
 *
 * Provides type-safe methods for interacting with the FastAPI backend.
 * Automatically includes JWT tokens in requests and handles errors.
 * Supports mock data mode for frontend-only deployment.
 */

import type {
  ApiError,
  ApiResponse,
  Task,
  TaskCreate,
  TaskUpdate,
} from './types';
import { mockTaskApi } from './mockData';

/**
 * API client configuration
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const USE_MOCK_DATA = process.env.NEXT_PUBLIC_USE_MOCK_DATA === 'true';

/**
 * Custom error class for API errors
 */
export class ApiClientError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public detail?: string
  ) {
    super(message);
    this.name = 'ApiClientError';
  }
}

/**
 * Get JWT token from storage
 * Currently using localStorage until Better Auth is fully integrated
 */
function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
}

/**
 * Make an authenticated API request
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  // Get auth token if available
  const token = getAuthToken();

  // Prepare headers
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Add Authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Make request with credentials to include cookies
  const response = await fetch(url, {
    ...options,
    headers,
    credentials: 'include', // Include cookies for Better Auth
  });

  // Handle non-OK responses
  if (!response.ok) {
    let errorDetail = 'An error occurred';
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch {
      // If response is not JSON, use status text
      errorDetail = response.statusText;
    }

    throw new ApiClientError(
      `API request failed: ${errorDetail}`,
      response.status,
      errorDetail
    );
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  // Parse JSON response
  try {
    return await response.json();
  } catch (error) {
    throw new ApiClientError('Failed to parse response JSON');
  }
}

/**
 * Task API methods
 */
export const taskApi = {
  /**
   * List all tasks for a user
   */
  async list(userId: string): Promise<Task[]> {
    if (USE_MOCK_DATA) {
      return mockTaskApi.list(userId);
    }
    return apiRequest<Task[]>(`/api/${userId}/tasks`, {
      method: 'GET',
    });
  },

  /**
   * Get a specific task
   */
  async get(userId: string, taskId: number): Promise<Task> {
    if (USE_MOCK_DATA) {
      return mockTaskApi.get(userId, taskId);
    }
    return apiRequest<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: 'GET',
    });
  },

  /**
   * Create a new task
   */
  async create(userId: string, data: TaskCreate): Promise<Task> {
    if (USE_MOCK_DATA) {
      return mockTaskApi.create(userId, data);
    }
    return apiRequest<Task>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  /**
   * Update an existing task
   */
  async update(
    userId: string,
    taskId: number,
    data: TaskUpdate
  ): Promise<Task> {
    if (USE_MOCK_DATA) {
      return mockTaskApi.update(userId, taskId, data);
    }
    return apiRequest<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  /**
   * Toggle task completion status
   */
  async toggleComplete(userId: string, taskId: number): Promise<Task> {
    if (USE_MOCK_DATA) {
      return mockTaskApi.toggleComplete(userId, taskId);
    }
    return apiRequest<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });
  },

  /**
   * Delete a task
   */
  async delete(userId: string, taskId: number): Promise<void> {
    if (USE_MOCK_DATA) {
      return mockTaskApi.delete(userId, taskId);
    }
    return apiRequest<void>(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  },
};

/**
 * Health check
 */
export async function healthCheck(): Promise<{ status: string }> {
  return apiRequest<{ status: string }>('/health', {
    method: 'GET',
  });
}

/**
 * Wrapper for handling API errors in components
 */
export async function handleApiCall<T>(
  apiCall: () => Promise<T>
): Promise<ApiResponse<T>> {
  try {
    const data = await apiCall();
    return { data };
  } catch (error) {
    if (error instanceof ApiClientError) {
      return {
        error: {
          detail: error.detail || error.message,
          status_code: error.statusCode,
        },
      };
    }
    return {
      error: {
        detail: error instanceof Error ? error.message : 'Unknown error',
      },
    };
  }
}

/**
 * Export default API object
 */
export const api = {
  tasks: taskApi,
  health: healthCheck,
};
