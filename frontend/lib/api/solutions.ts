import { apiClient } from './client';
import type { Solution } from '@/types/models';

export const solutionsApi = {
  async createSolution(
    problemId: number,
    data: {
      problem_id: number;
      code_snippet: string;
      explanation?: string;
      approach_type?: string;
      parent_solution_id?: number | null;
      improvement_description?: string;
      success_rate?: number;
      branch_type?: string;
    }
  ): Promise<Solution> {
    return apiClient(`/problems/${problemId}/solutions`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async getSolution(solutionId: number): Promise<Solution> {
    return apiClient(`/solutions/${solutionId}`);
  },

  async updateSolution(
    solutionId: number,
    data: Partial<Solution>
  ): Promise<Solution> {
    return apiClient(`/solutions/${solutionId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  },

  async deleteSolution(solutionId: number): Promise<{ deleted: boolean }> {
    return apiClient(`/solutions/${solutionId}`, {
      method: 'DELETE',
    });
  },

  async listProblemSolutions(problemId: number): Promise<Solution[]> {
    return apiClient(`/problems/${problemId}/solutions`);
  },

  async getSolutionChildren(solutionId: number): Promise<Solution[]> {
    return apiClient(`/solutions/${solutionId}/children`);
  },
};
