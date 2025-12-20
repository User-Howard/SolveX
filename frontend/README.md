# SolveX Frontend

SolveX 前端應用程式，使用 Next.js 16 + React 19 + TypeScript + Tailwind 4 + DaisyUI 5 建構。

## 功能特色

- ✅ 問題列表頁面 - 瀏覽與搜尋問題
- ✅ 問題詳情頁面 - 查看問題、解法與相關資源
- ✅ 響應式設計 - 支援手機、平板、桌面
- ✅ 深色模式支援 - 自動適配系統主題
- ✅ DaisyUI 元件 - 使用現代化的 UI 元件庫

## 技術棧

- **框架**: Next.js 16 (App Router)
- **UI 庫**: React 19
- **樣式**: Tailwind CSS 4 + DaisyUI 5
- **語言**: TypeScript
- **API**: 連接到 FastAPI 後端 (http://localhost:8000)

## 開始使用

### 安裝依賴

```bash
npm install
```

### 開發模式

```bash
npm run dev
```

應用程式將在 http://localhost:3000 啟動

### 建置

```bash
npm run build
npm start
```

## 環境變數

建立 `.env.local` 檔案（可選）：

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 專案結構

```
frontend/
├── app/                    # Next.js App Router 頁面
│   ├── problems/          # 問題相關頁面
│   ├── resources/         # 資源頁面
│   ├── layout.tsx         # 根布局
│   ├── page.tsx           # 首頁
│   └── globals.css        # 全域樣式
├── components/            # React 元件
│   ├── layout/           # 布局元件
│   └── features/         # 功能元件
├── lib/                  # 工具函式
│   └── api/             # API 客戶端
└── types/               # TypeScript 型別定義
```

## 頁面說明

### 首頁 (/)
- 展示 SolveX 的介紹與核心功能
- 快速導航連結

### 問題列表 (/problems)
- 顯示所有問題
- 搜尋功能
- 響應式卡片佈局

### 問題詳情 (/problems/[id])
- 顯示問題完整資訊
- 解法列表
- 相關資源
- 標記為已解決功能

## 設計規範

遵循 `docs/STYLE_GUIDE.md` 中的設計規範，使用 DaisyUI 元件與 Tailwind CSS 工具類別。

## 開發注意事項

1. 所有頁面元件使用 `'use client'` 因為需要互動功能
2. API 呼叫使用 `lib/api` 中的客戶端函式
3. 型別定義在 `types/models.ts`
4. 遵循 DaisyUI 5 的類別命名規範
