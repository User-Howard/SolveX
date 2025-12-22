'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { usersApi } from '@/lib/api/users';
import { authStorage } from '@/lib/auth';

export default function SignupPage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);

    if (!username.trim() || !email.trim()) {
      setError('請完整填寫必填欄位');
      return;
    }

    try {
      setSubmitting(true);
      const user = await usersApi.createUser({
        username: username.trim(),
        email: email.trim(),
        first_name: firstName.trim() || undefined,
        last_name: lastName.trim() || undefined,
      });
      authStorage.save(user);
      router.push('/problems');
    } catch (err) {
      setError(err instanceof Error ? err.message : '註冊失敗');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-base-100">
      <Header />
      <main className="container mx-auto px-4 py-10 max-w-2xl">
        <div className="card bg-base-100 shadow-lg">
          <div className="card-body">
            <h1 className="text-3xl font-bold mb-2">建立帳號</h1>
            <p className="text-base-content/70 mb-6">
              建立新帳號後將自動登入。
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

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="form-control">
                  <div className="flex flex-col gap-2 md:flex-row md:items-center md:gap-4">
                    <label className="label md:w-28">
                      <span className="label-text">名字</span>
                    </label>
                    <input
                      type="text"
                      className="input input-bordered flex-1"
                      value={firstName}
                      onChange={(event) => setFirstName(event.target.value)}
                      placeholder="選填"
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
                      value={lastName}
                      onChange={(event) => setLastName(event.target.value)}
                      placeholder="選填"
                    />
                  </div>
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
                      建立中...
                    </>
                  ) : (
                    '建立帳號'
                  )}
                </button>
              </div>
            </form>

            <div className="divider"></div>
            <p className="text-sm text-base-content/70">
              已有帳號？{' '}
              <Link href="/login" className="link link-primary">
                前往登入
              </Link>
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
