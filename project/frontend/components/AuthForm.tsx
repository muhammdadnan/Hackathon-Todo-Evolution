/**
 * AuthForm component
 *
 * Reusable authentication form for signin and signup.
 * Handles form validation, submission, and error display.
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from './ui/Button';
import { Input } from './ui/Input';
import { ApiClientError, handleApiCall } from '@/lib/api';
import { mockAuthApi } from '@/lib/mockData';

export interface AuthFormProps {
  mode: 'signin' | 'signup';
  onSuccess?: () => void;
}

interface FormData {
  email: string;
  password: string;
  name?: string;
}

interface FormErrors {
  email?: string;
  password?: string;
  name?: string;
  general?: string;
}

export function AuthForm({ mode, onSuccess }: AuthFormProps) {
  const router = useRouter();
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
    name: '',
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);

  const isSignup = mode === 'signup';

  // Validate form data
  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (isSignup && formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    // Name validation (signup only)
    if (isSignup && !formData.name) {
      newErrors.name = 'Name is required';
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
      const useMockData = process.env.NEXT_PUBLIC_USE_MOCK_DATA === 'true';
      let data;

      if (useMockData) {
        // Use mock data
        if (isSignup) {
          data = await mockAuthApi.signup(formData.email, formData.password);
        } else {
          data = await mockAuthApi.signin(formData.email, formData.password);
        }
      } else {
        // Use real API
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const endpoint = isSignup ? '/api/auth/signup' : '/api/auth/signin';

        const payload = isSignup
          ? {
              email: formData.email,
              password: formData.password,
              name: formData.name,
            }
          : {
              email: formData.email,
              password: formData.password,
            };

        const response = await fetch(`${apiUrl}${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include', // Include cookies for Better Auth
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new ApiClientError(
            errorData.detail || 'Authentication failed',
            response.status,
            errorData.detail
          );
        }

        data = await response.json();
      }

      // Store token in localStorage (temporary - Better Auth will handle this)
      if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));
      }

      // Call success callback
      if (onSuccess) {
        onSuccess();
      }

      // Redirect to tasks page
      router.push('/tasks');
    } catch (error) {
      if (error instanceof ApiClientError) {
        setErrors({
          general: error.detail || error.message,
        });
      } else if (error instanceof Error) {
        setErrors({
          general: error.message,
        });
      } else {
        setErrors({
          general: 'An unexpected error occurred. Please try again.',
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Handle input changes
  const handleChange = (field: keyof FormData) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [field]: e.target.value,
    }));
    // Clear error for this field
    if (errors[field]) {
      setErrors((prev) => ({
        ...prev,
        [field]: undefined,
      }));
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

      {/* Name field (signup only) */}
      {isSignup && (
        <Input
          label="Name"
          type="text"
          id="name"
          value={formData.name}
          onChange={handleChange('name')}
          error={errors.name}
          placeholder="John Doe"
          disabled={isLoading}
          required
        />
      )}

      {/* Email field */}
      <Input
        label="Email"
        type="email"
        id="email"
        value={formData.email}
        onChange={handleChange('email')}
        error={errors.email}
        placeholder="you@example.com"
        disabled={isLoading}
        required
      />

      {/* Password field */}
      <Input
        label="Password"
        type="password"
        id="password"
        value={formData.password}
        onChange={handleChange('password')}
        error={errors.password}
        placeholder={isSignup ? 'At least 8 characters' : 'Your password'}
        disabled={isLoading}
        required
      />

      {/* Submit button */}
      <Button
        type="submit"
        variant="primary"
        size="lg"
        isLoading={isLoading}
        className="w-full"
      >
        {isSignup ? 'Sign Up' : 'Sign In'}
      </Button>

      {/* Helper text */}
      <p className="text-sm text-gray-600 text-center">
        {isSignup ? (
          <>
            Already have an account?{' '}
            <a href="/signin" className="text-blue-600 hover:underline">
              Sign in
            </a>
          </>
        ) : (
          <>
            Don't have an account?{' '}
            <a href="/signup" className="text-blue-600 hover:underline">
              Sign up
            </a>
          </>
        )}
      </p>
    </form>
  );
}
