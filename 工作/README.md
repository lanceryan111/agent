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


这个组合其实能覆盖你日常工作的大部分场景——VS Code Copilot 管代码,M365 Copilot 管文档、邮件、会议。下面按工具说说最值得养成的用法。

## VS Code Copilot:别只用它补全代码

大多数人只用了灰色的行内补全,那只是它能力的 10%。真正提效的是这些:

**用 Chat 的不同模式干不同的活**

- 行内对话(选中代码按 `Ctrl+I`):就地改代码,比如"把这段改成异步"、"加上错误处理"。改动直接以 diff 形式出现,接受或拒绝即可。
- Chat 面板里切到 **Agent / Edits 模式**:这是现在最强的功能,可以让它跨多个文件自动完成一个任务,比如"给这个模块加单元测试"、"把配置从 JSON 迁移到 YAML",它会自己找文件、改文件、跑命令。
- `@workspace` 提问:"这个项目里登录逻辑在哪实现的?"——接手陌生代码库时极其省时间。`@terminal` 可以解释报错,`/explain`、`/fix`、`/tests` 这些斜杠命令也值得记住。

**给它写"说明书",一次配置长期受益**

在仓库根目录建一个 `.github/copilot-instructions.md`,写上你们团队的代码规范、常用框架、命名习惯。之后每次对话它都会自动遵守,你不用反复交代"我们用的是 Vue 3 组合式 API"之类的背景。

**喂对上下文比写好提示词更重要**

Copilot 主要看你打开的文件和你用 `#file` 引用的内容。让它写代码前,把相关的类型定义、类似的已有实现打开或引用进去,质量会有肉眼可见的提升。

**顺手的小功能**:提交时点一下魔棒图标自动生成 commit message;右上角可以切换模型(通常有 GPT 和 Claude 可选),复杂重构任务用推理更强的模型效果更好。

## M365 Copilot:把它当作"能读你全部工作数据的助理"

它最大的价值不是帮你写东西,而是它接入了你的邮件、日历、Teams 聊天和 SharePoint 文件(Microsoft Graph)。所以最有用的是**检索和汇总类**的问题:

- 每天早上在 Copilot Chat(选"工作"模式)问:"总结我昨天下班后收到的重要邮件,按需要我回复的优先级排序"
- 开会前:"我下午 3 点和 XX 的会,帮我准备:相关的邮件往来、上次会议纪要、还没关闭的行动项"
- 找东西:"上个月谁给我发过关于预算的那个 Excel?"——比自己翻邮件快得多

**各个应用里的高价值场景**:

- **Teams 会议**:开启转录后,迟到或没参加的会可以直接问"我错过了什么?有什么行动项分给我?"这是很多人公认 M365 Copilot 最值钱的功能。
- **Outlook**:长邮件串点"摘要",一秒抓住重点;写回复时让它起草再自己改。
- **Word → PowerPoint**:先在 Word 里把内容写好(用清晰的标题结构),然后在 PPT 里让 Copilot 基于这个 Word 文档生成幻灯片,比从零让它做 PPT 效果好很多。
- **Excel**:数据先格式化成"表格"(Ctrl+T),然后用自然语言让它加公式列、做透视分析、找异常值。

**提示词公式**:目标 + 背景 + 数据来源 + 输出要求。比如不说"写个邮件",而说"给客户 X 写一封跟进邮件,基于上周四的会议纪要,语气正式,不超过 150 字,结尾约下周通话"。

## 两个通用心法

一是**让 AI 出初稿,你做编辑**——审阅修改永远比从零创作快,这是这两个工具提效的本质。二是**别一句话怼过去就期待完美结果**,把它当实习生:先给背景,看初稿,再说"第二段展开一点"、"用词太正式了"迭代两三轮,质量远好于一次性长提示。

另外提醒一句:具体功能会因公司购买的许可证和 IT 管理员的设置而不同(比如 Agent 模式、模型选择、Teams 转录可能被关闭),如果发现某个功能没有,可以找 IT 确认是否启用。想深入的话,M365 Copilot 里自带的 Copilot 提示词库(Prompt Gallery)和 VS Code 文档里的 Copilot customization 章节都值得翻一翻。
