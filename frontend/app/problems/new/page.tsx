'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Header } from '@/components/layout/Header';
import { problemsApi } from '@/lib/api/problems';
import { tagsApi } from '@/lib/api/tags';
import type { Problem } from '@/types/models';
import type { Tag } from '@/types/models';

export default function NewProblemPage() {
  const router = useRouter();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [problemType, setProblemType] = useState('');
  const [userId, setUserId] = useState('1');
  const [availableTags, setAvailableTags] = useState<Tag[]>([]);
  const [selectedTags, setSelectedTags] = useState<number[]>([]);
  const [tagListOpen, setTagListOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [createdProblem, setCreatedProblem] = useState<Problem | null>(null);

  useEffect(() => {
    let mounted = true;

    async function fetchTags() {
      try {
        const data = await tagsApi.getTags();
        if (mounted) {
          setAvailableTags(data);
        }
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : '載入標籤失敗');
        }
      }
    }

    fetchTags();

    return () => {
      mounted = false;
    };
  }, []);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setCreatedProblem(null);

    const trimmedTitle = title.trim();
    const parsedUserId = Number(userId);
    if (!trimmedTitle) {
      setError('請輸入問題標題');
      return;
    }
    if (!Number.isFinite(parsedUserId) || parsedUserId <= 0) {
      setError('使用者 ID 必須是正整數');
      return;
    }

    try {
      setSubmitting(true);
      const result = await problemsApi.createProblem({
        user_id: parsedUserId,
        title: trimmedTitle,
        description: description.trim() || undefined,
        problem_type: problemType.trim() || undefined,
        tags: selectedTags.length ? selectedTags : undefined,
      });
      setCreatedProblem(result);
      setTitle('');
      setDescription('');
      setProblemType('');
      setSelectedTags([]);
    } catch (err) {
      setError(err instanceof Error ? err.message : '新增問題失敗');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-base-100">
      <Header />
      <main className="container mx-auto px-4 py-8 max-w-3xl">
        <div className="mb-6">
          <h1 className="text-3xl font-bold">新增問題</h1>
          <p className="text-base-content/70 mt-2">
            填寫問題資訊，系統將自動寫入資料庫。
          </p>
        </div>

        {error && (
          <div className="alert alert-error mb-4">
            <span>{error}</span>
          </div>
        )}

        {createdProblem && (
          <div className="alert alert-success mb-4">
            <span>已建立問題 #{createdProblem.problem_id}</span>
            <div className="flex gap-2">
              <Link
                href={`/problems/${createdProblem.problem_id}`}
                className="btn btn-sm btn-success"
              >
                查看詳情
              </Link>
              <button
                type="button"
                onClick={() => router.push('/problems')}
                className="btn btn-sm btn-outline"
              >
                返回列表
              </button>
            </div>
          </div>
        )}

        <div className="card bg-base-100 shadow-lg">
          <div className="card-body">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="form-control">
                <div className="flex items-center space-x-4">
                  <label className="label w-24">
                    <span className="label-text">問題標題</span>
                  </label>
                  <input
                    type="text"
                    className="input input-bordered flex-1"
                    value={title}
                    onChange={(event) => setTitle(event.target.value)}
                    placeholder="例如：如何處理 React 狀態同步問題"
                    required
                  />
                </div>
              </div>

              <div className="form-control">
                <div className="flex items-start space-x-4">
                  <label className="label w-24 pt-2">
                    <span className="label-text">問題描述</span>
                  </label>
                  <textarea
                    className="textarea textarea-bordered min-h-[120px] flex-1"
                    value={description}
                    onChange={(event) => setDescription(event.target.value)}
                    placeholder="補充問題背景、重現步驟或錯誤訊息"
                  />
                </div>
              </div>

              <div className="form-control">
                <div className="flex items-center space-x-4">
                  <label className="label w-24">
                    <span className="label-text">問題類型</span>
                  </label>
                  <input
                    type="text"
                    className="input input-bordered flex-1"
                    value={problemType}
                    onChange={(event) => setProblemType(event.target.value)}
                    placeholder="例如：Frontend / Backend / Database"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="form-control">
                  <div className="flex items-center space-x-4">
                    <label className="label w-24">
                      <span className="label-text">使用者 ID</span>
                    </label>
                    <input
                      type="number"
                      min={1}
                      className="input input-bordered flex-1"
                      value={userId}
                      onChange={(event) => setUserId(event.target.value)}
                      required
                    />
                  </div>
                </div>

              </div>

              <div className="form-control">
                <div className="flex items-start space-x-4">
                  <label className="label w-24 pt-2">
                    <span className="label-text">標籤</span>
                  </label>
                  <div className="flex-1 space-y-3">
                    <button
                      type="button"
                      onClick={() => setTagListOpen((prev) => !prev)}
                      className="input input-bordered flex w-full items-center justify-between"
                    >
                      <span className="text-base-content/70">
                        {selectedTags.length
                          ? `已選 ${selectedTags.length} 個標籤`
                          : '點擊選擇標籤'}
                      </span>
                      <span className="text-base-content/50">
                        {tagListOpen ? '收合' : '展開'}
                      </span>
                    </button>

                    {selectedTags.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {selectedTags.map((tagId) => {
                          const tag = availableTags.find(
                            (item) => item.tag_id === tagId
                          );
                          return (
                            <div key={tagId} className="badge badge-primary gap-2">
                              {tag?.tag_name || `#${tagId}`}
                              <button
                                type="button"
                                onClick={() =>
                                  setSelectedTags((prev) =>
                                    prev.filter((id) => id !== tagId)
                                  )
                                }
                                className="btn btn-ghost btn-xs"
                              >
                                ×
                              </button>
                            </div>
                          );
                        })}
                      </div>
                    )}

                    {tagListOpen && (
                      <div className="rounded-box border border-base-300 bg-base-100 p-2 shadow-sm max-h-48 overflow-y-auto">
                        {availableTags.length === 0 ? (
                          <div className="px-2 py-1 text-sm text-base-content/60">
                            目前沒有可用標籤
                          </div>
                        ) : (
                          <ul className="menu menu-sm">
                            {availableTags.map((tag) => {
                              const isSelected = selectedTags.includes(tag.tag_id);
                              return (
                                <li key={tag.tag_id}>
                                  <button
                                    type="button"
                                    onClick={() => {
                                      setSelectedTags((prev) =>
                                        isSelected
                                          ? prev.filter((id) => id !== tag.tag_id)
                                          : [...prev, tag.tag_id]
                                      );
                                    }}
                                    className={isSelected ? 'active font-semibold' : undefined}
                                  >
                                    {tag.tag_name}
                                  </button>
                                </li>
                              );
                            })}
                          </ul>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>

              <div className="card-actions justify-end gap-2 pt-2">
                <Link href="/problems" className="btn btn-outline">
                  取消
                </Link>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={submitting}
                >
                  {submitting ? (
                    <>
                      <span className="loading loading-spinner"></span>
                      建立中...
                    </>
                  ) : (
                    '建立問題'
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
