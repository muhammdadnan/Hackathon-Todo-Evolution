/**
 * Mock data for frontend-only deployment
 *
 * Provides fake data and simulated API responses for demo purposes.
 * Used when NEXT_PUBLIC_USE_MOCK_DATA=true
 */

import type { Task, User, AuthResponse } from './types';

/**
 * Mock users database
 */
const mockUsers: Map<string, { user: User; password: string }> = new Map([
  [
    'demo@example.com',
    {
      user: {
        id: 'user-1',
        email: 'demo@example.com',
        name: 'Demo User',
        created_at: '2026-02-01T00:00:00Z',
        updated_at: '2026-02-01T00:00:00Z',
      },
      password: 'demo123',
    },
  ],
]);

/**
 * Mock tasks database
 */
let mockTasks: Task[] = [
  {
    id: 1,
    user_id: 'user-1',
    title: 'Welcome to Todo Evolution!',
    description: 'This is a demo task. Try creating, editing, and completing tasks.',
    completed: false,
    created_at: '2026-02-08T10:00:00Z',
    updated_at: '2026-02-08T10:00:00Z',
  },
  {
    id: 2,
    user_id: 'user-1',
    title: 'Complete Phase 2 deployment',
    description: 'Deploy the Next.js frontend to Vercel with mock data',
    completed: true,
    created_at: '2026-02-08T09:00:00Z',
    updated_at: '2026-02-08T11:00:00Z',
  },
  {
    id: 3,
    user_id: 'user-1',
    title: 'Test task management features',
    description: 'Try adding, editing, completing, and deleting tasks',
    completed: false,
    created_at: '2026-02-08T08:00:00Z',
    updated_at: '2026-02-08T08:00:00Z',
  },
];

let nextTaskId = 4;

/**
 * Simulate network delay
 */
const delay = (ms: number = 300) =>
  new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Mock Authentication API
 */
export const mockAuthApi = {
  async signup(email: string, password: string): Promise<AuthResponse> {
    await delay();

    // Check if user already exists
    if (mockUsers.has(email)) {
      throw new Error('User already exists');
    }

    // Create new user
    const user: User = {
      id: `user-${Date.now()}`,
      email,
      name: email.split('@')[0],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    mockUsers.set(email, { user, password });

    return {
      access_token: `mock-token-${user.id}`,
      token_type: 'bearer',
      user,
    };
  },

  async signin(email: string, password: string): Promise<AuthResponse> {
    await delay();

    const userData = mockUsers.get(email);

    if (!userData || userData.password !== password) {
      throw new Error('Invalid email or password');
    }

    return {
      access_token: `mock-token-${userData.user.id}`,
      token_type: 'bearer',
      user: userData.user,
    };
  },
};

/**
 * Mock Task API
 */
export const mockTaskApi = {
  async list(userId: string): Promise<Task[]> {
    await delay();
    return mockTasks.filter((task) => task.user_id === userId);
  },

  async get(userId: string, taskId: number): Promise<Task> {
    await delay();
    const task = mockTasks.find((t) => t.id === taskId && t.user_id === userId);
    if (!task) {
      throw new Error('Task not found');
    }
    return task;
  },

  async create(
    userId: string,
    data: { title: string; description?: string }
  ): Promise<Task> {
    await delay();

    const newTask: Task = {
      id: nextTaskId++,
      user_id: userId,
      title: data.title,
      description: data.description,
      completed: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    mockTasks.push(newTask);
    return newTask;
  },

  async update(
    userId: string,
    taskId: number,
    data: { title: string; description?: string }
  ): Promise<Task> {
    await delay();

    const taskIndex = mockTasks.findIndex(
      (t) => t.id === taskId && t.user_id === userId
    );

    if (taskIndex === -1) {
      throw new Error('Task not found');
    }

    mockTasks[taskIndex] = {
      ...mockTasks[taskIndex],
      title: data.title,
      description: data.description,
      updated_at: new Date().toISOString(),
    };

    return mockTasks[taskIndex];
  },

  async toggleComplete(userId: string, taskId: number): Promise<Task> {
    await delay();

    const taskIndex = mockTasks.findIndex(
      (t) => t.id === taskId && t.user_id === userId
    );

    if (taskIndex === -1) {
      throw new Error('Task not found');
    }

    mockTasks[taskIndex] = {
      ...mockTasks[taskIndex],
      completed: !mockTasks[taskIndex].completed,
      updated_at: new Date().toISOString(),
    };

    return mockTasks[taskIndex];
  },

  async delete(userId: string, taskId: number): Promise<void> {
    await delay();

    const taskIndex = mockTasks.findIndex(
      (t) => t.id === taskId && t.user_id === userId
    );

    if (taskIndex === -1) {
      throw new Error('Task not found');
    }

    mockTasks.splice(taskIndex, 1);
  },
};
