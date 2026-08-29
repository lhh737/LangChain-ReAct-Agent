"""Agent 回调 — 工具监控 + 模型调用日志 + 轮次统计"""
import time
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import ToolMessage, AIMessage
from utils.logger_handler import logger


class AgentCallback(BaseCallbackHandler):
    """统一的 Agent 回调处理器，记录工具调用和模型调用详情"""

    def __init__(self):
        self.tool_invocation_log: list[dict] = []
        self._current_tool_name: str | None = None
        self._current_tool_start: float | None = None

    def on_tool_start(self, serialized: dict, input_str: str, **kwargs):
        name = serialized.get("name", "unknown")
        logger.info(f"[Tool] 执行: {name}")
        logger.info(f"[Tool] 参数: {input_str[:200]}")
        self._current_tool_name = name
        self._current_tool_start = time.time()

    def on_tool_end(self, output: str, **kwargs):
        elapsed = time.time() - (self._current_tool_start or 0)
        output_str = str(output) if not isinstance(output, str) else output
        output_len = len(output_str)
        logger.info(f"[Tool] {self._current_tool_name} 完成 ({elapsed:.1f}s) → 输出长度={output_len}")
        self.tool_invocation_log.append({
            "name": self._current_tool_name,
            "output": output,
            "elapsed": round(elapsed, 2),
            "status": "success",
        })

    def on_tool_error(self, error: BaseException, **kwargs):
        logger.error(f"[Tool] {self._current_tool_name} 失败: {error}")
        self.tool_invocation_log.append({
            "name": self._current_tool_name,
            "error": str(error),
            "elapsed": round(time.time() - (self._current_tool_start or 0), 2),
            "status": "error",
        })

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        msg_count = 0
        for p in prompts:
            if hasattr(p, "content"):
                msg_count += 1
        logger.info(f"[LLM] 调用模型，prompt片段数={len(prompts)}，消息数={msg_count}")

    def on_llm_end(self, response, **kwargs):
        token_info = ""
        if hasattr(response, "llm_output") and response.llm_output:
            usage = response.llm_output.get("token_usage", {})
            if usage:
                token_info = f" tokens: in={usage.get('prompt_tokens', '?')} out={usage.get('completion_tokens', '?')}"
        logger.info(f"[LLM] 模型调用完成{token_info}")

    def get_tool_log(self) -> list[dict]:
        return self.tool_invocation_log

    def get_round_stats(self) -> dict:
        total = len(self.tool_invocation_log)
        success = sum(1 for t in self.tool_invocation_log if t.get("status") == "success")
        errors = total - success
        return {
            "total_tool_calls": total,
            "successful": success,
            "errors": errors,
        }
