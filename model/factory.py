import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from utils.config_handler import rag_conf, agent_conf

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.siliconflow.cn/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", os.getenv("SILICONFLOW_API_KEY", ""))
LLM_MODEL = os.getenv("LLM_MODEL", rag_conf["chat_model_name"])

EMBED_BASE_URL = os.getenv("EMBED_BASE_URL", "https://api.siliconflow.cn/v1")
EMBED_API_KEY = os.getenv("EMBED_API_KEY", os.getenv("SILICONFLOW_API_KEY", ""))
EMBED_MODEL = os.getenv("EMBED_MODEL", rag_conf["embedding_model_name"])

chat_model = ChatOpenAI(
    model=LLM_MODEL,
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
    timeout=agent_conf.get("llm_timeout", 120),
    max_retries=agent_conf.get("llm_max_retries", 3),
)

embed_model = OpenAIEmbeddings(
    model=EMBED_MODEL,
    base_url=EMBED_BASE_URL,
    api_key=EMBED_API_KEY,
)
