export interface User {
  user_id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  created_at: string;
}

export interface Problem {
  problem_id: number;
  user_id: number;
  title: string;
  description?: string;
  problem_type?: string;
  resolved: boolean;
  created_at: string;
  updated_at: string;
}

export interface Solution {
  solution_id: number;
  problem_id: number;
  code_snippet: string;
  explanation?: string;
  approach_type?: string;
  parent_solution_id?: number;
  version_number: number;
  improvement_description?: string;
  success_rate?: number;
  branch_type?: string;
  created_at: string;
}

export interface Resource {
  resource_id: number;
  user_id: number;
  url: string;
  title?: string;
  source_platform?: string;
  content_summary?: string;
  usefulness_score?: number;
  created_at: string;
  last_visit_at: string;
}

export interface Tag {
  tag_id: number;
  tag_name: string;
  category?: string;
  description?: string;
  created_at: string;
}

export interface ProblemFull {
  problem: Problem;
  solutions: Solution[];
  tags: Tag[];
  linked_resources: Resource[];
  relations_out: ProblemRelation[];
  relations_in: ProblemRelation[];
}

export interface ProblemRelation {
  from_problem_id: number;
  to_problem_id: number;
  relation_type?: string;
  strength?: number;
  created_at: string;
}

