# LangGraph 可审批 Agent 工作流

基于 LangGraph 的多步 Agent 工作流，演示「搜索 → 分析 → 报告生成 → 人工审批 → 导出」的
生产级编排：支持**状态持久化暂停**、**跨进程恢复**、**人工审批门控**与**导出幂等**。

## 解决什么问题

多步 Agent 在生产环境里最大的风险不是“跑不通”，而是“跑到一半出错/需要人确认时，
无法安全暂停和恢复”。本项目用 LangGraph 的 StateGraph + checkpoint + interrupt，
把“暂停 → 人工审批 → 从断点恢复”做成执行器的一等能力，而不是业务代码里手写的
try-catch 和重试逻辑。

## 工作流架构

- `search / analyze / report`：三个业务节点，通过共享 State 传递数据
- `approval`：调用 `interrupt()` 暂停，等待人工给出 approve / reject / edit
- `export`：带幂等键的导出节点，防止重复审批导致外部动作重复执行

## 核心特性

| 特性 | 实现 | 验证方式 |
|---|---|---|
| 状态持久化 | `SqliteSaver` checkpoint，每个节点后落盘 | `workflow_checkpoints.db` |
| 跨进程暂停/恢复 | `interrupt()` + `Command(resume=...)` | `main.py` 暂停 → `resume.py` 恢复 |
| 人工审批门控 | 条件边按 `approval_decision` 路由 | `demo_paths.py` 三条路径 |
| 导出幂等 | `thread_id` 作幂等键 + 本地账本 | `test_idempotent.py` |
| 可观测性 | LangSmith trace，节点级调用链 | 项目页可查看完整 trace |

## 快速开始

```bash
python -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 配置 .env
```bash
DEEPSEEK_API_KEY=sk-...
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_pt_...
LANGSMITH_PROJECT=langgraph-approval-workflow
```

## 1) 跑到审批暂停
```bash
python main.py
```

## 2) 在另一个进程恢复并导出
```bash
python resume.py
```

## 3) 演示三条审批路径
```bash
python demo_paths.py
```

## 4) 验证导出幂等
```bash
python test_idempotent.py
```

## 技术栈

LangGraph：StateGraph 编排、checkpoint、interrupt

LangChain OpenAI：接入 DeepSeek（OpenAI 兼容接口）

SQLite：checkpoint 与幂等账本持久化

LangSmith：节点级 trace 与可观测性

## 设计要点

节点只返回增量：节点返回 {"key": value} 由 LangGraph 合并，而非原地修改 State，
保证 checkpoint 的一致性。

Reducer 区分覆盖与累积：search_results 用 operator.add 累积多源结果，
report_draft 等用默认覆盖。

两道幂等防线：LangGraph 层面拒绝已完成实例的重复恢复；export_node 内部用
thread_id 账本兜底节点重入。

恢复时不重放已完成节点：checkpoint 记录 next，恢复从 approval 继续，
search/analyze/report 不会二次调用模型。