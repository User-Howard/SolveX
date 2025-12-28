'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { authStorage } from '@/lib/auth';
import type { User } from '@/types/models';

export function Header() {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    setUser(authStorage.load());
  }, []);

  const handleLogout = () => {
    authStorage.clear();
    setUser(null);
  };

  return (
    <div className="navbar bg-base-200 shadow-md">
      <div className="navbar-start">
        <Link href="/" className="btn btn-ghost text-xl font-bold">
          SolveX
        </Link>
      </div>
      <div className="navbar-center hidden lg:flex">
        <ul className="menu menu-horizontal gap-2">
          <li>
            <Link href="/problems" className="btn btn-ghost">
              問題列表
            </Link>
          </li>
          <li>
            <Link href="/problems/new" className="btn btn-ghost">
              新增問題
            </Link>
          </li>
          <li>
            <Link href="/resources" className="btn btn-ghost">
              學習資源
            </Link>
          </li>
        </ul>
      </div>
      <div className="navbar-end gap-2">
        {user ? (
          <>
            <div className="hidden sm:flex items-center gap-2 text-sm text-base-content/70">
              <span>已登入:</span>
              <span className="font-semibold text-base-content">
                {user.username}
              </span>
            </div>
            <button onClick={handleLogout} className="btn btn-outline btn-sm">
              登出
            </button>
          </>
        ) : (
          <>
            <Link href="/login" className="btn btn-ghost btn-sm">
              登入
            </Link>
            <Link href="/signup" className="btn btn-primary btn-sm">
              註冊
            </Link>
          </>
        )}
        <div className="dropdown dropdown-end">
          <div tabIndex={0} role="button" className="btn btn-ghost btn-circle">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </div>
          <ul
            tabIndex={0}
            className="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow"
          >
            <li>
              <Link href="/problems">問題列表</Link>
            </li>
            <li>
              <Link href="/problems/new">新增問題</Link>
            </li>
            <li>
              <Link href="/resources">學習資源</Link>
            </li>
            {user && (
              <li>
                <Link href="/account">我的帳號</Link>
              </li>
            )}
            {user ? (
              <li>
                <button type="button" onClick={handleLogout}>
                  登出
                </button>
              </li>
            ) : (
              <>
                <li>
                  <Link href="/login">登入</Link>
                </li>
                <li>
                  <Link href="/signup">註冊</Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
}
