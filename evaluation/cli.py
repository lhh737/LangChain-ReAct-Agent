"""评估 CLI — python -m evaluation <command>"""
import sys
from dataclasses import dataclass


@dataclass
class Command:
    name: str
    module: str | None
    entry: str | None
    description: str
    required_data: list = None
    optional_deps: list = None
    needs_model: bool = False
    needs_network: bool = False
    stable: bool = True

    def __post_init__(self):
        if self.required_data is None:
            self.required_data = []
        if self.optional_deps is None:
            self.optional_deps = []


COMMANDS: dict[str, Command] = {
    "list": Command("list", None, None, "列出所有可用评估"),
    "build-dataset": Command(
        "build-dataset", "evaluation.build_eval_dataset", "main",
        "构建评估数据集", required_data=["data/"],
    ),
    "retrieval": Command(
        "retrieval", "evaluation.retrieval_eval", "main",
        "检索消融实验", required_data=["evaluation/test_questions.yml"],
    ),
    "query-rewrite": Command(
        "query-rewrite", "evaluation.query_rewrite_eval", "main",
        "查询改写评估", required_data=["evaluation/test_questions.yml"],
    ),
    "multi-query": Command(
        "multi-query", "evaluation.multi_query_eval", "main",
        "多查询评估", required_data=["evaluation/test_questions.yml"],
    ),
    "multi-query-ablation": Command(
        "multi-query-ablation", "evaluation.multi_query_ablation", "main",
        "多查询消融",
    ),
    "per-question": Command(
        "per-question", "evaluation.per_question_debug", "main",
        "逐题诊断", required_data=["evaluation/test_questions.yml"],
    ),
    "per-subquery": Command(
        "per-subquery", "evaluation.per_subquery_eval", "main",
        "逐子查询评估",
    ),
    "dump-chunks": Command(
        "dump-chunks", "evaluation.dump_chunks", "main",
        "导出 chunks",
    ),
    "inspect-top10": Command(
        "inspect-top10", "evaluation.inspect_top10_chunks", "main",
        "检查 Top10 chunks",
    ),
    "inspect-top10-rrf": Command(
        "inspect-top10-rrf", "evaluation.inspect_top10_rrf", "main",
        "检查 Top10 RRF",
    ),
    # 第二批（需要重型依赖或模型）
    "ragas": Command(
        "ragas", "evaluation.ragas_eval", "main",
        "RAGAS 指标评估", optional_deps=["ragas"], needs_model=True, stable=False,
    ),
    "agent": Command(
        "agent", "evaluation.evaluator", "main_agent",
        "Agent 端到端评估", optional_deps=["ragas"], needs_model=True, needs_network=True, stable=False,
    ),
    "rag": Command(
        "rag", "evaluation.evaluator", "main_rag",
        "RAG 直连评估", optional_deps=["ragas"], needs_model=True, needs_network=True, stable=False,
    ),
}


def _print_help() -> int:
    print("PaperMind 评估工具\n")
    print("用法: python -m evaluation <command> [args]\n")

    stable = {k: v for k, v in COMMANDS.items() if v.stable and k != "list"}
    exp = {k: v for k, v in COMMANDS.items() if not v.stable}

    print("  稳定命令:")
    for name, c in sorted(stable.items()):
        data = f"  data: {', '.join(c.required_data)}" if c.required_data else ""
        print(f"    {name:22s} {c.description:30s} {data}")

    if exp:
        print("\n  实验命令 (需要额外依赖或模型):")
        for name, c in sorted(exp.items()):
            flags = []
            if c.optional_deps:
                flags.append(f"deps: {', '.join(c.optional_deps)}")
            if c.needs_model:
                flags.append("model: yes")
            if c.needs_network:
                flags.append("network: yes")
            print(f"    {name:22s} {c.description:30s} {', '.join(flags)}")
    return 0


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help", "list"):
        return _print_help()

    cmd_name = argv[0]
    if cmd_name not in COMMANDS:
        print(f"Unknown command: {cmd_name}", file=sys.stderr)
        print("Run 'python -m evaluation list' to see available commands.", file=sys.stderr)
        return 1

    c = COMMANDS[cmd_name]
    if c.module is None:
        return _print_help()

    try:
        import importlib
        mod = importlib.import_module(c.module)
        func = getattr(mod, c.entry)
    except ModuleNotFoundError as e:
        missing = e.name
        if c.optional_deps and missing in c.optional_deps:
            print(f"Missing optional dependency: {missing}", file=sys.stderr)
            print(f"Install: pip install {missing}", file=sys.stderr)
            return 1
        raise
    except ImportError:
        raise

    return func(argv[1:])
