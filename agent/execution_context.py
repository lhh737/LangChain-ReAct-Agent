"""Per-request 执行上下文 —— 替换模块级 _shared_state 可变全局变量。

ExecutionContext 在 execute_stream() 入口创建，沿调用链显式传递，
不依赖任何模块级单例。
"""
from dataclasses import dataclass
from agent.retrieval_state import AgentRetrievalState
from agent.execution_policy import AgentExecutionPolicy


@dataclass
class ExecutionContext:
    """单次请求的不可变配置 + 可变运行时状态"""
    policy: AgentExecutionPolicy
    retrieval_state: AgentRetrievalState
