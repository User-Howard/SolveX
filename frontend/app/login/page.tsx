'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { usersApi } from '@/lib/api/users';
import { authStorage } from '@/lib/auth';

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);

    const trimmedUsername = username.trim();
    const trimmedEmail = email.trim();

    if (!trimmedUsername || !trimmedEmail) {
      setError('請輸入帳號與 Email');
      return;
    }

    try {
      setSubmitting(true);
      const user = await findUserByCredentials(trimmedUsername, trimmedEmail);
      authStorage.save(user);
      router.push('/problems');
    } catch (err) {
      setError(err instanceof Error ? err.message : '登入失敗');
    } finally {
      setSubmitting(false);
    }
  };

  const findUserByCredentials = async (lookupUsername: string, lookupEmail: string) => {
    const cached = authStorage.load();
    if (cached && cached.username === lookupUsername && cached.email === lookupEmail) {
      return cached;
    }

    const maxProbeId = 50;
    for (let userId = 1; userId <= maxProbeId; userId += 1) {
      try {
        const user = await usersApi.getUser(userId);
        if (user.username === lookupUsername && user.email === lookupEmail) {
          return user;
        }
      } catch {
        // Ignore missing IDs during the temporary lookup.
      }
    }

    throw new Error('找不到符合的使用者');
  };

  return (
    <div className="min-h-screen bg-base-100">
      <Header />
      <main className="container mx-auto px-4 py-10 max-w-2xl">
        <div className="card bg-base-100 shadow-lg">
          <div className="card-body">
            <h1 className="text-3xl font-bold mb-2">登入</h1>
            <p className="text-base-content/70 mb-6">
              使用使用者名稱與 Email 進行登入。
            </p>

            {error && (
              <div className="alert alert-error mb-4">
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="form-control">
                <div className="flex flex-col gap-2 md:flex-row md:items-center md:gap-4">
                  <label className="label md:w-28">
                    <span className="label-text">使用者名稱</span>
                  </label>
                  <input
                    type="text"
                    className="input input-bordered flex-1"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                    placeholder="你的帳號"
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
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    placeholder="name@example.com"
                    required
                  />
                </div>
              </div>

              <div className="card-actions justify-end">
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={submitting}
                >
                  {submitting ? (
                    <>
                      <span className="loading loading-spinner"></span>
                      登入中...
                    </>
                  ) : (
                    '登入'
                  )}
                </button>
              </div>
            </form>

            <div className="divider"></div>
            <p className="text-sm text-base-content/70">
              沒有帳號？{' '}
              <Link href="/signup" className="link link-primary">
                立即註冊
              </Link>
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
