"""上游 javalang FEATURE 实现测试"""
import unittest
from .. import parse, tree, tokenizer
from ..visitor import JavaVisitor


class Issue114PrefixPostfixTest(unittest.TestCase):
    """#114/#41/#26: prefix/postfix 运算符保留"""

    def test_prefix_not_in_return(self):
        code = 'class T { boolean m() { return !true; } }'
        result = parse.parse(code)
        ret = result.types[0].body[0].body[0]
        self.assertEqual(ret.expression.prefix_operators, ['!'])

    def test_postfix_increment(self):
        code = 'class T { void m() { int x = counter++; } }'
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_prefix_in_parens(self):
        code = 'class T { boolean m(boolean a, boolean b) { return (!a) && b; } }'
        result = parse.parse(code)
        self.assertIsNotNone(result)


class Issue88ReceiverParameterTest(unittest.TestCase):
    """#88: Receiver parameter"""

    def test_receiver_parameter_in_method(self):
        code = 'class Outer { class Inner { void m(Inner.this, int x) {} } }'
        result = parse.parse(code)
        inner = result.types[0].body[0]
        method = inner.body[0]
        self.assertEqual(len(method.parameters), 2)
        self.assertIsInstance(method.parameters[0], tree.ReceiverParameter)
        self.assertEqual(method.parameters[0].name, 'Inner.this')
        self.assertIsInstance(method.parameters[1], tree.FormalParameter)

    def test_normal_params_regression(self):
        code = 'class T { void m(int x, String y) {} }'
        result = parse.parse(code)
        method = result.types[0].body[0]
        self.assertEqual(len(method.parameters), 2)
        for p in method.parameters:
            self.assertIsInstance(p, tree.FormalParameter)


class Issue133VisitorTest(unittest.TestCase):
    """#133: Visitor 类"""

    def test_visitor_dispatches(self):
        """Visitor 应正确分发到 visit_ClassDeclaration"""
        class ClassCollector(JavaVisitor):
            def __init__(self):
                self.classes = []
            def visit_ClassDeclaration(self, node):
                self.classes.append(node.name)
                self.generic_visit(node)

        code = 'class A { class B {} }'
        tree = parse.parse(code)
        v = ClassCollector()
        v.visit(tree)
        self.assertEqual(v.classes, ['A', 'B'])

    def test_visitor_generic(self):
        """generic_visit 应递归遍历子节点"""
        class MethodCollector(JavaVisitor):
            def __init__(self):
                self.methods = []
            def visit_MethodDeclaration(self, node):
                self.methods.append(node.name)
                self.generic_visit(node)

        code = 'class T { void foo() {} int bar() { return 1; } }'
        tree = parse.parse(code)
        v = MethodCollector()
        v.visit(tree)
        self.assertEqual(v.methods, ['foo', 'bar'])


class Issue100TokenRangeTest(unittest.TestCase):
    """#100: Position.range 字段"""

    def test_position_has_range(self):
        tokens = list(tokenizer.tokenize('int x;'))
        self.assertTrue(hasattr(tokens[0].position, 'range'))
        self.assertIsInstance(tokens[0].position.range, slice)

    def test_range_correctness(self):
        code = 'int x = 42;'
        tokens = list(tokenizer.tokenize(code))
        # int -> [0:3], x -> [4:5], = -> [6:7], 42 -> [8:10], ; -> [10:11]
        self.assertEqual(code[tokens[0].position.range], 'int')
        self.assertEqual(code[tokens[1].position.range], 'x')
        self.assertEqual(code[tokens[3].position.range], '42')


class Issue137ReturnIndexTest(unittest.TestCase):
    """#137: tokenize return_index 参数"""

    def test_return_index_false(self):
        tokens = list(tokenizer.tokenize('int x;', return_index=False))
        self.assertTrue(all(not isinstance(t, tuple) for t in tokens))

    def test_return_index_true(self):
        results = list(tokenizer.tokenize('int x;', return_index=True))
        for item in results:
            token, (start, end) = item
            self.assertIsInstance(token, tokenizer.JavaToken)
            self.assertIsInstance(start, int)
            self.assertIsInstance(end, int)

    def test_index_values(self):
        code = 'int x;'
        results = list(tokenizer.tokenize(code, return_index=True))
        # First token 'int' -> [0, 3]
        _, (s, e) = results[0]
        self.assertEqual(code[s:e], 'int')
