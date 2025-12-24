'use client';

import { useEffect, useState } from 'react';
import { Header } from '@/components/layout/Header';
import { resourcesApi } from '@/lib/api/resources';
import type { ResourceSummary } from '@/types/models';

export default function ResourcesPage() {
  const [resources, setResources] = useState<ResourceSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    async function fetchResources() {
      try {
        setLoading(true);
        const data = await resourcesApi.getResources();
        if (mounted) {
          setResources(data);
          setError(null);
        }
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : '載入資源失敗');
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    fetchResources();

    return () => {
      mounted = false;
    };
  }, []);

  const formatDate = (value?: string | null) => {
    if (!value) return '—';
    const parsed = new Date(value);
    if (Number.isNaN(parsed.getTime())) return '—';
    return parsed.toLocaleString('zh-TW');
  };

  return (
    <div className="min-h-screen bg-base-100">
      <Header />
      <main className="container mx-auto px-4 py-8 max-w-5xl">
        <div className="flex items-center justify-between flex-wrap gap-3 mb-6">
          <div>
            <h1 className="text-3xl font-bold">學習資源</h1>
            <p className="text-base-content/70 mt-2">
              目前共 {resources.length} 筆資源
            </p>
          </div>
        </div>

        {loading && (
          <div className="flex justify-center items-center min-h-[50vh]">
            <span className="loading loading-spinner loading-lg"></span>
          </div>
        )}

        {!loading && error && (
          <div className="alert alert-error mb-6">
            <span>{error}</span>
          </div>
        )}

        {!loading && !error && resources.length === 0 && (
          <div className="alert alert-info">
            <span>目前尚無資源，請稍後再試。</span>
          </div>
        )}

        {!loading && !error && resources.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {resources.map((resource) => (
              <div
                key={resource.resource_id}
                className="card bg-base-100 shadow-md"
              >
                <div className="card-body">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <a
                        href={resource.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="link link-primary text-lg font-semibold"
                      >
                        {resource.title || resource.url}
                      </a>
                    </div>
                    {resource.usefulness_score !== null &&
                      resource.usefulness_score !== undefined && (
                        <div className="badge badge-primary">
                          {resource.usefulness_score.toFixed(1)}/5
                        </div>
                      )}
                  </div>
                      {resource.source_platform && (
                        <div className="badge badge-outline mt-2">
                          {resource.source_platform}
                        </div>
                      )}
                  <div>
                      
                  </div>
                  <div>
                  {resource.content_summary && (
                    <p className="text-sm text-base-content/70 mt-">
                      {resource.content_summary}
                    </p>
                  )}
                  </div>

                  <div className="text-xs text-base-content/60 mt-4 space-y-1">
                    <div>首次瀏覽: {formatDate(resource.first_visited_at)}</div>
                    <div>最近瀏覽: {formatDate(resource.last_visited_at)}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
