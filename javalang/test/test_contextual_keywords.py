"""Contextual keyword regression tests (JLS 3.8).

Module directives reserve words like 'to'/'with' ONLY inside module-info.
As plain identifiers they are legal everywhere (method names, variables).
Fixes: 'to' (839131f), 'with' (d468924, CVE-2026-15564 — Elytron's
AuthenticationContext.captureCurrent().with(..) in WildFly).
"""
import unittest
import javalang


class ContextualKeywordTest(unittest.TestCase):
    def test_with_as_method_name(self):
        src = (
            'class T { void m() { Object o = AuthenticationContext'
            '.captureCurrent().with(MatchRule.ALL.matchProtocol("iiop"), conf); } }'
        )
        tree = javalang.parse.parse(src)
        calls = [n.member for _, n in tree.filter(javalang.tree.MethodInvocation)]
        self.assertIn('with', calls)

    def test_with_as_variable(self):
        tree = javalang.parse.parse(
            'class T { Object with; void m() { with = null; } }')
        self.assertIsNotNone(tree)

    def test_to_as_method_name(self):
        tree = javalang.parse.parse(
            'class T { int to(int x) { return x; } void m() { int y = to(1); } }')
        self.assertIsNotNone(tree)

    def test_module_provides_with_still_works(self):
        tree = javalang.parse.parse(
            'module m { provides a.B with c.D, e.F; uses x.Y; }')
        provides = [n for _, n in tree.filter(javalang.tree.ProvidesDirective)]
        self.assertEqual(len(provides), 1)
        self.assertEqual(provides[0].implementations, ['c.D', 'e.F'])

    def test_module_opens_to_still_works(self):
        tree = javalang.parse.parse('module m { opens a.b to c.D, e.F; }')
        opens = [n for _, n in tree.filter(javalang.tree.OpensDirective)]
        self.assertEqual(len(opens), 1)


if __name__ == '__main__':
    unittest.main()
