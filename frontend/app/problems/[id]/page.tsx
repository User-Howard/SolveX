'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Header } from '@/components/layout/Header';
import { problemsApi } from '@/lib/api/problems';
import type { ProblemFull } from '@/types/models';

export default function ProblemDetailPage() {
  const params = useParams();
  const router = useRouter();
  const problemId = parseInt(params.id as string);
  const [data, setData] = useState<ProblemFull | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [resolving, setResolving] = useState(false);

  useEffect(() => {
    async function fetchProblem() {
      try {
        setLoading(true);
        const result = await problemsApi.getProblemFull(problemId);
        setData(result);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : '載入問題失敗');
      } finally {
        setLoading(false);
      }
    }

    if (!isNaN(problemId)) {
      fetchProblem();
    }
  }, [problemId]);

  const handleResolve = async () => {
    if (!data || data.problem.resolved) return;
    
    try {
      setResolving(true);
      await problemsApi.resolveProblem(problemId);
      // Refresh data
      const result = await problemsApi.getProblemFull(problemId);
      setData(result);
    } catch (err) {
      alert(err instanceof Error ? err.message : '標記失敗');
    } finally {
      setResolving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-base-100">
        <Header />
        <div className="flex justify-center items-center min-h-[60vh]">
          <span className="loading loading-spinner loading-lg"></span>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-base-100">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <div className="alert alert-error">
            <span>{error || '找不到問題'}</span>
          </div>
          <button
            onClick={() => router.push('/problems')}
            className="btn btn-primary mt-4"
          >
            返回問題列表
          </button>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-base-100">
      <Header />
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Problem Card */}
        <div className="card bg-base-100 shadow-lg mb-6">
          <div className="card-body">
            <div className="flex items-start justify-between gap-4 mb-4">
              <h1 className="card-title text-3xl flex-1">{data.problem.title}</h1>
              {data.problem.resolved ? (
                <div className="badge badge-success badge-lg">已解決</div>
              ) : (
                <button
                  onClick={handleResolve}
                  disabled={resolving}
                  className="btn btn-success btn-sm"
                >
                  {resolving ? (
                    <>
                      <span className="loading loading-spinner loading-xs"></span>
                      處理中...
                    </>
                  ) : (
                    '標記為已解決'
                  )}
                </button>
              )}
            </div>

            {data.problem.description && (
              <p className="text-base-content/80 mb-4 whitespace-pre-wrap">
                {data.problem.description}
              </p>
            )}

            <div className="flex flex-wrap gap-2 mb-4">
              {data.problem.problem_type && (
                <div className="badge badge-outline badge-lg">
                  {data.problem.problem_type}
                </div>
              )}
              {data.tags.map((tag) => (
                <div key={tag.tag_id} className="badge badge-primary badge-lg">
                  {tag.tag_name}
                </div>
              ))}
            </div>

            <div className="text-sm text-base-content/50">
              建立時間: {new Date(data.problem.created_at).toLocaleString('zh-TW')}
            </div>
          </div>
        </div>

        {/* Solutions Section */}
        <div className="mb-6">
          <h2 className="text-2xl font-bold mb-4">解法 ({data.solutions.length})</h2>
          {data.solutions.length === 0 ? (
            <div className="alert alert-info">
              <span>目前沒有解法</span>
            </div>
          ) : (
            <div className="space-y-4">
              {data.solutions.map((solution) => (
                <div key={solution.solution_id} className="card bg-base-200 shadow-md">
                  <div className="card-body">
                    <div className="flex items-start justify-between gap-4 mb-2">
                      <h3 className="font-semibold">解法 #{solution.solution_id}</h3>
                      {solution.success_rate !== undefined && (
                        <div className="badge badge-info">
                          成功率: {solution.success_rate}%
                        </div>
                      )}
                    </div>
                    {solution.explanation && (
                      <p className="text-sm text-base-content/80 mb-3">
                        {solution.explanation}
                      </p>
                    )}
                    <div className="mockup-code">
                      <pre>
                        <code>{solution.code_snippet}</code>
                      </pre>
                    </div>
                    {solution.approach_type && (
                      <div className="mt-2">
                        <span className="badge badge-outline">{solution.approach_type}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Resources Section */}
        {data.linked_resources.length > 0 && (
          <div className="mb-6">
            <h2 className="text-2xl font-bold mb-4">相關資源 ({data.linked_resources.length})</h2>
            <div className="space-y-2">
              {data.linked_resources.map((resource) => (
                <div key={resource.resource_id} className="card bg-base-200 shadow-sm">
                  <div className="card-body py-3">
                    <a
                      href={resource.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="link link-primary"
                    >
                      {resource.title || resource.url}
                    </a>
                    {resource.content_summary && (
                      <p className="text-sm text-base-content/70">
                        {resource.content_summary}
                      </p>
                    )}
                    {resource.usefulness_score !== undefined && (
                      <div className="badge badge-sm">
                        評分: {resource.usefulness_score}/5
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="flex gap-4">
          <button
            onClick={() => router.push('/problems')}
            className="btn btn-outline"
          >
            返回列表
          </button>
        </div>
      </main>
    </div>
  );
}

