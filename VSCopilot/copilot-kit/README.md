# Copilot DevOps Kit（Java / Spring Boot / K8s / Ansible / GitHub Actions）

给 VS Code Copilot（1.137）用的一套仓库级配置：排错、写代码、部署后优化，同时按幻灯片里的原则控制 AI credit 消耗。

> 面向模型的文件（instructions / agents / skills / prompts）都用英文写：始终加载的内容用英文 token 更少、团队也能共用。说明文档用中文。

---

## 1. 安装（10 分钟）

1. 把 `.github/` 和 `docs/ai/` 复制到仓库根目录（已有 `.github/copilot-instructions.md` 的话手工合并）。
2. 给脚本加执行权限：`chmod +x .github/skills/*/scripts/*.sh`
3. 改掉所有 `TODO`：`grep -rn TODO .github docs/ai`
   - `copilot-instructions.md` 的仓库描述
   - `kubernetes.instructions.md` / `ansible.instructions.md` 的 `applyTo` 路径，改成你仓库的真实目录
4. 本地工具（脚本会用到，缺的就跳过对应功能）：`gh`（已 `gh auth login`）、`kubectl`、`helm`、`kubeconform`、`ansible-lint`、`actionlint`
5. 打开 VS Code → Chat → 跑一次 `/bootstrap-knowledge`，审核生成的 `docs/ai/*.md` 后提交。**这是整套配置最值钱的一步。**

## 2. 确认真的生效了

| 检查 | 怎么看 |
|---|---|
| 全局 instructions | 随便问一句，展开回答上方的 References，应包含 `copilot-instructions.md` |
| 按文件 instructions | 打开一个 `.java` 文件再提问，References 里应出现 `java-spring.instructions.md` |
| Custom agents | Chat 输入框的 agent 选择器里能看到 triage / planner / coder / reviewer |
| Skills | 对 triage 说"CI 挂了"，应看到它读取 `ci-failure-triage/SKILL.md` 并运行脚本 |
| Prompt files | 输入 `/` 能看到 triage、feature、handoff、optimize 等 |
| 模型 | 切换到某个 agent 后看模型选择器显示的是不是 `model:` 里写的模型。名字必须和模型选择器里显示的完全一致，且是组织已启用的模型；不一致就照着选择器里的名字改 |
| 工具名 | agent 的 `tools:` 用的是工具集名（read/search/edit/execute/web/todo）。如果某个 agent 跑不了命令或改不了文件，用 Chat 里的工具配置界面重新勾选，以界面显示的名字为准 |

Skill 没触发：最常见原因是你说的话和 `description:` 里的关键词对不上——把你习惯的说法（包括中文，如"流水线挂了"、"pod 起不来"）加进 description。

## 3. 文件一览

```
.github/
├── copilot-instructions.md            # 始终加载：仓库是什么、工作方式、硬性禁区（≤40 行）
├── instructions/                       # 打开对应文件时才加载
│   ├── java-spring.instructions.md     #   **/*.java
│   ├── java-tests.instructions.md      #   **/src/test/**
│   ├── kubernetes.instructions.md      #   k8s/helm/charts/deploy/...
│   ├── ansible.instructions.md         #   ansible/playbooks/roles/inventories
│   └── github-actions.instructions.md  #   .github/workflows/**
├── agents/
│   ├── triage.agent.md     # 排错，只读，可跑诊断命令 → 交接给 coder / planner
│   ├── planner.agent.md    # 设计/复杂问题，只读，最强模型 → 交接给 coder
│   ├── coder.agent.md      # 有界实现：限定文件、窄测试、失败两次就停 → 交接给 reviewer
│   └── reviewer.agent.md   # 提交前审查 git diff，便宜模型
├── skills/                 # 按需加载，脚本替代 agent 的盲目探索
│   ├── ci-failure-triage/          gh 只取失败 step 的日志尾部
│   ├── k8s-pod-debug/              一次性 pod 快照：状态/describe/events/前后日志/用量
│   ├── spring-boot-startup-debug/  抽取 FAILED TO START、最深 Caused by、profile
│   ├── ansible-debug/              syntax-check → lint → 单主机 --check --diff
│   ├── java-test-runner/           Maven/Gradle 自动识别，只输出失败摘要
│   ├── repo-knowledge/             生成/刷新 docs/ai 知识包
│   └── post-deploy-review/         部署后评审 → 排好优先级的优化清单
└── prompts/                # /命令
    ├── triage.prompt.md            /triage   结构化提问（相当于"拍照"）
    ├── feature.prompt.md           /feature  新功能先出计划
    ├── optimize.prompt.md          /optimize 部署后优化评审
    ├── handoff.prompt.md           /handoff  压缩线程，换新会话
    ├── known-issue.prompt.md       /known-issue 解决后记入知识库
    └── bootstrap-knowledge.prompt.md
docs/ai/
├── ARCHITECTURE.md   # 服务、环境、部署流、配置来源
├── REPO_MAP.md       # 目录 → 用途 → 入口文件
└── KNOWN_ISSUES.md   # 排障记忆，越用越准
```

