"""Java 16-17 新特性解析测试"""
import unittest
from .. import parse, tree


class RecordDeclarationTest(unittest.TestCase):
    """Java 16 record class"""

    def test_record_simple(self):
        code = "record Point(int x, int y) {}"
        result = parse.parse(code)
        self.assertIsNotNone(result)
        self.assertIsInstance(result.types[0], tree.RecordDeclaration)
        self.assertEqual(result.types[0].name, 'Point')

    def test_record_implements(self):
        code = "record R(int x) implements java.io.Serializable {}"
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_record_with_body(self):
        code = """record R(int x) {
            public String toString() { return "R"; }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_record_generic(self):
        code = "record Pair<A, B>(A a, B b) {}"
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_record_as_member(self):
        """record 作为类内部成员"""
        code = """class T {
            record Point(int x, int y) {}
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_local_record_in_method(self):
        """record 作为方法内的局部声明"""
        code = """class T {
            void m() {
                record R(int x) {}
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_local_enum_in_method(self):
        """enum 作为方法内的局部声明"""
        code = """class T {
            void m() {
                enum E { A, B }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)


class SealedClassTest(unittest.TestCase):
    """Java 17 sealed / permits / non-sealed"""

    def test_sealed_class(self):
        code = """sealed class Shape permits Circle, Rect {}
        final class Circle extends Shape {}
        final class Rect extends Shape {}"""
        result = parse.parse(code)
        self.assertIsNotNone(result)
        self.assertIn('sealed', result.types[0].modifiers)

    def test_sealed_class_permits_attr(self):
        """验证 permits 属性被正确解析"""
        code = "sealed class Shape permits Circle {} final class Circle extends Shape {}"
        result = parse.parse(code)
        self.assertIsNotNone(result.types[0].permits)

    def test_sealed_interface(self):
        code = """sealed interface I permits A, B {}
        record A(int x) implements I {}
        record B(int x) implements I {}"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_non_sealed(self):
        code = """sealed class S permits X, Y {}
        non-sealed class X extends S {}
        final class Y extends S {}"""
        result = parse.parse(code)
        self.assertIsNotNone(result)
        self.assertIn('non-sealed', result.types[1].modifiers)

    def test_sealed_with_record(self):
        code = """sealed interface Shape permits Point, Rect {}
        record Point(int x, int y) implements Shape {}
        record Rect(int w, int h) implements Shape {}"""
        result = parse.parse(code)
        self.assertIsNotNone(result)
