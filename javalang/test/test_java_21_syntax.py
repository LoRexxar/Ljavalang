"""Java 21+ 新特性解析测试"""
import unittest
from .. import parse, tree


class PatternMatchingSwitchTest(unittest.TestCase):
    """Java 21 pattern matching switch"""

    def test_type_pattern_switch(self):
        code = """class T {
            void m(Object o) {
                switch(o) {
                    case String s -> System.out.println(s);
                    case Integer i -> System.out.println(i);
                    default -> {}
                }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_null_case(self):
        code = """class T {
            void m(String s) {
                switch(s) {
                    case null -> System.out.println("null");
                    default -> {}
                }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)


class RecordPatternTest(unittest.TestCase):
    """Java 21 record pattern (deconstruction pattern)"""

    def test_simple_record_pattern(self):
        code = """class T {
            record Point(int x, int y) {}
            void m(Object o) {
                switch(o) {
                    case Point(int x, int y) -> System.out.println(x + y);
                    default -> {}
                }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_nested_record_pattern(self):
        code = """class T {
            record Point(int x, int y) {}
            record Rect(Point p1, Point p2) {}
            void m(Object o) {
                switch(o) {
                    case Rect(Point(int x1, int y1), Point(int x2, int y2)) ->
                        System.out.println(x1);
                    default -> {}
                }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_unnamed_pattern(self):
        code = """class T {
            record Point(int x, int y) {}
            void m(Object o) {
                switch(o) {
                    case Point(_, int y) -> System.out.println(y);
                    default -> {}
                }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_record_pattern_in_expression(self):
        code = """class T {
            record Point(int x, int y) {}
            int m(Object o) {
                return switch(o) {
                    case Point(int x, int y) -> x + y;
                    default -> 0;
                };
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)


class UnnamedVariableTest(unittest.TestCase):
    """Java 22 unnamed variable _"""

    def test_unnamed_catch(self):
        code = """class T {
            void m() {
                try {
                    int x = 1 / 0;
                } catch (Exception _) {
                    System.out.println("ignored");
                }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_unnamed_lambda(self):
        code = """import java.util.*;
        class T {
            void m() {
                new ArrayList<String>().forEach(_ -> System.out.println("x"));
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)


class ChainCallTest(unittest.TestCase):
    """链式调用修复验证"""

    def test_two_step_chain(self):
        """Runtime.getRuntime().exec(cmd) 链式调用"""
        code = """class T {
            void m(String cmd) throws Exception {
                Runtime.getRuntime().exec(cmd);
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_three_step_chain(self):
        code = """class T {
            void m() {
                new java.util.ArrayList<>().stream().count();
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)
