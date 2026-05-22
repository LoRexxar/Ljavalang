# Ljavalang

[![PyPI](https://img.shields.io/pypi/v/ljavalang?color=blue)](https://pypi.org/project/ljavalang/)
[![Python](https://img.shields.io/pypi/pyversions/ljavalang)](https://pypi.org/project/ljavalang/)
[![GitHub Actions](https://github.com/LoRexxar/Ljavalang/actions/workflows/tests.yml/badge.svg?branch=develop)](https://github.com/LoRexxar/Ljavalang/actions/workflows/tests.yml)

**[English](README.md)** | [中文](README.zh.md)

> Enhanced fork of [javalang](https://github.com/c2nes/javalang) — fixes core AST bugs, adds Java 9-22 syntax support, zero external dependencies.

## Installation

```bash
pip install ljavalang
```

The package name is `ljavalang` on PyPI, but the import name remains `javalang` — fully compatible with upstream.

## Quick Start

```python
>>> import javalang
>>> tree = javalang.parse.parse('package com.example; class Test {}')
>>> tree.package.name
'com.example'
>>> tree.types[0].name
'Test'
```

### New Syntax Examples

**Java 14 switch expression:**
```python
>>> code = '''
... class T {
...     int m(int x) {
...         return switch(x) {
...             case 1 -> 10;
...             case 2 -> 20;
...             default -> 0;
...         };
...     }
... }'''
>>> tree = javalang.parse.parse(code)
>>> tree.types[0].body[0].body[0].expression
SwitchExpression
```

**Java 16 record:**
```python
>>> tree = javalang.parse.parse('record Point(int x, int y) {}')
>>> tree.types[0]
RecordDeclaration
```

**Java 21 record pattern:**
```python
>>> code = '''
... class T {
...     record Point(int x, int y) {}
...     void m(Object o) {
...         switch(o) {
...             case Point(int x, int y) -> System.out.println(x + y);
...             default -> {}
...         }
...     }
... }'''
>>> javalang.parse.parse(code)  # parses successfully
```

**Chained method calls (core bug fix):**
```python
>>> code = 'class T { void m(String cmd) { Runtime.getRuntime().exec(cmd); } }'
>>> tree = javalang.parse.parse(code)
>>> # Upstream incorrectly places exec in a flat selectors list
>>> # Ljavalang correctly builds nested MethodInvocation qualifier chain
```

### Visitor Pattern

```python
from javalang.visitor import JavaVisitor

class MethodCollector(JavaVisitor):
    def __init__(self):
        self.methods = []

    def visit_MethodDeclaration(self, node):
        self.methods.append(node.name)
        self.generic_visit(node)

collector = MethodCollector()
collector.visit(tree)
print(collector.methods)  # ['foo', 'bar', ...]
```

### Token Position Range

```python
from javalang.tokenizer import tokenize

code = 'int x = 42;'
for token in tokenize(code):
    r = token.position.range
    print(f'{token.value} -> code[{r.start}:{r.stop}] = {code[r]!r}')
# int -> code[0:3] = 'int'
# x -> code[4:5] = 'x'
```

### AST Node end_position

```python
>>> code = 'class T { void m() { try { int x = 1; } catch (Exception e) {} } }'
>>> tree = javalang.parse.parse(code)
>>> tree.types[0].end_position
Position(line=1, column=66, range=slice(65, 66, None))
```

## Supported Java Syntax

<details>
<summary>Full list (click to expand)</summary>

### Java 8 (upstream)
- Lambda expressions
- Method references
- Type annotations
- Interface default/static methods
- Generic try-with-resources
- Receiver parameter (`Inner.this`)

### Java 9
- try-with-resources with effectively final variables
- module-info.java (module / open module / requires / exports / opens / uses / provides)
- Interface private methods
- Anonymous class diamond operator

### Java 10-11
- `var` local variable type inference
- `var` in for-each / try-with-resources
- `var` in lambda parameters

### Java 14
- Switch expression (`case X ->` arrow syntax)
- Switch expression at expression level (`return switch(...)`)
- Multi-label case (`case 1, 2, 3 ->`)
- `yield` statement
- Pattern matching `instanceof` (`obj instanceof String s`)

### Java 15
- Text block (`"""..."""` triple-quoted strings)

### Java 16
- `record` class declaration
- Local record / enum (inside method body)
- Record as class member

### Java 17
- `sealed` class / interface
- `permits` clause
- `non-sealed` modifier

### Java 21
- Pattern matching switch (`case String s ->`)
- Record pattern deconstruction (`case Point(int x, int y) ->`)
- Nested record patterns
- `case null` matching

### Java 22
- Unnamed variable `_`
- Unnamed lambda parameters

</details>

## Key Changes from Upstream

| Category | Details |
|----------|---------|
| **Core bug fix** | Chained method calls now produce nested `MethodInvocation` qualifier chains instead of flat `selectors` lists |
| **Bug fixes** | 6 upstream bugs fixed: #90/#117 (DecimalInteger), #145 (Character token), #81/#112 (type annotations), #141 (void return_type) |
| **New features** | end_position for 6 AST nodes, Visitor class, Position.range, tokenize return_index, ReceiverParameter, prefix/postfix operators |
| **Dependencies** | Zero external dependencies (removed `six`) |
| **Packaging** | Modern `pyproject.toml` (PEP 621), setuptools ≥64.0 |
| **Tests** | 112 pytest tests (Python 3.9-3.12 CI matrix) |

## Project Structure

```
Ljavalang/
├── pyproject.toml    # Packaging (PEP 621)
├── javalang/
│   ├── parse.py      # Entry: parse() / parse_expression()
│   ├── parser.py     # Recursive descent parser (~2800 lines)
│   ├── tokenizer.py  # Lexer (~700 lines)
│   ├── tree.py       # AST node definitions (~340 lines)
│   ├── visitor.py    # Visitor pattern traversal
│   └── test/         # 112 test cases
└── docs/
    ├── changelog.md
    └── architecture.md
```

## Credits

Based on [c2nes/javalang](https://github.com/c2nes/javalang) by Chris Thunes.

## License

MIT License
