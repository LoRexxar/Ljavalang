import unittest

import javalang


class TestRestrictedKeywords(unittest.TestCase):
    """The directives of a module declaration are restricted keywords.

    Inside a module declaration they are directives. Everywhere else they are
    ordinary identifiers, and Java programs do use them as method and variable
    names - Jackson's ``reader.readerFor(Map.class).with(schema)`` being the
    case that brought this up. Tokenising them as keywords made any such file
    fail to parse, with the error reported at an unrelated token earlier in the
    statement.
    """

    DIRECTIVES = ['requires', 'exports', 'opens', 'to', 'uses', 'provides',
                  'with', 'transitive']

    def test_directive_as_method_name(self):
        for name in self.DIRECTIVES:
            with self.subTest(name=name):
                javalang.parse.parse(
                    'class T { void m() { a.%s(b); } }' % name)

    def test_directive_as_variable_name(self):
        for name in self.DIRECTIVES:
            with self.subTest(name=name):
                javalang.parse.parse('class T { int %s = 1; }' % name)

    def test_directive_as_declared_method(self):
        for name in self.DIRECTIVES:
            with self.subTest(name=name):
                javalang.parse.parse('class T { void %s() {} }' % name)

    def test_chained_call_on_generic_declaration(self):
        # The shape that occurs in the wild, and the one whose error message
        # points at the type rather than at the identifier.
        javalang.parse.parse(
            'class T { void m() {'
            ' MappingIterator<Map<String, String>> r ='
            ' mapper.readerFor(Map.class).with(schema).readValues(file); } }')

    def test_module_declaration_still_parses(self):
        # The parser accepts the directives by value, so dropping them from the
        # keyword set leaves module declarations readable.
        javalang.parse.parse(
            'module com.example {'
            ' requires transitive java.base;'
            ' exports com.a to com.b;'
            ' opens com.c;'
            ' uses com.S;'
            ' provides com.A with com.B; }')


if __name__ == "__main__":
    unittest.main()
