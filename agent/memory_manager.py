"""三层记忆系统 — 短期缓冲 + LLM 压缩摘要 + 长期事实提取"""
import json
import os
import re
from datetime import datetime
from utils.path_tool import get_abs_path
from utils.logger_handler import logger


class ShortTermMemory:
    """最近 4 轮对话缓冲，JSON 持久化"""

    MAX_TURNS = 4
    STORE_FILE = "data/short_term_memory.json"

    def __init__(self):
        self.buffer: list[dict] = []
        self._load()

    def add_turn(self, user_msg: str, assistant_msg: str):
        now = datetime.now().isoformat()
        self.buffer.append({"role": "user", "content": user_msg, "timestamp": now})
        self.buffer.append({"role": "assistant", "content": assistant_msg, "timestamp": now})
        self._trim()
        self._save()

    def _trim(self):
        max_entries = self.MAX_TURNS * 2
        if len(self.buffer) > max_entries:
            self.buffer = self.buffer[-max_entries:]

    def get_recent_turns(self) -> list[dict]:
        return [{"role": m["role"], "content": m["content"]} for m in self.buffer]

    def should_compress(self) -> bool:
        return len(self.buffer) >= self.MAX_TURNS * 4

    def turn_count(self) -> int:
        return len(self.buffer) // 2

    def _load(self):
        path = get_abs_path(self.STORE_FILE)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.buffer = json.load(f)
                logger.info(f"[ShortTermMemory] 已加载 {len(self.buffer)} 条记录")
            except Exception as e:
                logger.warning(f"[ShortTermMemory] 加载失败: {e}")
                self.buffer = []

    def _save(self):
        path = get_abs_path(self.STORE_FILE)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.buffer, f, ensure_ascii=False, indent=2)


class CumulativeSummary:
    """超出短期记忆的对话由 LLM 压缩为累积摘要，JSON 持久化"""

    SUMMARY_FILE = "data/cumulative_summary.json"

    def __init__(self):
        self.summary: str = ""
        self._load()

    def update(self, conversation_text: str, chat_model):
        if not self.summary:
            self.summary = conversation_text
        else:
            prompt = (
                "将以下两段内容合并为一段简洁的对话摘要（中文，≤200字），"
                "保留关键的论文名、方法名、研究发现和用户偏好。\n"
                f"已有摘要：{self.summary}\n"
                f"新增对话：{conversation_text}\n"
                "合并后的摘要："
            )
            try:
                response = chat_model.invoke(prompt, temperature=0, max_tokens=300)
                self.summary = response.content.strip()
            except Exception as e:
                logger.warning(f"[CumulativeSummary] LLM 压缩失败: {e}")
        self._save()

    def get_summary_message(self) -> dict | None:
        if not self.summary:
            return None
        return {"role": "system", "content": f"对话历史摘要: {self.summary}"}

    def _load(self):
        path = get_abs_path(self.SUMMARY_FILE)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.summary = json.load(f).get("summary", "")
            except Exception:
                self.summary = ""

    def _save(self):
        path = get_abs_path(self.SUMMARY_FILE)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"summary": self.summary, "updated_at": datetime.now().isoformat()},
                      f, ensure_ascii=False, indent=2)


class FactStore:
    """长期事实提取与持久化（每 3 轮触发一次），跨会话保留"""

    STORE_FILE = "data/long_term_facts.json"
    EXTRACT_INTERVAL = 3

    FACT_EXTRACT_PROMPT = (
        "从以下科研对话中提取客观事实语句。只提取关于论文名、方法、实验数据、"
        "研究发现、用户研究偏好的陈述。每行一条，只返回纯文本，不要编号和 JSON。\n"
        "对话内容：\n{conversation}\n"
        "提取的事实："
    )

    def __init__(self):
        self.facts: dict[str, list[str]] = {}
        self._load()

    def extract_facts(self, conversation_buffer: list[dict]) -> list[str]:
        text = "\n".join(
            f"[{m['role']}]: {m['content'][:300]}" for m in conversation_buffer[-8:]
        )
        try:
            from model.factory import chat_model
            response = chat_model.invoke(
                self.FACT_EXTRACT_PROMPT.format(conversation=text),
                temperature=0,
                max_tokens=200,
            )
            lines = [l.strip("- ").strip() for l in response.content.strip().split("\n") if l.strip()]
            return [l for l in lines if len(l) > 10]
        except Exception as e:
            logger.warning(f"[FactStore] 事实提取失败: {e}")
            return []

    def add_facts(self, category: str, facts: list[str]):
        if category not in self.facts:
            self.facts[category] = []
        existing = {f.lower() for f in self.facts[category]}
        for fact in facts:
            if fact.lower() not in existing:
                self.facts[category].append(fact)
                existing.add(fact.lower())
        self._save()

    def get_facts_text(self) -> str:
        if not self.facts:
            return ""
        lines = []
        for category, items in self.facts.items():
            if items:
                lines.append(f"已知信息（{category}）：")
                for item in items[-10:]:
                    lines.append(f"- {item}")
        return "\n".join(lines)

    def _load(self):
        path = get_abs_path(self.STORE_FILE)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.facts = json.load(f)
            except Exception:
                self.facts = {}

    def _save(self):
        path = get_abs_path(self.STORE_FILE)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.facts, f, ensure_ascii=False, indent=2)