## 4. 日常三条工作流

**排错**
`/triage` → triage 跑 skill 脚本拿证据 → 给出排序的假设 + 验证命令 → 你确认 → 点 **Fix it** 交接给 coder → `/known-issue` 记录。
难题点 **Escalate** 交给 planner（只有这时才花 Opus 的钱）。

**写代码**
`/feature` → planner 出分步计划（每步带验证命令）→ 点 **Implement step 1** → coder 改代码 + 跑窄测试 → 点 **Review diff** → reviewer 审查 → 下一步开**新会话**再交给 coder。
小改动直接选 coder，不必经过 planner。

**部署后优化**
`/optimize` → 拿 pod 快照 + 你贴的监控指标 + 最近 CI 运行 → 输出影响/成本排序的优化表 → 前 3 项交给 `/feature` 进入计划。

## 5. 模型路由与 credit 预算

价格来自 GitHub 官方定价页（每 100 万 token，1 credit = $0.01）：

| 模型 | 输入 | 缓存输入 | 输出 | 本套配置用在 |
|---|---|---|---|---|
| Claude Opus 4.8 | $5.00 | $0.50 | $25.00 | planner |
| Claude Opus 5.5 | $4.00 | $0.20 | $20.00 | *若组织已启用，可替换 Opus 4.8：更便宜* |
| GPT-5.6 Sol | $4.00 | $0.40 | $20.00 | planner 备选 |
| Claude Sonnet 5.5 | $2.00 | $0.20 | $10.00 | coder |
| GPT-5.6 Terra | $2.00 | $0.20 | $12.00 | triage |
| GPT-5.6 Luna | $0.20 | $0.02 | $1.20 | reviewer、/handoff |
| Claude Haiku 4.5 | $1.00 | $0.10 | $5.00 | reviewer 备选 |

⚠️ "GPT-5.6" 有 Luna / Terra / Sol 三档，输出价格相差约 17 倍——在模型选择器里确认你平时用的是哪一档。

**一个典型 agent 会话的大概花费**（假设累计 40 万输入 token、其中 75% 命中缓存、2.5 万输出）：

| 模型 | 约 credits / 会话 |
|---|---|
| Opus 4.8 | ~140 |
| Sonnet 5.5 / GPT-5.6 Terra | ~55–60 |
| GPT-5.6 Luna | ~6 |

这只是数量级估算，以账单页实际数字为准。结论：**同样的会话，Opus 约是 Sonnet/Terra 的 2.5 倍、Luna 的 20 倍以上**；而上下文越乱、线程越长，输入 token 越多——所以 skill 脚本和 `/handoff` 省下的往往比换模型还多。

**50,000 credits 的建议分配**（≈ $500；如果这是团队共享池，按人数折算）：

| 用途 | 占比 | 说明 |
|---|---|---|
| 日常排错 + 编码（triage / coder） | 60% | Terra / Sonnet |
| 规划与疑难问题（planner） | 25% | 只在跨模块、架构、证据不足时 |
| 知识包生成与刷新 | 10% | 一次性投入，长期复用 |
| 缓冲 | 5% | |

如果你在 GitHub 的 billing 设置里能设置预算告警，把告警设在 50% / 80%。

详细的上线后优化步骤见 [ROADMAP.md](ROADMAP.md)。
