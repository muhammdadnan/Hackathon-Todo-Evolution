/**
 * Authentication utilities and state management.
 *
 * Provides authentication state management, token handling, and user session.
 * This is a temporary implementation until Better Auth is fully integrated.
 */

'use client';

import { useEffect, useState } from 'react';
import type { User } from './types';

/**
 * Auth state interface
 */
export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

/**
 * Get JWT token from localStorage
 */
export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
}

/**
 * Get current user from localStorage
 */
export function getCurrentUser(): User | null {
  if (typeof window === 'undefined') return null;

  const userStr = localStorage.getItem('user');
  if (!userStr) return null;

  try {
    return JSON.parse(userStr) as User;
  } catch {
    return null;
  }
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
  return getToken() !== null && getCurrentUser() !== null;
}

/**
 * Sign out user
 */
export async function signOut(): Promise<void> {
  if (typeof window === 'undefined') return;

  // Clear local storage
  localStorage.removeItem('access_token');
  localStorage.removeItem('user');

  // Redirect to home page
  window.location.href = '/';
}

/**
 * React hook for authentication state
 *
 * @returns AuthState with user, isAuthenticated, and isLoading
 *
 * @example
 * function MyComponent() {
 *   const { user, isAuthenticated, isLoading } = useAuth();
 *
 *   if (isLoading) return <div>Loading...</div>;
 *   if (!isAuthenticated) return <div>Please sign in</div>;
 *
 *   return <div>Welcome, {user.name}!</div>;
 * }
 */
export function useAuth(): AuthState {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
  });

  useEffect(() => {
    // Check authentication status on mount
    const user = getCurrentUser();
    const token = getToken();

    setState({
      user,
      isAuthenticated: user !== null && token !== null,
      isLoading: false,
    });
  }, []);

  return state;
}

/**
 * React hook to require authentication
 * Redirects to signin page if not authenticated
 *
 * @example
 * function ProtectedPage() {
 *   const { user, isLoading } = useRequireAuth();
 *
 *   if (isLoading) return <div>Loading...</div>;
 *
 *   return <div>Protected content for {user.name}</div>;
 * }
 */
export function useRequireAuth(): AuthState {
  const auth = useAuth();

  useEffect(() => {
    if (!auth.isLoading && !auth.isAuthenticated) {
      // Redirect to signin page
      window.location.href = '/signin';
    }
  }, [auth.isLoading, auth.isAuthenticated]);

  return auth;
}

/**
 * Auth utilities export
 */
export const auth = {
  getCurrentUser,
  signOut,
  isAuthenticated,
  getToken,
  useAuth,
  useRequireAuth,
};

/**
 * TODO: Migrate to Better Auth
 *
 * Once Better Auth is installed and configured:
 * 1. Replace localStorage with Better Auth session management
 * 2. Use Better Auth's useSession hook instead of useAuth
 * 3. Use Better Auth's signOut function
 * 4. Configure JWT plugin with shared secret
 * 5. Set up Better Auth provider in root layout
 */
