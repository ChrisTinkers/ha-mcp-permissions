"""Static policy and API-surface checks. Run with: python -m unittest discover -s tests"""
import ast
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "ha_mcp_permissions" / "server.py").read_text(encoding="utf-8")
MODULE = ast.parse(SOURCE)


class PolicyTests(unittest.TestCase):
    def test_target_is_fixed(self):
        assignments = [n for n in MODULE.body if isinstance(n, ast.Assign)]
        matching = [n for n in assignments if any(isinstance(t, ast.Name) and t.id == "TARGET" for t in n.targets)]
        self.assertEqual(len(matching), 1)
        self.assertEqual(ast.literal_eval(matching[0].value), "todo.ha_weiterentwicklung")

    def test_only_approved_mcp_tools(self):
        names = set()
        for node in MODULE.body:
            if isinstance(node, ast.AsyncFunctionDef):
                if any(isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr == "tool" for d in node.decorator_list):
                    names.add(node.name)
        self.assertEqual(names, {
            "list_development_tasks",
            "add_development_task",
            "rename_development_task",
            "complete_development_task",
        })

    def test_no_entity_parameter_on_tools(self):
        for node in MODULE.body:
            if isinstance(node, ast.AsyncFunctionDef) and node.name.endswith("_development_task"):
                self.assertFalse({"entity_id", "domain", "service", "url"}.intersection(
                    {a.arg for a in node.args.args}
                ))

    def test_allowed_service_actions_constant(self):
        f = next(n for n in MODULE.body if isinstance(n, ast.AsyncFunctionDef) and n.name == "_ha_call")
        allowed = [n for n in ast.walk(f) if isinstance(n, ast.Set) and len(n.elts) == 3]
        self.assertTrue(any({ast.literal_eval(e) for e in n.elts} == {"get_items", "add_item", "update_item"} for n in allowed))


if __name__ == "__main__":
    unittest.main()
