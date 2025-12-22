# SolveX Frontend 風格與架構指南

## 專案概述

**SolveX** 是一個程式學習者的知識管理系統，整合多元學習資源，解決知識碎片化問題。

- **前端技術棧**: Next.js 16 + React 19 + TypeScript + Tailwind 4 + DaisyUI
- **後端 API**: FastAPI (http://localhost:8000)
- **設計理念**: 簡約、乾淨、基礎互動特效

---

## 🎨 設計系統 (DaisyUI)

### 主題配色

```js
// Light Mode
primary: #3b82f6    // 主要動作按鈕
secondary: #6366f1  // 次要功能
accent: #8b5cf6     // 強調元素
neutral: #1f2937    // 文字、邊框
base-100: #ffffff   // 背景色

// Dark Mode
primary: #60a5fa
secondary: #818cf8
accent: #a78bfa
base-100: #0a0a0a
```

### 常用元件

#### 按鈕
```tsx
// 主要動作
<button className="btn btn-primary">新增問題</button>

// 次要動作
<button className="btn btn-secondary">查看詳情</button>

// 輪廓按鈕
<button className="btn btn-outline">取消</button>

// 大小變化
<button className="btn btn-sm">小按鈕</button>
<button className="btn btn-lg">大按鈕</button>
```

#### 輸入框
```tsx
// 基礎輸入
<input type="text" className="input input-bordered w-full" />

// 帶標籤
<div className="form-control">
  <label className="label">
    <span className="label-text">問題標題</span>
  </label>
  <input type="text" className="input input-bordered" />
</div>

// 文字區域
<textarea className="textarea textarea-bordered w-full" rows={4} />
```

#### 卡片
```tsx
<div className="card bg-base-100 shadow-md">
  <div className="card-body">
    <h2 className="card-title">卡片標題</h2>
    <p>內容文字</p>
    <div className="card-actions justify-end">
      <button className="btn btn-primary">動作</button>
    </div>
  </div>
</div>
```

#### 徽章與標籤
```tsx
// 標籤 (Tags)
<div className="badge badge-primary">JavaScript</div>
<div className="badge badge-secondary">React</div>
<div className="badge badge-outline">TypeScript</div>
```

#### Loading 狀態
```tsx
<span className="loading loading-spinner loading-md"></span>
<button className="btn btn-primary">
  <span className="loading loading-spinner"></span>
  載入中...
</button>
```

---

## 📁 專案架構

### 推薦資料夾結構

```
frontend/
├── app/
│   ├── (auth)/              # 認證相關頁面
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/           # 使用者儀表板
│   │   └── page.tsx
│   ├── problems/            # 問題相關頁面
│   │   ├── page.tsx         # 問題列表
│   │   ├── [id]/            # 問題詳情
│   │   │   └── page.tsx
│   │   └── new/             # 新增問題
│   │       └── page.tsx
│   ├── solutions/           # 解法頁面
│   │   └── [id]/
│   │       └── page.tsx
│   ├── resources/           # 學習資源
│   │   └── page.tsx
│   ├── tags/                # 標籤管理
│   │   └── page.tsx
│   ├── layout.tsx
│   ├── page.tsx             # 首頁
│   └── globals.css
├── components/
│   ├── ui/                  # 基礎 UI 元件
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── Badge.tsx
│   │   └── Modal.tsx
│   ├── layout/              # 佈局元件
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Footer.tsx
│   ├── features/            # 功能元件
│   │   ├── ProblemCard.tsx
│   │   ├── SolutionCard.tsx
│   │   ├── ResourceCard.tsx
│   │   ├── TagSelector.tsx
│   │   └── SearchBar.tsx
│   └── forms/               # 表單元件
│       ├── ProblemForm.tsx
│       ├── SolutionForm.tsx
│       └── ResourceForm.tsx
├── lib/
│   ├── api/                 # API 呼叫
│   │   ├── client.ts        # Axios/Fetch 設定
│   │   ├── problems.ts
│   │   ├── solutions.ts
│   │   ├── resources.ts
│   │   ├── tags.ts
│   │   └── users.ts
│   ├── hooks/               # Custom Hooks
│   │   ├── useProblem.ts
│   │   ├── useSolution.ts
│   │   └── useAuth.ts
│   └── utils/               # 工具函式
│       ├── formatDate.ts
│       └── validators.ts
├── types/
│   ├── api.ts               # API 回應型別
│   ├── models.ts            # 資料模型
│   └── index.ts
└── public/
    └── images/
```

---

## 🔧 型別定義

### 核心資料模型

```typescript
// types/models.ts

export interface User {
  user_id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  created_at: string;
}

export interface Problem {
  problem_id: number;
  user_id: number;
  title: string;
  description?: string;
  problem_type?: string;
  resolved: boolean;
  created_at: string;
  updated_at: string;
}

export interface Solution {
  solution_id: number;
  problem_id: number;
  code_snippet: string;
  explanation?: string;
  approach_type?: string;
  parent_solution_id?: number;
  version_number: number;
  improvement_description?: string;
  success_rate?: number;
  branch_type?: string;
  created_at: string;
}

export interface Resource {
  resource_id: number;
  user_id: number;
  url: string;
  title?: string;
  source_platform?: string;
  content_summary?: string;
  usefulness_score?: number;
  created_at: string;
  last_visit_at: string;
}

export interface Tag {
  tag_id: number;
  tag_name: string;
  category?: string;
  description?: string;
  created_at: string;
}

// 完整問題資料（含關聯）
export interface ProblemFull {
  problem: Problem;
  solutions: Solution[];
  tags: Tag[];
  linked_resources: Resource[];
  relations_out: ProblemRelation[];
  relations_in: ProblemRelation[];
}

export interface ProblemRelation {
  from_problem_id: number;
  to_problem_id: number;
  relation_type?: string;
  strength?: number;
  created_at: string;
}
```

---

## 🛠️ API 整合模式

### API Client 設定

```typescript
// lib/api/client.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'API request failed');
  }

  return response.json();
}
```

### API 函式範例

```typescript
// lib/api/problems.ts
import { apiClient } from './client';
import type { Problem, ProblemFull } from '@/types/models';

export const problemsApi = {
  // 取得所有問題
  async getProblems(params?: {
    keyword?: string;
    type?: string;
    tag?: string;
  }): Promise<Problem[]> {
    const query = new URLSearchParams(params as any).toString();
    return apiClient(`/problems?${query}`);
  },

  // 取得單一問題詳情
  async getProblemFull(problemId: number): Promise<ProblemFull> {
    return apiClient(`/problems/${problemId}/full`);
  },

  // 建立問題
  async createProblem(data: {
    user_id: number;
    title: string;
    description?: string;
    problem_type?: string;
    tags?: number[];
  }): Promise<Problem> {
    return apiClient('/problems', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // 更新問題
  async updateProblem(
    problemId: number,
    data: Partial<Problem>
  ): Promise<Problem> {
    return apiClient(`/problems/${problemId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  },

  // 標記問題為已解決
  async resolveProblem(problemId: number): Promise<Problem> {
    return apiClient(`/problems/${problemId}/resolve`, {
      method: 'POST',
    });
  },
};
```

---

## 🎯 元件開發規範

### 1. 元件命名

- **PascalCase**: 所有元件檔案與元件名稱
- **kebab-case**: 資料夾名稱
- **camelCase**: 函式、變數、hooks

```tsx
// ✅ 正確
components/features/ProblemCard.tsx
export function ProblemCard() {}

