import { apiClient } from './client';
import type { Problem, User } from '@/types/models';

export const usersApi = {
  async createUser(data: {
    username: string;
    email: string;
    first_name?: string;
    last_name?: string;
  }): Promise<User> {
    return apiClient('/users', {
      method: 'POST',
      body: JSON.stringify({
        ...data,
        password: 'temporary-password',
      }),
    });
  },

  async login(data: { username: string; email: string }): Promise<User> {
    return apiClient('/users/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async getUser(userId: number): Promise<User> {
    return apiClient(`/users/${userId}`);
  },

  async updateUser(
    userId: number,
    data: {
      username?: string;
      email?: string;
      first_name?: string;
      last_name?: string;
    }
  ): Promise<User> {
    return apiClient(`/users/${userId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  },

  async getUserProblems(userId: number): Promise<Problem[]> {
    return apiClient(`/users/${userId}/problems`);
  },
};
