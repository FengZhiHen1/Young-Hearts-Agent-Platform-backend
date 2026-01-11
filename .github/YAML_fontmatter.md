# 提示文件（.prompt.md）的头部

|字段|描述|
|---|---|
|description|对提示的简短描述。|
|name|提示的名称，在聊天中键入 / 后使用。如果未指定，则使用文件名。|
|argument-hint|在聊天输入字段中显示的可选提示文本，用于指导用户如何与提示进行交互。|
|agent|用于运行提示的代理：ask、edit、agent，或 自定义代理 的名称。默认情况下，使用当前代理。如果指定了工具且当前代理为 ask 或 edit，则默认代理为 agent。|
|model|运行提示时使用的语言模型。如果未指定，则使用模型选择器中当前选定的模型。|
|tools|可用于此提示的工具或工具集名称列表。可以包括内置工具、工具集、MCP 工具或扩展程序提供的工具。要包含 MCP 服务器的所有工具，请使用 <server name>/* 格式。|

## 示例

```markdown
---
agent: 'agent'
model: GPT-4o
tools: ['githubRepo', 'search/codebase']
description: 'Generate a new React form component'
---
```

# 自定义代理文件（.agent.md）的头部

|字段|描述|
|---|---|
|描述|自定义代理的简短描述，显示为聊天输入字段中的占位符文本。|
|name|自定义代理的名称。如果未指定，则使用文件名。|
|argument-hint|显示在聊天输入字段中以指导用户如何与自定义代理交互的可选提示文本。|
|tools|可用于此自定义代理的工具或工具集名称列表。可以包括内置工具、工具集、MCP 工具或扩展提供的工具。要包含 MCP 服务器的所有工具，请使用 <server name>/* 格式。|
|model|运行提示时使用的 AI 模型。如果未指定，则使用模型选择器中当前选择的模型。|
|infer|可选的布尔标志，用于启用将自定义代理用作子代理（默认值为 true）。|
|target|自定义代理的目标环境或上下文（vscode 或 github-copilot）。|
|mcp-servers|可选的模型上下文协议 (MCP) 服务器配置 json 列表，用于与GitHub Copilot 中的自定义代理一起使用（目标：github-copilot）。|
|handoffs|可选的建议下一步操作或提示列表，用于在自定义代理之间进行切换。交接按钮在聊天响应完成后显示为交互式建议。|
|handoffs.label|显示在交接按钮上的显示文本。|
|handoffs.agent|要切换到的目标代理标识符。|
|handoffs.prompt|要发送到目标代理的提示文本。|
|handoffs.send|可选的布尔标志，用于自动提交提示（默认值为 false）。|


## 示例

```markdown
---
description: Generate an implementation plan for new features or refactoring existing code.
name: Planner
tools: ['fetch', 'githubRepo', 'search', 'usages']
model: Claude Sonnet 4
handoffs:
  - label: Implement Plan
    agent: agent
    prompt: Implement the plan outlined above.
    send: false
---
```