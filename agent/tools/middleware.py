from typing import Callable
from utils.prompt_loader import load_system_prompts, load_report_prompts
from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import logger

@wrap_tool_call
def monitor_tool(
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")

    max_retries = 3
    last_exception = None

    for attempt in range(1, max_retries + 1):
        try:
            result = handler(request)
            logger.info(f"[tool monitor]工具{request.tool_call['name']}调用成功（尝试 {attempt} 次）")

            if request.tool_call['name'] == "fill_context_for_report":
                request.runtime.context["report"] = True
                
            return result
        except Exception as e:
            last_exception = e
            logger.warning(f"[tool monitor]工具{request.tool_call['name']}调用失败（尝试 {attempt}/{max_retries}），原因：{str(e)}")
            if attempt < max_retries:
                import time
                time.sleep(0.5)
            continue

    logger.error(f"[tool monitor]工具{request.tool_call['name']}重试{max_retries}次后仍失败")
    raise last_exception

@before_model
def log_before_model(
        state: AgentState,        
        runtime: Runtime,          
):        
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条消息。")

    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")

    return None


@dynamic_prompt                 
def report_prompt_switch(request: ModelRequest):     
    is_report = request.runtime.context.get("report", False)
    if is_report:              
        return load_report_prompts()

    return load_system_prompts()
