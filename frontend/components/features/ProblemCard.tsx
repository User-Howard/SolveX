import Link from 'next/link';
import type { Problem } from '@/types/models';

interface ProblemCardProps {
  problem: Problem;
  className?: string;
}

export function ProblemCard({ problem, className = '' }: ProblemCardProps) {
  return (
    <Link
      href={`/problems/${problem.problem_id}`}
      className={`
        card
        block
        cursor-pointer
        transition
        hover:-translate-y-0.5
        hover:shadow-lg
        focus-visible:outline-none
        focus-visible:ring-2 focus-visible:ring-primary/40
        ${problem.resolved
          ? "bg-green-50 border border-green-200 dark:bg-green-900/20 dark:border-green-700/40"
          : "bg-base-100 shadow-md"}
        ${className}
      `}
    >
      <div className="card-body">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <h2 className="card-title text-lg transition-colors group-hover:text-primary">
              {problem.title}
            </h2>

            {problem.description && (
              <p className="text-sm text-base-content/70 mt-2 line-clamp-2">
                {problem.description}
              </p>
            )}
          </div>

          {problem.resolved && (
            <div className="badge badge-success badge-lg shrink-0">
              已解決
            </div>
          )}
        </div>

        <div className="card-actions justify-between items-center mt-4">
          <div className="flex gap-2">
            {problem.problem_type && (
              <div className="badge badge-outline">
                {problem.problem_type}
              </div>
            )}
          </div>

          <div className="text-xs text-base-content/50">
            {new Date(problem.created_at).toLocaleDateString('zh-TW')}
          </div>
        </div>
      </div>
    </Link>
  );
}
