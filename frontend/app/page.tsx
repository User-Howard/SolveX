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
                animate-[gradientMove_4s_ease-in-out_infinite]
              "
            />
         
         
         
          <div className="absolute inset-0 opacity-60 [mask-image:radial-gradient(ellipse_at_top,black,transparent_55%)] bg-gradient-to-tr from-primary/20 via-secondary/10 to-accent/20" />
          <div className="relative py-14 px-10 sm:py-20 sm:px-14 text-center">
            <div className="mb-4 flex justify-center gap-2">
              <span className="badge badge-outline">問題管理</span>
              <span className="badge badge-outline">解法演進</span>
              <span className="badge badge-outline">資源整合</span>
            </div>

              <h1
                className="
                  relative mt-3
                  text-5xl sm:text-6xl lg:text-7xl
                  font-black tracking-tight
                  text-[#0b1f3a]
                  drop-shadow-[0_10px_24px_rgba(3,18,38,0.45)]
                "
              >
                <span
                  className="
                    text-transparent bg-clip-text
                    bg-gradient-to-r
                    from-[#07162b]
                  via-[#183d73]
                    to-[#07162b]
                    bg-[length:300%_100%]
                    animate-[deepBlueFlow_6s_linear_infinite]
                  "
                >
                  SolveX
                </span>
              </h1>
            <p className="mt-5 text-base sm:text-lg leading-relaxed text-base-content/80">
              程式學習者的知識管理系統
              <br />
              整合多元學習資源，整理碎片化知識
            </p>
            <div className="mt-8 flex flex-col gap-3 w-full max-w-sm mx-auto">
           <Link
                  href="/problems"
                  className="
                    btn btn-primary btn-lg w-full
                    relative overflow-hidden
                    transition-all duration-300
                    hover:scale-[1.02]
                    hover:brightness-110
                    hover:shadow-[0_0_18px_rgba(59,130,246,0.55),0_0_36px_rgba(168,85,247,0.35)]
                    active:scale-[0.99]

                    before:pointer-events-none
                    before:absolute
                    before:inset-y-0
                    before:left-[-120%]
                    before:w-[120%]
                    before:bg-gradient-to-r
                    before:from-transparent
                    before:via-white/35
                    before:to-transparent
                    before:skew-x-[-20deg]

                    hover:before:left-[120%]
                    before:transition-all
                    before:duration-700
                    before:ease-out
                  "
                >
                  立即瀏覽問題
                </Link>

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

        <section className="flex flex-col gap-8">
          <div className="flex flex-col items-center text-center gap-2">
            <h2 className="text-2xl font-bold tracking-tight">核心功能</h2>
            <p className="text-sm text-base-content/70">
              用一套系統，把你的卡關與解法整理成可回顧的知識庫
            </p>
          </div>

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

        <section>
          <div className="rounded-2xl border border-info/30 bg-info/10 px-5 py-4 text-sm text-base-content/80">
            這是一個簡潔的 prototype，展示 SolveX 的核心功能
          </div>
        </section>
      </main>
    </div>
  );
}
