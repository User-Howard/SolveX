import { apiClient } from './client';
import type { User } from '@/types/models';

export const usersApi = {
  async createUser(data: {
    username: string;
    email: string;
    password: string;
    first_name?: string;
    last_name?: string;
  }): Promise<User> {
    return apiClient('/users', {
      method: 'POST',
      body: JSON.stringify(data),
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
};
