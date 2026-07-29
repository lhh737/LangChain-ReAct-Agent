"""缓存线程安全：原子写入、per-key 锁、损坏恢复"""
import os
import json
import threading
from utils.logger_handler import logger

# per-key 进程内锁
_key_locks: dict[str, threading.Lock] = {}
_locks_guard = threading.Lock()


def _get_lock(key: str) -> threading.Lock:
    with _locks_guard:
        if key not in _key_locks:
            _key_locks[key] = threading.Lock()
        return _key_locks[key]


def atomic_write(path: str, data: object):
    """先写临时文件再 rename，保证原子性"""
    tmp = path + f".tmp.{os.getpid()}"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except Exception as e:
        logger.warning(f"[CacheSafety] atomic write failed: {path} - {e}")
        try:
            os.remove(tmp)
        except OSError:
            pass


def safe_read(path: str) -> object | None:
    """安全读缓存：损坏 JSON → None"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError):
        return None


def safe_remove(path: str):
    """安全删除：容忍文件不存在"""
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


class CacheGuard:
    """per-key lock + atomic write 的缓存写保护"""

    @staticmethod
    def write(key: str, cache_dir: str, data: object):
        lock = _get_lock(key)
        with lock:
            cache_file = os.path.join(cache_dir, f"{key}.json")
            atomic_write(cache_file, data)

    @staticmethod
    def read(key: str, cache_dir: str) -> object | None:
        cache_file = os.path.join(cache_dir, f"{key}.json")
        result = safe_read(cache_file)
        if result is None and os.path.exists(cache_file):
            # 损坏 → 删除
            safe_remove(cache_file)
        return result

    @staticmethod
    def remove_expired(key: str, cache_dir: str):
        lock = _get_lock(key)
        with lock:
            cache_file = os.path.join(cache_dir, f"{key}.json")
            safe_remove(cache_file)