// ❌ 錯誤
components/features/problemCard.tsx
export function problem_card() {}
```

### 2. 元件結構模板

```tsx
// components/features/ProblemCard.tsx
import { Problem } from '@/types/models';

interface ProblemCardProps {
  problem: Problem;
  onResolve?: (id: number) => void;
  className?: string;
}

export function ProblemCard({
  problem,
  onResolve,
  className = ''
}: ProblemCardProps) {
  return (
    <div className={`card bg-base-100 shadow-md ${className}`}>
      <div className="card-body">
        <h2 className="card-title">{problem.title}</h2>
        <p className="text-sm text-neutral/70">
          {problem.description}
        </p>
        <div className="card-actions justify-between items-center">
          <div className="badge badge-outline">
            {problem.problem_type}
          </div>
          {!problem.resolved && onResolve && (
            <button
              className="btn btn-sm btn-primary"
              onClick={() => onResolve(problem.problem_id)}
            >
              標記為已解決
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
```

### 3. Custom Hook 範例

```typescript
// lib/hooks/useProblem.ts
import { useState, useEffect } from 'react';
import { problemsApi } from '@/lib/api/problems';
import type { ProblemFull } from '@/types/models';

export function useProblem(problemId: number) {
  const [data, setData] = useState<ProblemFull | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchProblem() {
      try {
        setLoading(true);
        const result = await problemsApi.getProblemFull(problemId);
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }

    fetchProblem();
  }, [problemId]);

  return { data, loading, error };
}
```

### 4. 頁面元件範例

```tsx
// app/problems/[id]/page.tsx
import { useProblem } from '@/lib/hooks/useProblem';
import { ProblemCard } from '@/components/features/ProblemCard';
import { SolutionCard } from '@/components/features/SolutionCard';

export default function ProblemDetailPage({
  params
}: {
  params: { id: string }
}) {
  const problemId = parseInt(params.id);
  const { data, loading, error } = useProblem(problemId);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="alert alert-error">
        <span>{error || '找不到問題'}</span>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <ProblemCard problem={data.problem} />

      <div className="mt-8">
        <h2 className="text-2xl font-bold mb-4">解法</h2>
        <div className="space-y-4">
          {data.solutions.map(solution => (
            <SolutionCard key={solution.solution_id} solution={solution} />
          ))}
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-2xl font-bold mb-4">標籤</h2>
        <div className="flex gap-2">
          {data.tags.map(tag => (
            <div key={tag.tag_id} className="badge badge-primary">
              {tag.tag_name}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

---

## 📋 表單處理模式

```tsx
// components/forms/ProblemForm.tsx
'use client';

import { useState } from 'react';
import { problemsApi } from '@/lib/api/problems';

interface ProblemFormProps {
  userId: number;
  onSuccess?: () => void;
}

export function ProblemForm({ userId, onSuccess }: ProblemFormProps) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    problem_type: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await problemsApi.createProblem({
        user_id: userId,
        ...formData,
      });
      onSuccess?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create problem');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="alert alert-error">
          <span>{error}</span>
        </div>
      )}

      <div className="form-control">
        <label className="label">
          <span className="label-text">問題標題</span>
        </label>
        <input
          type="text"
          className="input input-bordered w-full"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          required
        />
      </div>

      <div className="form-control">
        <label className="label">
          <span className="label-text">描述</span>
        </label>
        <textarea
          className="textarea textarea-bordered w-full"
          rows={4}
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
        />
      </div>

      <div className="form-control">
        <label className="label">
          <span className="label-text">問題類型</span>
        </label>
        <select
          className="select select-bordered w-full"
          value={formData.problem_type}
          onChange={(e) => setFormData({ ...formData, problem_type: e.target.value })}
        >
          <option value="">選擇類型</option>
          <option value="bug">Bug</option>
          <option value="concept">概念問題</option>
          <option value="implementation">實作問題</option>
        </select>
      </div>

      <button
        type="submit"
        className="btn btn-primary w-full"
        disabled={loading}
      >
        {loading && <span className="loading loading-spinner"></span>}
        {loading ? '建立中...' : '建立問題'}
      </button>
    </form>
  );
}
```

---

## 🎨 樣式規範

### Tailwind 類別順序

推薦順序：佈局 → 尺寸 → 間距 → 外觀 → 互動

```tsx
// ✅ 推薦
<div className="flex items-center gap-4 p-4 bg-white rounded-lg shadow-md hover:shadow-lg">

// ❌ 不推薦（順序混亂）
<div className="hover:shadow-lg bg-white flex p-4 rounded-lg items-center gap-4 shadow-md">
```

### 響應式設計

```tsx
<div className="
  grid
  grid-cols-1           // 手機: 1列
  md:grid-cols-2        // 平板: 2列
  lg:grid-cols-3        // 桌面: 3列
  gap-4
">
  {/* 內容 */}
</div>
```

### 深色模式

DaisyUI 自動處理深色模式，無需額外配置。

---

## 🚀 實作檢查清單

### Phase 1: 基礎架構
- [ ] 設定環境變數 (`NEXT_PUBLIC_API_URL`)
- [ ] 建立資料夾結構
- [ ] 定義 TypeScript 型別
- [ ] 設定 API client

### Phase 2: 基礎元件
- [ ] Layout 元件 (Header, Sidebar, Footer)
- [ ] UI 元件 (Button, Card, Input, Modal)
- [ ] Feature 元件 (ProblemCard, SolutionCard, ResourceCard)

### Phase 3: 頁面開發
- [ ] 首頁 (/)
- [ ] 儀表板 (/dashboard)
- [ ] 問題列表 (/problems)
- [ ] 問題詳情 (/problems/[id])
- [ ] 新增問題 (/problems/new)
- [ ] 資源頁面 (/resources)
- [ ] 標籤管理 (/tags)

### Phase 4: 功能整合
- [ ] API 整合
- [ ] 表單驗證
- [ ] Error handling
- [ ] Loading 狀態
- [ ] 搜尋功能
- [ ] 標籤篩選

### Phase 5: 優化
- [ ] 效能優化
- [ ] SEO 設定
- [ ] 無障礙測試
- [ ] 響應式測試

---

## 📝 命名規範總結

| 類型 | 格式 | 範例 |
|------|------|------|
| 元件檔案 | PascalCase | `ProblemCard.tsx` |
| 元件名稱 | PascalCase | `function ProblemCard()` |
| Hook 檔案 | camelCase | `useProblem.ts` |
| Hook 名稱 | camelCase | `function useProblem()` |
| API 函式 | camelCase | `getProblemFull()` |
| 型別/介面 | PascalCase | `interface Problem` |
| 常數 | UPPER_SNAKE_CASE | `API_BASE_URL` |
| 資料夾 | kebab-case | `problem-list/` |

---

## 🔗 相關連結

- [DaisyUI 文件](https://daisyui.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Next.js App Router](https://nextjs.org/docs/app)
- [TypeScript](https://www.typescriptlang.org/)
- [後端 API 文件](../docs/api.md)

---

**建立日期**: 2025-12-20
**維護者**: SolveX Team
**版本**: 1.0.0
