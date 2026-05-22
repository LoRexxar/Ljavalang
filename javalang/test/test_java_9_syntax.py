"""Java 9 新特性解析测试"""
import unittest
from .. import parse, tree


class TryWithResourcesTest(unittest.TestCase):
    """Java 9 effectively final try-with-resources"""

    def test_effectively_final_resource(self):
        """J9: try(fis) 引用 effectively final 变量"""
        code = """import java.io.*;
        class T {
            void m() throws Exception {
                FileInputStream fis = new FileInputStream("x");
                try (fis) { fis.read(); }
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_mixed_resources(self):
        """J9: 混合 effectively final 和声明式 resource"""
        code = """import java.io.*;
        class T {
            void m() throws Exception {
                FileInputStream fis = new FileInputStream("a");
                try (fis; FileOutputStream fos = new FileOutputStream("b")) {}
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_classic_twr_regression(self):
        """J8: 经典 TWR 回归"""
        code = """import java.io.*;
        class T {
            void m() throws Exception {
                try (FileInputStream f = new FileInputStream("x")) {}
            }
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)


class PrivateInterfaceMethodsTest(unittest.TestCase):
    """Java 9 private interface methods"""

    def test_private_interface_method(self):
        code = """interface I {
            private void helper() {}
            private static void util() {}
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)


class ModuleInfoTest(unittest.TestCase):
    """Java 9 module-info 解析"""

    def test_module_basic(self):
        code = "module foo { requires java.base; }"
        result = parse.parse(code)
        self.assertEqual(result.module.name, 'foo')
        self.assertFalse(result.module.open)

    def test_module_open(self):
        code = "open module bar { requires java.base; }"
        result = parse.parse(code)
        self.assertEqual(result.module.name, 'bar')
        self.assertTrue(result.module.open)

    def test_module_requires_transitive(self):
        code = "module app { requires transitive java.sql; }"
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_module_exports_to(self):
        code = "module app { exports api to client1, client2; }"
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_module_opens(self):
        code = "module app { opens impl to fw; }"
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_module_uses_provides(self):
        code = "module app { uses spi.Service; provides spi.Service with impl.Impl; }"
        result = parse.parse(code)
        self.assertIsNotNone(result)

    def test_module_full(self):
        code = """module com.app {
            requires transitive java.sql;
            requires java.logging;
            exports com.app.api;
            exports com.app.spi to com.app.client;
            opens com.app.internal to com.app.framework;
            uses com.app.spi.Service;
            provides com.app.spi.Service with com.app.internal.Impl;
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)


class AnonymousDiamondTest(unittest.TestCase):
    """Java 9 diamond operator with anonymous class"""

    def test_anonymous_diamond(self):
        code = """import java.util.*;
        class T {
            List<String> list = new ArrayList<>() {};
        }"""
        result = parse.parse(code)
        self.assertIsNotNone(result)
