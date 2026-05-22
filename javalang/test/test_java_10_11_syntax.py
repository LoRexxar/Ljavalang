"""Java 10-11 新特性解析测试"""
import unittest
from .. import parse, tree


class VarLocalTest(unittest.TestCase):
    """Java 10 var 局部变量类型推断"""

    def test_var_simple(self):
        code = """class T {
            void m() {
                var x = "hello";
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_var_with_init(self):
        code = """class T {
            void m() {
                var list = new java.util.ArrayList<String>();
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_var_in_for_loop(self):
        code = """import java.util.*;
        class T {
            void m() {
                for (var s : new ArrayList<String>()) {}
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_var_in_twr(self):
        code = """import java.io.*;
        class T {
            void m() throws Exception {
                try (var fis = new FileInputStream("x")) {}
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)


class VarLambdaParamsTest(unittest.TestCase):
    """Java 11 var in lambda parameters"""

    def test_var_lambda_param(self):
        code = """import java.util.function.*;
        class T {
            Function<String, String> f = (var s) -> s.toUpperCase();
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_var_lambda_multiple_params(self):
        code = """import java.util.function.*;
        class T {
            java.util.function.BiFunction<String, String, String> f =
                (var a, var b) -> a + b;
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)
