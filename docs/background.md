Section 1: Project Description (50%)
Finalize your project idea and describe your proposed database application. You may select one idea from Milestone 1 or propose a new concept.
Application Description (25%)
Domain (3%): Identify the general domain area of your application.
教育科技/個人知識管理

Problem Statement (10%): Describe the specific problem your application solves in one clear paragraph.
What pain point or need does it address?
在程式學習過程中，學習者經常需要查閱來自不同平台（如 Stack Overflow、官方文件、教學部落格等）的解答，資訊分散且缺乏整合，導致知識碎片化、重複搜尋與難以系統化整理的問題。我們的應用旨在解決此痛點，協助使用者集中管理學習資源，並建立可追蹤的知識脈絡。
Who are the intended users?
我們自身作為程式學習者，體會到知識分散帶來的低效率與挫折。我們希望透過此專案整合多元知識來源，讓學習過程更順暢，並嘗試探索資料庫技術在教育科技領域的實際應用。

Why is a database necessary for this application?
使用資料庫可有效管理使用者、文章、問題及關聯資料，支援搜尋與追蹤功能。
Database-Relevant Functions (9%)
List 3-5 core functions that require database operations.
(Examples: "Search courses by department and semester," "Track student enrollment history," "Generate grade reports". Be specific about what data is queried, inserted, updated, or deleted.)

    1.	搜尋問題、解答與標籤（SELECT）

　使用者可以依照關鍵字或標籤搜尋程式問題與解法。
　此功能會根據 Problems、Solutions 與 Tags 三個資料表進行關聯查詢（透過 has_tags、has_solutions 關係），以找出對應的內容與相關主題。2. 記錄與更新使用者學習活動（INSERT / UPDATE）
　當使用者建立新問題或新增解法時，系統會在 Problems 或 Solutions 資料表中插入新紀錄，並透過 creates 關係連結到該使用者。
　此外，系統也可更新資料，例如修改問題的解決狀態 (resolved) 或更新解法的成功率 (success_rate)。3. 管理解法版本與演進歷史（INSERT / UPDATE）
　每個解法可能隨時間改進並形成新版本。
　系統利用 evolve_from 關係儲存不同版本之間的關聯，並記錄 version_number 與 improvement_description，以追蹤解法的演進過程。4. 儲存與管理外部學習資源（INSERT / UPDATE / DELETE）
　使用者在撰寫解法時可引用多個外部資源（透過 refer 關係連結至 Resources）。
　資料庫需支援新增新資源、更新其效用評分 (usefulness_score) 或瀏覽次數 (visit_count)，以及刪除無效或過期的連結。5. 標籤建立與推薦（SELECT / INSERT）
　在使用者新增問題或解法時，系統可查詢既有標籤或自動建立新標籤 (Tags)。
　同時，根據標籤的分類 (category) 與使用頻率，系統能推薦常見或相關標籤，以協助知識組織。
Motivation (3%)
Explain why your team is interested in building this application (2-3 sentences).
我們作為程式學習者，深感資料分散帶來的不便。我們希望透過此專案整合知識來源，改善學習體驗，並嘗試將資料庫結合於教育科技中。
