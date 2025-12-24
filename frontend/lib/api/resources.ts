import { apiClient } from './client';
import type { ResourceSummary } from '@/types/models';

export const resourcesApi = {
  async getResources(params?: {
    tag?: string;
    min_score?: number;
    keyword?: string;
  }): Promise<ResourceSummary[]> {
    const searchParams = new URLSearchParams();

    if (params?.tag) {
      searchParams.set('tag', params.tag);
    }

    if (params?.min_score !== undefined) {
      searchParams.set('min_score', params.min_score.toString());
    }

    if (params?.keyword) {
      searchParams.set('keyword', params.keyword);
    }

    const query = searchParams.toString();
    return apiClient(`/resources${query ? `?${query}` : ''}`);
  },
};
