'use client';

import Link from 'next/link';
import type { Problem } from '@/types/models';

interface ProblemCardProps {
  problem: Problem;
  className?: string;
  mode?: 'active' | 'deleted';
  onMoveToDeleted?: (id: number) => void;
  onRestore?: (id: number) => void;
}

export function ProblemCard({
  problem,
  className = '',
  mode = 'active',
  onMoveToDeleted,
  onRestore,
}: ProblemCardProps) {
  const stop = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  return (
    <Link
      href={`/problems/${problem.problem_id}`}
      className={`
        card block cursor-pointer transition
        hover:-translate-y-0.5 hover:shadow-lg
        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/40
        ${mode === 'deleted' ? 'opacity-80' : ''}
        ${
          problem.resolved
            ? 'bg-green-50 border border-green-200 dark:bg-green-900/20 dark:border-green-700/40'
            : 'bg-base-100 shadow-md'
        }
        ${className}
      `}
    >
      <div className="card-body">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <h2 className="card-title text-lg">
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
          <div className="flex items-center gap-2">
            {mode === 'active' ? (
              <button
                type="button"
                onClick={(e) => {
                  stop(e);
                  onMoveToDeleted?.(problem.problem_id);
                }}
                className="
                btn btn-ghost btn-xs
                text-blue-900/50
                hover:text-blue-900
                hover:bg-blue-900/10
                opacity-60
                hover:opacity-100
                transition
              "
              >
                刪除題目
              </button>
            ) : (
              <button
                type="button"
                onClick={(e) => {
                  stop(e);
                  onRestore?.(problem.problem_id);
                }}
               className="
                btn btn-ghost btn-xs
                text-blue-900/50
                hover:text-blue-900
                hover:bg-blue-900/10
                opacity-60
                hover:opacity-100
                transition
              "
              >
                還原
              </button>
            )}

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
