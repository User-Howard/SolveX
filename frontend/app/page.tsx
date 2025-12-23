import Link from "next/link";
import { Header } from "@/components/layout/Header";

export default function Home() {
  return (
    <div className="min-h-screen">
      <Header />

        <main className="flex flex-col gap-16 px-4 pt-10 pb-16 max-w-6xl mx-auto">
        {/* Hero */}
        <section className="relative overflow-hidden rounded-2xl border border-base-300/60 bg-gradient-to-b from-base-200 to-base-100 shadow-xl">
         {/* animated soft gradient */}
            <div
              className="
                pointer-events-none
                absolute inset-0
                bg-gradient-to-r 
                from-blue-500/12 via-violet-500/12 to-purple-500/12
                bg-[length:200%_200%]
                animate-[gradientMove_5s_ease-in-out_infinite]
              "
            />
         
         
         
          <div className="absolute inset-0 opacity-60 [mask-image:radial-gradient(ellipse_at_top,black,transparent_55%)] bg-gradient-to-tr from-primary/20 via-secondary/10 to-accent/20" />
          <div className="relative py-14 px-10 sm:py-20 sm:px-14 text-center">
            <div className="mb-4 flex justify-center gap-2">
              <span className="badge badge-outline">問題管理</span>
              <span className="badge badge-outline">解法演進</span>
              <span className="badge badge-outline">資源整合</span>
            </div>

            <h1 className="text-4xl sm:text-5xl font-bold tracking-tight">
              SolveX
            </h1>
            <p className="mt-5 text-base sm:text-lg leading-relaxed text-base-content/80">
              程式學習者的知識管理系統
              <br />
              整合多元學習資源，解決知識碎片化問題
            </p>
            <div className="mt-8 flex flex-col gap-3 w-full max-w-sm mx-auto">
              {/* 主 CTA：瀏覽問題 */}
              <Link
                href="/problems"
                className="btn btn-primary btn-lg w-full"
              >
                瀏覽問題
              </Link>

              {/* 次 CTA：並排，合起來等於上面 */}
              <div className="flex flex-col sm:flex-row gap-3">
                <Link
                  href="/problems/new"
                  className="btn btn-outline btn-md flex-1"
                >
                  新增問題
                </Link>
                <Link
                  href="/resources"
                  className="btn btn-outline btn-md flex-1"
                >
                  看資源
                </Link>
              </div>
            </div>

          </div>
        </section>

        {/* Feature cards */}
        <section className="flex flex-col gap-8">
          {/* Section header */}
          <div className="flex flex-col items-center text-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">核心功能</h2>
            <p className="text-sm text-base-content/70">
              用一套系統，把你的卡關與解法整理成可回顧的知識庫
            </p>
          </div>

          {/* Cards */}
            <div className="flex flex-col md:flex-row gap-6">
              {[
                {
                  title: "問題管理",
                  desc: "記錄與追蹤程式學習過程中遇到的問題",
                  href: "/problems",
                },
                {
                  title: "解法追蹤",
                  desc: "管理多種解法，理解自己怎麼一步步想通",
                  href: "/problems",
                },
                {
                  title: "資源整合",
                  desc: "集中管理文章、影片與外部學習資源",
                  href: "/resources",
                },
              ].map((x) => (
                <Link
                  key={x.title}
                  href={x.href}
                  className="
                    flex-1
                    group
                    rounded-2xl
                    border border-base-300/60
                    bg-base-100
                    shadow-sm
                    transition
                    cursor-pointer
                    hover:-translate-y-0.5
                    hover:shadow-lg
                    hover:ring-2 hover:ring-primary/20
                    focus-visible:outline-none
                    focus-visible:ring-2 focus-visible:ring-primary/40
                  "
                >
                  <div className="flex h-full flex-col p-6">
                    <h3 className="text-lg font-semibold tracking-tight group-hover:text-primary transition">
                      {x.title}
                    </h3>
                    <p className="mt-2 text-sm leading-relaxed text-base-content/75">
                      {x.desc}
                    </p>
                  </div>
                </Link>
              ))}
            </div>
        </section>

        {/* Info */}
        <section>
          <div className="rounded-2xl border border-info/30 bg-info/10 px-5 py-4 text-sm text-base-content/80">
            這是一個簡潔的 prototype，展示 SolveX 的核心功能
          </div>
        </section>
      </main>
    </div>
  );
}
