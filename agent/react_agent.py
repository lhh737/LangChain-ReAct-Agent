from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import (rag_summarize, get_weather, get_user_location, get_user_id,
                                     get_current_month, fetch_external_data, fill_context_for_report)
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage


class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[rag_summarize, get_weather, get_user_location, get_user_id,
                   get_current_month, fetch_external_data, fill_context_for_report],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )

    def execute_stream(self, query: str, chat_history: list[BaseMessage] = None):
        """
        支持多轮对话的流式执行
        :param query: 当前用户输入
        :param chat_history: 可选，LangChain 消息列表（仅包含 HumanMessage 和纯文本 AIMessage）
        """
        messages = []
        if chat_history:
            for msg in chat_history:
                if isinstance(msg, HumanMessage):
                    messages.append(msg)
                elif isinstance(msg, AIMessage) and not msg.tool_calls:
                    messages.append(msg)
        messages.append(HumanMessage(content=query))
        input_dict = {"messages": messages}
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() + "\n"

if __name__ == '__main__':
    agent = ReactAgent()

    for chunk in agent.execute_stream("给我生成我的使用报告"):
        print(chunk, end="", flush=True)
