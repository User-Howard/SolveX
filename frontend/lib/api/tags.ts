import { apiClient } from './client';
import type { Tag } from '@/types/models';

export const tagsApi = {
  async getTags(): Promise<Tag[]> {
    return apiClient('/tags');
  },
};
