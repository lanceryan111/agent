# Copilot DevOps v2：开发、排障与优化

适用技术栈：Java、Spring Boot、Kubernetes、Ansible、GitHub Actions。根据用户所述 VS Code 1.137 环境设计；未在用户公司的 VS Code、Copilot 扩展、策略或真实仓库中验证。公开文档为当前版本文档，不能保证所有 UI 和配置在公司安装版本完全一致。

## 使用方式

1. 在公司仓库中新建工作分支，将本包的 `.github` 与 `docs/ai` 内容合并进去。保留已有组织/仓库要求；不要覆盖现有同名文件。按真实目录调整各 instructions 的 applyTo，尤其 Kubernetes/Ansible 路径。
2. 用一次受限的仓库探索补齐 `docs/ai/repo-map.md`：只查服务入口、部署链路、配置来源、工具版本和验证命令；每项带路径证据。不清楚的项保留未验证。
3. 在 Copilot 会话的 Customizations 界面确认 instructions、agent、skills 可见。新建测试会话，检查 References 和工具调用，确认规则被实际使用。诊断类只读任务不一定靠 applyTo 自动触发，必要时显式附加相关 instructions。
4. `DevOps Diagnose` 配置了 read/search 工具组，没有终端和编辑工具。检查本机工具选择器是否识别这两个工具组，并检查最终有效工具权限。它只能分析仓库和已提供证据，不能自动取得集群/Actions 运行状态。
5. 写功能、改配置或修复时选择 `DevOps Build`，配置的工具为 read/search/edit/execute；先确认本机有效工具与权限，再使用。它会读取相关实现、修改代码并运行验证。`DevOps Review` 只读评审，`DevOps Optimize` 只读制定优化计划。本包不设置自动批准、生产凭据或 MCP。
6. 模型没有写死：使用公司模型选择器中的精确名称与价格。GPT 5.6 的完整变体、Opus 是否 fast mode 都会影响价格。

## Settings 检查

若使用 Local agent 且本机识别对应设置，检查：

```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "chat.includeApplyingInstructions": true,
  "chat.useAgentSkills": true
}
```

这些在当前文档中默认开启。不要为了本包替换整个 settings.json。不同 harness/session target 的发现规则不同，Customizations 实际发现情况更重要。

若本机提供 agent 最大请求次数，可设置适合小任务的上限作为循环限制；它不等于工具调用数、token 数或 credits 硬上限。本包不依赖未核实版本适用性的设置键。

## 日常使用

- 新功能/重构/测试：选择 Build，使用 [开发任务模板](docs/ai/feature-template.md)，按需调用 feature-delivery。
- 复杂变更评审：选择 Review，附任务标准和 diff；该角色不执行测试。
- 配置落地后的改进：按 [优化计划](docs/ai/rollout-optimization-plan.md) 执行，并记录 [评估表](docs/ai/evaluation-template.md)。
- 应用上线后优化：选择 Optimize，使用 post-deploy-review，先有基线再提改动。
- 简单日志解释/局部问答：附精简证据，用能满足质量要求的较低成本模型。
- 跨配置链路的故障：部署排障 skill + 必要读工具；根据实际难度使用强模型。
- 根因清楚后修复：给出范围和验收标准，使用修复验证 skill。
- 新故障开新会话；同一故障仍在有效推进则保留会话。出现漂移时用 handoff 模板交接，避免丢弃证据后重复扫描。
- 常规 grep、测试和日志筛选优先复用已有命令/脚本；agent 发起和解释工具调用仍可能消耗模型 token。
- instructions 复用减少重复编写与遗漏，但不意味着上下文免费；缓存命中及费用以平台统计为准。

## 对应三张图的原则

| 图中原则 | 落地方式 |
|---|---|
| 新话题新会话 | incident 与 handoff 模板 |
| 匹配模式/模型 | 简单问答、取证、修复分开选择；模型不写死 |
| 复用规则 | 短全局规则 + 四组按需规则 |
| 本地工具优先 | 复用 build wrapper、测试和证据采集入口 |
| 精确上下文 | repo-map 导航、明确故障身份和错误 |
| 先计划再执行 | 复杂修复先诊断/给范围；不强制小任务都换会话 |
| 尽早验证 | failure-regression 按故障边界选择检查 |
| 压缩交接 | handoff 保留证据、反证、工作区状态 |
| 纠正变规则 | 仅固化可复用、已验证的经验 |
| 有界自主执行 | 两次无新证据重新评估 + 明确完成标准 |
| 判断处用强模型 | 跨层诊断/复杂修复才升级；按结果成本比较 |

## 验证与额度评估

选 5 个已知根因的历史案例（如 Spring 配置覆盖、K8s 健康检查、Ansible 变量覆盖、Actions 可复用工作流、Java 测试失败）。相同起始证据、模型和仓库版本，对比默认配置与本包；在隔离会话/工作区中运行，适当重复。
记录：根因准确性、验证是否有效、人工纠正次数、耗时、credits，以及可见的输入/缓存/输出 token。先验证上下文改进，再比较模型。
50,000 AI credits 的公开计价等值为 500 USD；它是否为个人月度额度、剩余额度或共享预算，需要由实际页面说明确认。不要据此推算个人账单或每月可完成任务数。

## 校验边界

本包提供配置和流程模板，不包含公司架构、已验证测试命令或真实生产操作。静态结构校验不能证明真实排障效果。先用一个历史故障确认文件发现、规则应用和工具权限，再推广。

## 参考资料（2026-10-05 查询）

- [VS Code instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
- [VS Code skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [VS Code context](https://code.visualstudio.com/docs/agents/reference/workspace-context)
- [VS Code credit optimization](https://code.visualstudio.com/docs/agents/guides/optimize-usage)
- [GitHub model pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing)
- [Usage billing announcement: June 1, 2026](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/)
- [Spring Boot configuration](https://docs.spring.io/spring-boot/reference/features/external-config.html)
- [Ansible check mode limitations](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_checkmode.html)

## v2 的角色与技能

| 角色 | 工具 | 典型任务 |
|---|---|---|
| DevOps Build | read/search/edit/execute | 新功能、重构、测试、pipeline/配置修改 |
| DevOps Diagnose | read/search | 排障分析、解释现有证据 |
| DevOps Review | read/search | 根据需求和 diff 查实际缺陷 |
| DevOps Optimize | read/search | Copilot 或应用部署后的优化计划 |

四个角色由用户按需选择，不是自动并行的多 agent 编排。普通开发通常只用 Build 即可。强模型与低成本模型的选择依据实际评估，文件没有写死模型标识。

新增技能 feature-delivery 与 post-deploy-review；保留 deployment-triage 与 failure-regression。除全局短规则外，技能按任务加载。Build 拥有终端工具不等于只能运行测试，工具权限仍须在公司环境核对。

若已有上一版：在工作分支比较并合并，不要覆盖自己补充的仓库地图或组织规则。v2 保留了上一版排障能力。
