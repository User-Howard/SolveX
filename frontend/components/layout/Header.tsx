import Link from 'next/link';

export function Header() {
  return (
<div className="navbar min-h-12 h-12 bg-base-200 shadow-sm px-2">
      <div className="navbar-start">
        <Link href="/" className="btn btn-ghost btn-sm text-lg font-bold tracking-tight">
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
      <div className="navbar-end">
        <div className="dropdown dropdown-end">
  <button
    tabIndex={0}
    className="btn btn-ghost btn-circle hover:bg-base-200/80"
    aria-label="Open menu"
  >
    {/* hamburger icon */}
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  </button>

  {/* 下拉內容 */}
  <ul
    tabIndex={0}
    className="
      dropdown-content z-[50] mt-3 w-56
      rounded-2xl border border-base-300/60
      bg-base-100/95 backdrop-blur
      p-2 shadow-lg
    "
  >
    <li className="px-2 py-2 text-xs font-semibold text-base-content/60">
      快速導覽
    </li>

    <li>
      <Link
        href="/problems"
        className="flex items-center gap-2 rounded-xl px-3 py-2 hover:bg-base-200/70 transition"
      >
        <span className="text-sm"></span>
        <span className="text-sm font-medium">瀏覽問題</span>
      </Link>
    </li>

    <li>
      <Link
        href="/problems/new"
        className="flex items-center gap-2 rounded-xl px-3 py-2 hover:bg-base-200/70 transition"
      >
        <span className="text-sm"></span>
        <span className="text-sm font-medium">新增問題</span>
      </Link>
    </li>

    <li>
      <Link
        href="/resources"
        className="flex items-center gap-2 rounded-xl px-3 py-2 hover:bg-base-200/70 transition"
      >
        <span className="text-sm"></span>
        <span className="text-sm font-medium">看資源</span>
      </Link>
    </li>

    <div className="my-2 h-px bg-base-300/60" />

    
  </ul>
</div>
      </div>
    </div>
  );
}

