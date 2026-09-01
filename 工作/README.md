这个问题不用建文件，直接给你一套实战打法。结合 2026 年这两个工具的最新能力，核心思想是：**别把它们当"自动补全"和"聊天框"用，要把它们当 agent 用**。大多数人只用到了两成能力。

## VS Code Copilot：从补全升级到 Agent

**1. 主力用 Agent 模式，不是 Tab 补全。** Chat 面板切到 Agent 模式后，它能自己读整个代码库、改多个文件、跑终端命令、看报错再自我修正。正确姿势是给它一个完整任务（"把这个模块的错误处理重构成统一的 exception，改完跑一遍测试"）然后审查结果，而不是一行行等补全。

**2. 模型选择器里挑最强的模型。** Copilot 现在内置多家模型（Claude、GPT、Gemini 系列），公司订阅允许的话，复杂任务手动切到最强的推理模型，简单补全用快的。很多人从不碰这个下拉框，白白用默认模型。

**3. 写一份 `.github/copilot-instructions.md`。** 这是投入产出比最高的一件事：把你们项目的技术栈、代码规范、目录结构、"永远不要做什么"写进去，Copilot 每次回答都会自动带上这些上下文，从此不用每次重复解释背景。

**4. 用 Prompt Files（`.prompt.md`）固化重复任务。** 你每天重复的操作——生成单元测试、写 PR 描述、按固定模板做 code review——写成提示词文件存在仓库里，之后一条斜杠命令调用。这相当于给自己造"技能"。

**5. 喂对上下文。** 用 `#codebase` 让它搜全库、`#file` 指定文件、直接把终端报错和截图拖进聊天框。回答质量的差距 80% 来自上下文给没给够。

**6. MCP 服务器（如果公司政策允许）。** VS Code 的 Copilot 支持接 MCP，可以把内部数据库、Jira、内部 API 接进来，agent 就能直接查工单、读表结构来干活。

**7. 别只用它写"工作代码"。** 你不是程序员的部分工作也能受益：让它写 Python/PowerShell 脚本批量处理文件、清洗 Excel 数据、写正则、写 SQL——就像我们上一步给你 Mac 写的股票脚本一样，公司里的重复杂活都可以让 Copilot 写脚本自动化掉。

## M365 Copilot：把它当有权限读你全部工作数据的助理

它最大的优势不是写作，而是**它能读你的邮件、日历、Teams 消息和 SharePoint 文档**（Microsoft Graph），这是任何外部 AI 做不到的。

**1. 每天从 Copilot Chat（工作模式）开始。** "总结我昨天下班后的未读邮件和 Teams 消息，按需要我行动的优先级排序""我今天的会议各需要准备什么"——这一条习惯每天省半小时。

**2. 会议全交给它。** 开着转录，会后让它出摘要和行动项；没参加的会直接问"这个会上关于 X 的决定是什么，谁负责"。Teams 长消息串也让它先总结再看。

**3. 用"引用文档"的方式写东西。** 在 Word/PPT 里起草时用 `/` 引用已有文件："基于这份需求文档和上季度的汇报 PPT，生成新一季的汇报框架"。Word 文档可以一键转 PPT 初稿。

**4. Excel 里用高级分析。** 让它找趋势、生成透视表、写公式，复杂分析它会在后台跑 Python。你贴一堆数据问"哪个产品线环比异常"比自己拉表快得多。

**5. 用 Scheduled Prompts 做自动化。** 和你在 Mac 上做的股票 agent 同一个思路：设定每天早上自动运行"汇总我今天的会议和待办邮件"这类提示词，定时推给你。

**6. 试试内置 Agent 和自建 Agent。** Researcher（深度研究）、Analyst（数据分析）这两个内置 agent 处理复杂任务比普通聊天强很多；如果公司开了 Copilot Studio / Agent Builder，可以把你的固定流程（比如周报生成）做成自己的 agent 给团队用。

## 两者怎么配合

分工原则：**涉及邮件、会议、公司文档的事给 M365 Copilot（因为只有它有权限）；涉及文件处理、数据、任何可以脚本化的事给 VS Code Copilot（因为它能真正执行代码）。** 中间地带——比如"把 SharePoint 上导出的数据批量清洗"——用 M365 拿数据，VS Code 写脚本处理。最后提醒一句：这两个都在公司合规边界内，内部数据尽量留在这两个工具里处理，别贴到外部 AI 去。

想更进一步的话，我可以帮你写一份可以直接放进公司仓库的 `copilot-instructions.md` 模板，或者一组常用 `.prompt.md` 提示词文件——告诉我你的具体岗位和日常工作内容就行。

Sources: [GitHub Copilot Agent Mode in VS Code: Full Guide (2026)](https://lucaberton.com/blog/github-copilot-agent-mode-vscode-complete-guide/), [GitHub Copilot Agent Mode and MCP in VS Code: 2026 Guide](https://www.itechguides.com/vibe-coding-with-github-copilot-agent-mode-and-mcp-in-vs-code-updated-for-2026/), [20 Microsoft Copilot Tips and Tricks for 2026](https://reflectiveit.com/blog/microsoft-copilot-tips-and-tricks/), [What's New in Microsoft 365 Copilot | January 2026](https://techcommunity.microsoft.com/blog/microsoft365copilotblog/what%E2%80%99s-new-in-microsoft-365-copilot--january-2026/4488916)
