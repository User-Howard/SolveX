import { apiClient } from './client';
import type { Problem, ProblemFull } from '@/types/models';

export const problemsApi = {
  async getProblems(params?: {
    keyword?: string;
    type?: string;
    tag?: string;
  }): Promise<Problem[]> {
    const query = new URLSearchParams(
      Object.entries(params || {}).filter(([_, v]) => v !== undefined) as [string, string][]
    ).toString();
    return apiClient(`/problems${query ? `?${query}` : ''}`);
  },

  async getProblem(problemId: number): Promise<Problem> {
    return apiClient(`/problems/${problemId}`);
  },

  async getProblemFull(problemId: number): Promise<ProblemFull> {
    return apiClient(`/problems/${problemId}/full`);
  },

  async createProblem(data: {
    user_id: number;
    title: string;
    description?: string;
    problem_type?: string;
    tags?: number[];
  }): Promise<Problem> {
    return apiClient('/problems', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async updateProblem(
    problemId: number,
    data: Partial<Problem>
  ): Promise<Problem> {
    return apiClient(`/problems/${problemId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  },

  async resolveProblem(problemId: number): Promise<Problem> {
    return apiClient(`/problems/${problemId}/resolve`, {
      method: 'POST',
    });
  },
};

