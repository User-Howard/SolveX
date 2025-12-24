'use client';

import { useEffect, useRef, useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ProblemCard } from '@/components/features/ProblemCard';
import { problemsApi } from '@/lib/api/problems';
import type { Problem } from '@/types/models';

const LS_KEY = 'solvex.deletedProblemIds';

export default function ProblemsPage() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [keywordDraft, setKeywordDraft] = useState('');
  const [keyword, setKeyword] = useState('');

  const [deletedIds, setDeletedIds] = useState<number[]>([]);
  const [showDeleted, setShowDeleted] = useState(false);

  const requestIdRef = useRef(0);
  const skipFirstDeletedWriteRef = useRef(true);

  useEffect(() => {
    const raw = localStorage.getItem(LS_KEY);
    if (!raw) return;
    try {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        setDeletedIds(parsed.filter((x) => Number.isFinite(x)));
      }
    } catch {}
  }, []);

  useEffect(() => {
    if (skipFirstDeletedWriteRef.current) {
      skipFirstDeletedWriteRef.current = false;
      return;
    }
    localStorage.setItem(LS_KEY, JSON.stringify(deletedIds));
  }, [deletedIds]);

  useEffect(() => {
    const t = window.setTimeout(() => setKeyword(keywordDraft.trim()), 350);
    return () => window.clearTimeout(t);
  }, [keywordDraft]);

  useEffect(() => {
    let alive = true;
    const myRequestId = ++requestIdRef.current;

    async function fetchProblems() {
      try {
        setLoading(true);
        setError(null);

        const data = await problemsApi.getProblems({
          keyword: keyword ? keyword : undefined,
        });

        if (!alive || myRequestId !== requestIdRef.current) return;
        setProblems(data);
      } catch (err) {
        if (!alive || myRequestId !== requestIdRef.current) return;
        setError(err instanceof Error ? err.message : '載入問題失敗');
      } finally {
        if (!alive || myRequestId !== requestIdRef.current) return;
        setLoading(false);
      }
    }

    fetchProblems();
    return () => {
      alive = false;
    };
  }, [keyword]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setKeyword(keywordDraft.trim());
  };

  const hasKeyword = keywordDraft.trim().length > 0;

  const activeProblems = problems.filter((p) => !deletedIds.includes(p.problem_id));
  const deletedProblems = problems.filter((p) => deletedIds.includes(p.problem_id));
  const list = showDeleted ? deletedProblems : activeProblems;

  return (
    <div className="min-h-screen bg-base-100">
      <Header />

      <main className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="h-10 w-1 rounded-full bg-primary" />

            <h1 className="text-3xl font-bold tracking-tight">
              {showDeleted ? '刪除區' : '問題列表'}
            </h1>

            <span className="text-sm text-base-content/50 mt-1">
              （共 {list.length} 筆）
            </span>

            <div className="ml-auto flex gap-2">
              <button
                type="button"
                onClick={() => setShowDeleted(false)}
                className={`
                  btn btn-sm
                  ${!showDeleted
                    ? 'bg-orange-50 text-orange-800 hover:bg-orange-100 border border-orange-200'
                    : 'btn-ghost'}
                `}
              >
                回到列表
              </button>

              <button
                type="button"
                className={`btn btn-sm ${showDeleted ? 'btn-primary' : 'btn-ghost'}`}
                onClick={() => setShowDeleted(true)}
              >
                刪除區
              </button>
            </div>
          </div>

          <form onSubmit={handleSearch} className="flex gap-2">
            <input
              type="text"
              placeholder="搜尋問題..."
              className="input input-bordered flex-1"
              value={keywordDraft}
              onChange={(e) => setKeywordDraft(e.target.value)}
            />

            {hasKeyword && (
              <button
                type="button"
                className="btn btn-ghost"
                onClick={() => {
                  setKeywordDraft('');
                  setKeyword('');
                }}
              >
                清除
              </button>
            )}

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

        {!loading && error && (
          <div className="alert alert-error mb-4">
            <span>{error}</span>
          </div>
        )}

        {!loading && !error && (
          <>
            {list.length === 0 ? (
              <div className="alert alert-info">
                <span className="font-semibold">
                  {showDeleted
                    ? '刪除區目前是空的'
                    : keyword
                    ? `找不到符合「${keyword}」的問題`
                    : '目前沒有問題'}
                </span>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                {list.map((problem) => (
                  <ProblemCard
                    key={problem.problem_id}
                    problem={problem}
                    mode={showDeleted ? 'deleted' : 'active'}
                    onMoveToDeleted={(id) =>
                      setDeletedIds((prev) => (prev.includes(id) ? prev : [...prev, id]))
                    }
                    onRestore={(id) =>
                      setDeletedIds((prev) => prev.filter((x) => x !== id))
                    }
                  />
                ))}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}
