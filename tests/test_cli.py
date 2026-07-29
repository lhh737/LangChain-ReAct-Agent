"""S10: 评估 CLI 测试"""
import unittest
from evaluation.cli import main, COMMANDS, Command


class TestCLI(unittest.TestCase):

    def test_list_returns_zero(self):
        self.assertEqual(main(["list"]), 0)

    def test_help_returns_zero(self):
        self.assertEqual(main(["-h"]), 0)

    def test_unknown_returns_nonzero(self):
        self.assertNotEqual(main(["nonexistent_cmd_xyz"]), 0)

    def test_no_args_shows_help(self):
        self.assertEqual(main([]), 0)

    def test_command_registry_valid(self):
        for name, cmd in COMMANDS.items():
            self.assertIsInstance(cmd, Command)
            self.assertEqual(cmd.name, name)
            if cmd.module is not None:
                self.assertIsNotNone(cmd.entry)

    def test_command_with_args_passed(self):
        """验证 list 命令正常返回"""
        result = main(["list"])
        self.assertEqual(result, 0)


class TestLazyImport(unittest.TestCase):

    def test_list_does_not_import_heavy_modules(self):
        """list 命令不导入重型评估模块"""
        import sys
        before = set(sys.modules.keys())
        main(["list"])
        after = set(sys.modules.keys())
        new_modules = after - before
        heavy = [m for m in new_modules if "ragas" in m or "evaluation." in m]
        self.assertEqual(len(heavy), 0,
                         f"Unexpected heavy imports: {heavy}")


if __name__ == "__main__":
    unittest.main()
