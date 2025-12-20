'use client';

import { useState, useEffect } from 'react';
import { Header } from '@/components/layout/Header';
import { ProblemCard } from '@/components/features/ProblemCard';
import { problemsApi } from '@/lib/api/problems';
import type { Problem } from '@/types/models';

export default function ProblemsPage() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [keyword, setKeyword] = useState('');

  useEffect(() => {
    async function fetchProblems() {
      try {
        setLoading(true);
        const data = await problemsApi.getProblems({ keyword: keyword || undefined });
        setProblems(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : '載入問題失敗');
      } finally {
        setLoading(false);
      }
    }

    fetchProblems();
  }, [keyword]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // Search is handled by useEffect when keyword changes
  };

  return (
    <div className="min-h-screen bg-base-100">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold mb-4">問題列表</h1>
          <form onSubmit={handleSearch} className="flex gap-2">
            <input
              type="text"
              placeholder="搜尋問題..."
              className="input input-bordered flex-1"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
            />
            <button type="submit" className="btn btn-primary">
              搜尋
            </button>
          </form>
        </div>

        {loading && (
          <div className="flex justify-center items-center py-12">
            <span className="loading loading-spinner loading-lg"></span>
          </div>
        )}

        {error && (
          <div className="alert alert-error mb-4">
            <span>{error}</span>
          </div>
        )}

        {!loading && !error && (
          <>
            {problems.length === 0 ? (
              <div className="alert alert-info">
                <span>目前沒有問題</span>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {problems.map((problem) => (
                  <ProblemCard key={problem.problem_id} problem={problem} />
                ))}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}

