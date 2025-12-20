import Link from 'next/link';
import { Header } from '@/components/layout/Header';

export default function Home() {
  return (
    <div className="min-h-screen bg-base-100">
      <Header />
      <main className="container mx-auto px-4 py-16">
        <div className="hero bg-base-200 rounded-lg mb-12">
          <div className="hero-content text-center">
            <div className="max-w-md">
              <h1 className="text-5xl font-bold mb-4">SolveX</h1>
              <p className="text-lg mb-6">
                程式學習者的知識管理系統
                <br />
                整合多元學習資源，解決知識碎片化問題
              </p>
              <div className="flex gap-4 justify-center">
                <Link href="/problems" className="btn btn-primary">
                  瀏覽問題
                </Link>
                <Link href="/problems/new" className="btn btn-outline">
                  新增問題
                </Link>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="card bg-base-100 shadow-md">
            <div className="card-body">
              <h2 className="card-title">問題管理</h2>
              <p>記錄與追蹤程式學習過程中遇到的問題</p>
              <div className="card-actions justify-end">
                <Link href="/problems" className="btn btn-primary btn-sm">
                  查看
                </Link>
              </div>
            </div>
          </div>

          <div className="card bg-base-100 shadow-md">
            <div className="card-body">
              <h2 className="card-title">解法追蹤</h2>
              <p>管理多種解法，追蹤版本演進與成功率</p>
              <div className="card-actions justify-end">
                <Link href="/problems" className="btn btn-secondary btn-sm">
                  查看
                </Link>
              </div>
            </div>
          </div>

          <div className="card bg-base-100 shadow-md">
            <div className="card-body">
              <h2 className="card-title">資源整合</h2>
              <p>集中管理來自不同平台的學習資源</p>
              <div className="card-actions justify-end">
                <Link href="/resources" className="btn btn-accent btn-sm">
                  查看
                </Link>
              </div>
            </div>
          </div>
        </div>

        <div className="alert alert-info">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            className="stroke-current shrink-0 w-6 h-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
          </svg>
          <span>這是一個簡潔的 prototype，展示 SolveX 的核心功能</span>
        </div>
      </main>
    </div>
  );
}
