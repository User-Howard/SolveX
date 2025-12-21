'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Header } from '@/components/layout/Header';
import { problemsApi } from '@/lib/api/problems';
import { solutionsApi } from '@/lib/api/solutions';
import type { ProblemFull } from '@/types/models';

export default function ProblemDetailPage() {
  const params = useParams();
  const router = useRouter();
  const problemId = parseInt(params.id as string);
  const [data, setData] = useState<ProblemFull | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [resolving, setResolving] = useState(false);
  const [solutionCode, setSolutionCode] = useState('');
  const [solutionExplanation, setSolutionExplanation] = useState('');
  const [solutionApproach, setSolutionApproach] = useState('');
  const [solutionSuccessRate, setSolutionSuccessRate] = useState('');
  const [solutionSubmitting, setSolutionSubmitting] = useState(false);
  const [solutionError, setSolutionError] = useState<string | null>(null);

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

  const handleAddSolution = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSolutionError(null);

    const trimmedCode = solutionCode.trim();
    if (!trimmedCode) {
      setSolutionError('請輸入解法程式碼');
      return;
    }

    const parsedSuccessRate =
      solutionSuccessRate.trim() === ''
        ? undefined
        : Number(solutionSuccessRate);

    if (
      parsedSuccessRate !== undefined &&
      (!Number.isFinite(parsedSuccessRate) ||
        parsedSuccessRate < 0 ||
        parsedSuccessRate > 100)
    ) {
      setSolutionError('成功率需介於 0 到 100');
      return;
    }

    try {
      setSolutionSubmitting(true);
      const result = await solutionsApi.createSolution(problemId, {
        problem_id: problemId,
        code_snippet: trimmedCode,
        explanation: solutionExplanation.trim() || undefined,
        approach_type: solutionApproach.trim() || undefined,
        success_rate: parsedSuccessRate,
      });
      setSolutionCode('');
      setSolutionExplanation('');
      setSolutionApproach('');
      setSolutionSuccessRate('');
      setData((prev) =>
        prev
          ? {
              ...prev,
              solutions: [result, ...prev.solutions],
            }
          : prev
      );
    } catch (err) {
      setSolutionError(err instanceof Error ? err.message : '新增解法失敗');
    } finally {
      setSolutionSubmitting(false);
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
              <div className="flex-1">
                <h1 className="card-title text-3xl mb-2">{data.problem.title}</h1>
                {data.problem.author && (
                  <div className="text-sm text-base-content/60 mt-1">
                    作者: {data.problem.author.username}
                  </div>
                )}
              </div>
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
          <div className="card bg-base-100 shadow-md mb-4">
            <div className="card-body">
              <h3 className="text-lg font-semibold mb-2">新增解法</h3>
              {solutionError && (
                <div className="alert alert-error mb-3">
                  <span>{solutionError}</span>
                </div>
              )}
              <form onSubmit={handleAddSolution} className="space-y-4">
                <div className="form-control">
                  <div className="flex items-start space-x-4">
                    <label className="label w-24 pt-2">
                      <span className="label-text">程式碼</span>
                    </label>
                    <textarea
                      className="textarea textarea-bordered min-h-[140px] flex-1"
                      value={solutionCode}
                      onChange={(event) => setSolutionCode(event.target.value)}
                      placeholder="貼上你的解法程式碼"
                      required
                    />
                  </div>
                </div>

                <div className="form-control">
                  <div className="flex items-start space-x-4">
                    <label className="label w-24 pt-2">
                      <span className="label-text">解法說明</span>
                    </label>
                    <textarea
                      className="textarea textarea-bordered flex-1"
                      value={solutionExplanation}
                      onChange={(event) =>
                        setSolutionExplanation(event.target.value)
                      }
                      placeholder="補充說明思路或注意事項"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="form-control">
                    <div className="flex items-center space-x-4">
                      <label className="label w-24">
                        <span className="label-text">解法類型</span>
                      </label>
                      <input
                        type="text"
                        className="input input-bordered flex-1"
                        value={solutionApproach}
                        onChange={(event) =>
                          setSolutionApproach(event.target.value)
                        }
                        placeholder="例如：Greedy / DP"
                      />
                    </div>
                  </div>

                  <div className="form-control">
                    <div className="flex items-center space-x-4">
                      <label className="label w-24">
                        <span className="label-text">成功率 (%)</span>
                      </label>
                      <input
                        type="number"
                        min={0}
                        max={100}
                        step={0.1}
                        className="input input-bordered flex-1"
                        value={solutionSuccessRate}
                        onChange={(event) =>
                          setSolutionSuccessRate(event.target.value)
                        }
                        placeholder="例如：80.5"
                      />
                    </div>
                  </div>
                </div>

                <div className="card-actions justify-end">
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={solutionSubmitting}
                  >
                    {solutionSubmitting ? (
                      <>
                        <span className="loading loading-spinner"></span>
                        建立中...
                      </>
                    ) : (
                      '新增解法'
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
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
              {data.linked_resources.map((resource, index) => (
                <div
                  key={`${resource.resource_id}-${resource.url}-${index}`}
                  className="card bg-base-200 shadow-sm"
                >
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
