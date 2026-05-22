"""上游 javalang issue 修复验证测试"""
import unittest
from .. import parse, tree
from .. import tokenizer


class Issue90And117Test(unittest.TestCase):
    """#90/#117: DecimalInteger 应继承 Integer 而非 Literal"""

    def test_decimal_integer_is_integer(self):
        self.assertTrue(issubclass(tokenizer.DecimalInteger, tokenizer.Integer))

    def test_decimal_integer_is_literal(self):
        self.assertTrue(issubclass(tokenizer.DecimalInteger, tokenizer.Literal))

    def test_other_integers_are_integer(self):
        for cls in (tokenizer.OctalInteger, tokenizer.HexInteger, tokenizer.BinaryInteger):
            self.assertTrue(issubclass(cls, tokenizer.Integer), f"{cls} should inherit Integer")


class Issue145Test(unittest.TestCase):
    """#145: char 字面量应生成 Character token 类型"""

    def test_char_literal_token_type(self):
        tokens = list(tokenizer.tokenize("'a'"))
        self.assertIsInstance(tokens[0], tokenizer.Character)

    def test_string_literal_token_type(self):
        tokens = list(tokenizer.tokenize('"hello"'))
        self.assertIsInstance(tokens[0], tokenizer.String)

    def test_char_escape(self):
        tokens = list(tokenizer.tokenize(r"'\n'"))
        self.assertIsInstance(tokens[0], tokenizer.Character)


class Issue81And112Test(unittest.TestCase):
    """#81/#112: 泛型内注解支持"""

    def test_annotation_in_generics(self):
        code = 'class T { List<@NotNull String> list; }'
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_annotation_with_value_in_generics(self):
        code = 'class T { List<@Length(min=0) String> list; }'
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_multiple_annotations_in_generics(self):
        code = 'class T { Map<@NotNull String, @Valid Integer> map; }'
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_normal_generics_regression(self):
        code = 'class T { List<String> list; }'
        result = parse.parse(code)
        self.assertIsNotNone(result)


class Issue141Test(unittest.TestCase):
    """#141: void 返回类型不应为 None"""

    def test_class_void_method_return_type(self):
        code = 'class T { void m() {} }'
        result = parse.parse(code)
        method = result.types[0].body[0]
        self.assertEqual(method.return_type, 'void')

    def test_interface_void_method_return_type(self):
        code = 'interface I { void m(); }'
        result = parse.parse(code)
        method = result.types[0].body[0]
        self.assertEqual(method.return_type, 'void')

    def test_non_void_return_type_regression(self):
        code = 'class T { int m() { return 1; } }'
        result = parse.parse(code)
        method = result.types[0].body[0]
        self.assertIsInstance(method.return_type, tree.BasicType)
        self.assertEqual(method.return_type.name, 'int')


class Issue77And150Test(unittest.TestCase):
    """#77/#150: 双分号空语句支持"""

    def test_double_semicolon(self):
        code = 'class T { void m() { int x = 1;; } }'
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_empty_statement(self):
        code = 'class T { void m() { ; } }'
        result = parse.parse(code)
        self.assertIsNotNone(result)


class Issue76And135Test(unittest.TestCase):
    """#76/#135: 逻辑非 ! 运算符"""

    def test_not_operator(self):
        code = 'class T { boolean m() { return !true; } }'
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_not_in_if(self):
        code = 'class T { void m() { if (!true) {} } }'
        result = parse.parse(code)
        self.assertIsNotNone(result)


class Issue89And142Test(unittest.TestCase):
    """#89/#142: 链式调用修复"""

    def test_two_step_chain(self):
        code = 'class T { void m() { Runtime.getRuntime().exec("ls"); } }'
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_three_step_chain(self):
        code = 'class T { void m() { a.b().c().d(); } }'
        result = parse.parse(code)
        self.assertIsNotNone(result)


class Issue19Test(unittest.TestCase):
    """#19: Node __equals__ 自反性"""

    def test_equals_reflexive(self):
        node = tree.Literal(value='test')
        self.assertEqual(node, node)

    def test_not_equals_reflexive(self):
        node = tree.Literal(value='test')
        self.assertFalse(node != node)


class Issue146Test(unittest.TestCase):
    """#146: Tokenizer 对整数 0 结尾表达式不崩溃"""

    def test_zero_integer(self):
        tokens = list(tokenizer.tokenize("int x = 0;"))
        self.assertTrue(len(tokens) > 0)

    def test_zero_in_expression(self):
        code = 'class T { void m() { i = 0; } }'
        result = parse.parse(code)
        self.assertIsNotNone(result)


class Issue114Test(unittest.TestCase):
    """#114: 前缀/后缀运算符"""

    def test_postfix_increment(self):
        code = 'class T { void m() { int x = 1; x++; } }'
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_prefix_increment(self):
        code = 'class T { void m() { int x = 1; ++x; } }'
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_prefix_decrement(self):
        code = 'class T { void m() { int x = 1; --x; } }'
        result = parse.parse(code)
        self.assertIsNotNone(result)


class Issue24And108Test(unittest.TestCase):
    """#24/#108: 强制类型转换后方法调用"""

    def test_cast_then_method_call(self):
        code = 'class T { void m(Object x) { ((String)x).length(); } }'
        result = parse.parse(code)
        self.assertIsNotNone(result)
