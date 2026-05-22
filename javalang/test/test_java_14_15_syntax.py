"""Java 14-15 新特性解析测试"""
import unittest
from .. import parse, tree


class SwitchArrowTest(unittest.TestCase):
    """Java 14 switch arrow 语法"""

    def test_arrow_simple(self):
        code = """class T {
            void m(int x) {
                switch(x) {
                    case 1 -> System.out.println("one");
                    default -> System.out.println("other");
                }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_arrow_block(self):
        code = """class T {
            void m(int x) {
                switch(x) {
                    case 1 -> {
                        System.out.println("one");
                        System.out.println("1");
                    }
                    default -> {}
                }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_arrow_throw(self):
        code = """class T {
            void m(int x) {
                switch(x) {
                    case 1 -> throw new RuntimeException("one");
                    default -> {}
                }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_multi_case_arrow(self):
        code = """class T {
            void m(int x) {
                switch(x) {
                    case 1, 2, 3 -> System.out.println("small");
                    default -> System.out.println("big");
                }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_classic_colon_regression(self):
        """确保经典冒号 switch 不受影响"""
        code = """class T {
            String m(int x) {
                switch(x) {
                    case 1: return "one";
                    default: return "other";
                }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)


class YieldStatementTest(unittest.TestCase):
    """Java 14 yield 语句"""

    def test_yield_in_switch(self):
        code = """class T {
            void m(int x) {
                switch(x) {
                    case 1: yield "one";
                    default: yield "other";
                }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)


class SwitchExpressionTest(unittest.TestCase):
    """Java 14 switch expression (表达式级别)"""

    def test_switch_expr_return(self):
        code = """class T {
            int m(Object o) {
                return switch(o) {
                    case String s -> s.length();
                    case Integer i -> i;
                    default -> -1;
                };
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)
        # 验证 return 语句中的表达式是 SwitchExpression
        method = result.types[0].body[0]
        ret_stmt = method.body[0]
        self.assertIsInstance(ret_stmt.expression, tree.SwitchExpression)

    def test_switch_expr_assign(self):
        code = """class T {
            int m(int x) {
                int result = switch(x) {
                    case 1 -> 10;
                    case 2 -> 20;
                    default -> 0;
                };
                return result;
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)


class PatternMatchingInstanceofTest(unittest.TestCase):
    """Java 14 pattern matching instanceof"""

    def test_instanceof_pattern(self):
        code = """class T {
            void m(Object obj) {
                if (obj instanceof String s) {
                    System.out.println(s.length());
                }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_instanceof_pattern_negated(self):
        code = """class T {
            void m(Object obj) {
                if (!(obj instanceof String s)) {
                    return;
                }
                System.out.println(s);
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_instanceof_classic_regression(self):
        """确保经典 instanceof 不受影响"""
        code = """class T {
            boolean m(Object obj) {
                return obj instanceof String;
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)


class TextBlockTest(unittest.TestCase):
    """Java 15 text block 三引号字符串"""

    def test_text_block_multiline(self):
        code = '''class T {
            String query = """
                SELECT * FROM users
                WHERE id = 1
            """;
        }'''
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_text_block_empty(self):
        code = 'class T { String s = """"""; }'
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_text_block_oneline(self):
        code = 'class T { String s = """hello"""; }'
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_regular_string_regression(self):
        """确保普通字符串不受影响"""
        code = 'class T { String s = "hello world"; }'
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_char_literal_regression(self):
        """确保字符字面量不受影响"""
        code = "class T { char c = 'x'; }"
        result = parse.parse(code)
        self.assertIsNotNone(result)
