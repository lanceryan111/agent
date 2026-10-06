# 上线后的优化计划

配置放进仓库只是开始。真正让效果超过"拍照问 App"的，是接下来几周持续把你的判断和团队经验沉淀进去。

---

## 阶段 0 — 第 1 天：装好、跑通

- [ ] 按 README 安装，清掉所有 `TODO`
- [ ] 逐项完成 README "确认真的生效了" 的检查
- [ ] `/bootstrap-knowledge` 生成 `docs/ai/`，**亲自审改**所有 `(inferred)` 内容后提交
- [ ] 把最近 3–5 次真实故障补进 `KNOWN_ISSUES.md`（凭记忆写也行）

**完成标准**：问 "orders-svc 的配置从哪来、怎么部署到 dev"，agent 直接引用 ARCHITECTURE.md 回答，而不是全仓搜索。

## 阶段 1 — 第 1–2 周：建立基线

每次用 Copilot 处理一件事，花 20 秒记一行（放在个人笔记里，不必进仓库）：

| 日期 | 任务类型 | agent | 模型 | credits（账单页） | 一次答对？ | 轮数 | 不好的地方 |
|---|---|---|---|---|---|---|---|
| 10-07 | CI 失败 | triage | Terra | 42 | 是 | 3 | — |
| 10-07 | 新接口 | planner→coder | Opus→Sonnet | 210 | 否 | 9 | 改了没让改的文件 |

两周后看三个数字：

1. **首次命中率**：triage 第一轮给出的首要假设是否正确
2. **每个已解决问题的 credits**
3. **Opus 会话占比**：超过 25% 说明 planner 用得太随意，或者 triage/coder 的上下文不够好

## 阶段 2 — 第 3–4 周：根据记录调优

| 现象 | 调整 |
|---|---|
| 同一个纠正说了两次 | 写进对应的 `*.instructions.md`（幻灯片 Principle 09） |
| 某类故障反复出现 | 新建一个 skill，带上采集脚本 |
| skill 该触发没触发 | 把你实际的说法（含中文）加进 `description` |
| agent 总在全仓乱搜 | ARCHITECTURE / REPO_MAP 缺了对应信息，补上 |
| coder 越界改文件 | 收紧 coder 的 Rules，或在 plan 里写死文件清单 |
| Terra/Sonnet 在某类任务上稳定答对 | 保持；只有它稳定失败的类别才升级模型 |
| reviewer 用 Luna 漏掉明显问题 | 换 Haiku 或 Terra 再观察一周 |
| `copilot-instructions.md` 超过 50 行 | 把非全局内容下沉到 `applyTo` instructions 或 skill |

**原则**：一次只改一处，改完观察几天，再改下一处。否则分不清是哪个改动起的作用。

## 阶段 3 — 第 2 个月：护栏与外部上下文

1. **用 hooks 把"禁止"变成确定性的拦截**。目前"不准 `kubectl apply` / `helm upgrade`"只是写在 instructions 里，模型可能不遵守。VS Code 和 Copilot 支持在工具调用前执行 hook：写一个脚本，命令里出现 `kubectl (apply|delete|edit|scale)`、`helm (upgrade|uninstall)`、或 `ansible-playbook` 且不带 `--check` 时直接拒绝。具体字段以你所在版本的 hooks 文档为准。
2. **接只读 MCP 拿仓库外的证据**（需公司批准）：
   - GitHub MCP：PR、Issue、Actions 运行信息
   - Prometheus / Grafana：让 `/optimize` 直接拿 p95 指标，不用你手贴
   - 日志平台：按 traceId 查日志
   每个 MCP 只开读权限，并且只加到需要它的 agent 的 `tools:` 里，避免所有会话都多带一堆工具定义。
3. **推广给团队**：通过 PR 合入仓库；个人偏好放到 `~/.copilot/skills/` 等个人目录，不污染仓库。

## 阶段 4 — 持续：保鲜与回归

- **每季度**：跑一次 `repo-knowledge` 的 Refresh；删掉过时的 KNOWN_ISSUES 条目
- **新模型出来时**：从 KNOWN_ISSUES 里挑 5 个已知答案的问题作为固定测试集，分别用新旧模型跑 `/triage`，对比答对率和 credits，再决定是否改 agent 的 `model:`
- **每月看一次账单**：如果 credits 突然升高，先检查是否有超长线程没用 `/handoff`，或某个 MCP / instructions 文件变大了

---

## 一页纸版：每天的习惯

1. 新问题 → 新会话（`/triage` 或 `/feature` 开头）
2. 先让脚本取证，再让模型推理
3. 默认 Terra / Sonnet；Opus 只给 planner
4. 线程超过 ~10 轮或开始绕圈 → `/handoff` → 新会话
5. 修好了 → `/known-issue`
6. 纠正第二次 → 写进 instructions
