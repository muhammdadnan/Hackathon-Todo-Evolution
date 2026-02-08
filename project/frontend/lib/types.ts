/**
 * TypeScript type definitions for the Todo application.
 *
 * Defines interfaces for User, Task, and API responses.
 */

/**
 * User interface
 */
export interface User {
  id: string;
  email: string;
  name?: string;
  created_at: string;
  updated_at: string;
}

/**
 * Task interface
 */
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Task creation payload
 */
export interface TaskCreate {
  title: string;
  description?: string;
}

/**
 * Task update payload
 */
export interface TaskUpdate {
  title: string;
  description?: string;
}

/**
 * Authentication credentials
 */
export interface AuthCredentials {
  email: string;
  password: string;
}

/**
 * Authentication response
 */
export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

/**
 * API error response
 */
export interface ApiError {
  detail: string;
  status_code?: number;
}

/**
 * Generic API response wrapper
 */
export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
}
