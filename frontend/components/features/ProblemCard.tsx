import Link from 'next/link';
import type { ReactNode } from 'react';
import type { Problem } from '@/types/models';

interface ProblemCardProps {
  problem: Problem;
  className?: string;
  actions?: ReactNode;
}

export function ProblemCard({ problem, className = '', actions }: ProblemCardProps) {
  return (
    <div className={`card bg-base-100 shadow-md hover:shadow-lg transition-shadow ${className}`}>
      <div className="card-body">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <Link href={`/problems/${problem.problem_id}`}>
              <h2 className="card-title text-lg hover:text-primary transition-colors">
                {problem.title}
              </h2>
            </Link>
            {problem.description && (
              <p className="text-sm text-base-content/70 mt-2 line-clamp-2">
                {problem.description}
              </p>
            )}
          </div>
          {problem.resolved && (
            <div className="badge badge-success badge-lg">已解決</div>
          )}
        </div>
        <div className="card-actions justify-between items-center mt-4">
          <div className="flex gap-2">
            {problem.problem_type && (
              <div className="badge badge-outline">{problem.problem_type}</div>
            )}
          </div>
          <div className="flex items-center gap-2">
            {actions}
            <div className="text-xs text-base-content/50">
              {new Date(problem.created_at).toLocaleDateString('zh-TW')}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
