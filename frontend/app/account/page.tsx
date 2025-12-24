'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { Header } from '@/components/layout/Header';
import { usersApi } from '@/lib/api/users';
import { problemsApi } from '@/lib/api/problems';
import { authStorage } from '@/lib/auth';
import { ProblemCard } from '@/components/features/ProblemCard';
import type { Problem, User } from '@/types/models';

export default function AccountPage() {
  const [user, setUser] = useState<User | null>(null);
  const [problems, setProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState(false);
  const [formUsername, setFormUsername] = useState('');
  const [formEmail, setFormEmail] = useState('');
  const [formFirstName, setFormFirstName] = useState('');
  const [formLastName, setFormLastName] = useState('');
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const [deletingProblemId, setDeletingProblemId] = useState<number | null>(null);

  useEffect(() => {
    const currentUser = authStorage.load();
    setUser(currentUser);

    if (!currentUser) {
      setLoading(false);
      return;
    }

    let mounted = true;

    async function fetchData() {
      try {
        const [freshUser, userProblems] = await Promise.all([
          usersApi.getUser(currentUser.user_id),
          usersApi.getUserProblems(currentUser.user_id),
        ]);
        if (!mounted) return;
        setUser(freshUser);
        setProblems(userProblems);
        setFormUsername(freshUser.username);
        setFormEmail(freshUser.email);
        setFormFirstName(freshUser.first_name || '');
        setFormLastName(freshUser.last_name || '');
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : '載入資料失敗');
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    fetchData();

    return () => {
      mounted = false;
    };
  }, []);

  const handleEditStart = () => {
    if (!user) return;
    setFormUsername(user.username);
    setFormEmail(user.email);
    setFormFirstName(user.first_name || '');
    setFormLastName(user.last_name || '');
    setSaveError(null);
    setEditing(true);
  };

  const handleEditCancel = () => {
    if (!user) return;
    setFormUsername(user.username);
    setFormEmail(user.email);
    setFormFirstName(user.first_name || '');
    setFormLastName(user.last_name || '');
    setSaveError(null);
    setEditing(false);
  };

  const handleSave = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!user) return;
    setSaveError(null);

    const trimmedUsername = formUsername.trim();
    const trimmedEmail = formEmail.trim();
    if (!trimmedUsername || !trimmedEmail) {
      setSaveError('使用者名稱與 Email 為必填');
      return;
    }

    try {
      setSaving(true);
      const updated = await usersApi.updateUser(user.user_id, {
        username: trimmedUsername,
        email: trimmedEmail,
        first_name: formFirstName.trim() || undefined,
        last_name: formLastName.trim() || undefined,
      });
      setUser(updated);
      authStorage.save(updated);
      setEditing(false);
    } catch (err) {
      setSaveError(err instanceof Error ? err.message : '更新失敗');
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteProblem = async (problem: Problem) => {
    const confirmed = window.confirm('確定要刪除這個問題嗎？此操作無法復原。');
    if (!confirmed) return;
    setDeleteError(null);
    setDeletingProblemId(problem.problem_id);
    try {
      await problemsApi.deleteProblem(problem.problem_id);
      setProblems((prev) =>
        prev.filter((item) => item.problem_id !== problem.problem_id)
      );
    } catch (err) {
      setDeleteError(err instanceof Error ? err.message : '刪除失敗');
    } finally {
      setDeletingProblemId(null);
    }
  };

  return (
    <div className="min-h-screen bg-base-100">
      <Header />
      <main className="container mx-auto px-4 py-8 max-w-5xl">
        <div className="mb-6">
          <h1 className="text-3xl font-bold">我的帳號</h1>
          <p className="text-base-content/70 mt-2">
            查看你的帳號資料與提交的問題。
          </p>
        </div>

        {!user && !loading && (
          <div className="alert alert-warning mb-6">
            <span>尚未登入，請先登入。</span>
            <Link href="/login" className="btn btn-sm btn-primary">
              前往登入
            </Link>
          </div>
        )}

        {error && (
          <div className="alert alert-error mb-6">
            <span>{error}</span>
          </div>
        )}

        {user && (
          <div className="card bg-base-100 shadow-lg mb-8">
            <div className="card-body">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">帳號資訊</h2>
                {!editing && (
                  <button
                    type="button"
                    onClick={handleEditStart}
                    className="btn btn-outline btn-sm"
                  >
                    編輯
                  </button>
                )}
              </div>

              {editing ? (
                <form onSubmit={handleSave} className="space-y-4">
                  {saveError && (
                    <div className="alert alert-error">
                      <span>{saveError}</span>
                    </div>
                  )}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="form-control">
                      <div className="flex flex-col gap-2 md:flex-row md:items-center md:gap-4">
                        <label className="label md:w-28">
                          <span className="label-text">使用者名稱</span>
                        </label>
                        <input
                          type="text"
                          className="input input-bordered flex-1"
                          value={formUsername}
                          onChange={(event) => setFormUsername(event.target.value)}
                          required
                        />
                      </div>
                    </div>

                    <div className="form-control">
                      <div className="flex flex-col gap-2 md:flex-row md:items-center md:gap-4">
                        <label className="label md:w-28">
                          <span className="label-text">Email</span>
                        </label>
                        <input
                          type="email"
                          className="input input-bordered flex-1"
                          value={formEmail}
                          onChange={(event) => setFormEmail(event.target.value)}
                          required
                        />
                      </div>
                    </div>

                    <div className="form-control">
                      <div className="flex flex-col gap-2 md:flex-row md:items-center md:gap-4">
                        <label className="label md:w-28">
                          <span className="label-text">名字</span>
                        </label>
                        <input
                          type="text"
                          className="input input-bordered flex-1"
                          value={formFirstName}
                          onChange={(event) => setFormFirstName(event.target.value)}
                        />
                      </div>
                    </div>

                    <div className="form-control">
                      <div className="flex flex-col gap-2 md:flex-row md:items-center md:gap-4">
                        <label className="label md:w-28">
                          <span className="label-text">姓氏</span>
                        </label>
                        <input
                          type="text"
                          className="input input-bordered flex-1"
                          value={formLastName}
                          onChange={(event) => setFormLastName(event.target.value)}
                        />
                      </div>
                    </div>
                  </div>

                  <div className="card-actions justify-end gap-2">
                    <button
                      type="button"
                      onClick={handleEditCancel}
                      className="btn btn-outline"
                      disabled={saving}
                    >
                      取消
                    </button>
                    <button
                      type="submit"
                      className="btn btn-primary"
                      disabled={saving}
                    >
                      {saving ? (
                        <>
                          <span className="loading loading-spinner"></span>
                          儲存中...
                        </>
                      ) : (
                        '儲存'
                      )}
                    </button>
                  </div>
                </form>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <div className="text-base-content/60">使用者名稱</div>
                    <div className="font-semibold">{user.username}</div>
                  </div>
                  <div>
                    <div className="text-base-content/60">Email</div>
                    <div className="font-semibold">{user.email}</div>
                  </div>
                  <div>
                    <div className="text-base-content/60">名字</div>
                    <div className="font-semibold">{user.first_name || '-'}</div>
                  </div>
                  <div>
                    <div className="text-base-content/60">姓氏</div>
                    <div className="font-semibold">{user.last_name || '-'}</div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {user && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold">提交的問題</h2>
              <Link href="/problems/new" className="btn btn-primary btn-sm">
                新增問題
              </Link>
            </div>

            {deleteError && (
              <div className="alert alert-error mb-4">
                <span>{deleteError}</span>
              </div>
            )}

            {loading ? (
              <div className="flex justify-center items-center py-10">
                <span className="loading loading-spinner loading-lg"></span>
              </div>
            ) : problems.length === 0 ? (
              <div className="alert alert-info">
                <span>目前沒有提交的問題</span>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {problems.map((problem) => (
                  <ProblemCard
                    key={problem.problem_id}
                    problem={problem}
                    actions={
                      <button
                        type="button"
                        className="btn btn-ghost btn-xs text-error"
                        onClick={() => handleDeleteProblem(problem)}
                        disabled={deletingProblemId === problem.problem_id}
                      >
                        {deletingProblemId === problem.problem_id ? '刪除中...' : '刪除'}
                      </button>
                    }
                  />
                ))}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
