# Ljavalang

> 感谢AI时代吧，停止维护的项目可以以非常极低成本的方式继续维护。
> [javalang](https://github.com/c2nes/javalang) 的增强版本，修复上游 AST 构造缺陷并支持 Java 9-22 新语法

[![PyPI](https://img.shields.io/pypi/v/ljavalang?color=blue)](https://pypi.org/project/ljavalang/)
[![Python](https://img.shields.io/pypi/pyversions/ljavalang)](https://pypi.org/project/ljavalang/)
[![GitHub Actions](https://github.com/LoRexxar/Ljavalang/actions/workflows/tests.yml/badge.svg?branch=develop)](https://github.com/LoRexxar/Ljavalang/actions/workflows/tests.yml)

## 安装

```bash
pip install ljavalang
```
代码中仍然 `import javalang` 使用，与上游完全兼容。

## 快速开始

```python
>>> import javalang
>>> tree = javalang.parse.parse('package com.example; class Test {}')
>>> tree.package.name
'com.example'
>>> tree.types[0].name
'Test'
```

### 新语法示例

**Java 14 switch expression：**
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
>>> # return 语句中的表达式是 SwitchExpression
>>> tree.types[0].body[0].body[0].expression
SwitchExpression
```

**Java 16 record：**
```python
>>> tree = javalang.parse.parse('record Point(int x, int y) {}')
>>> tree.types[0]
RecordDeclaration
>>> tree.types[0].name
'Point'
```

**Java 21 record pattern：**
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
>>> javalang.parse.parse(code)  # 正常解析
```

**链式调用（核心 bug 修复）：**
```python
>>> code = 'class T { void m(String cmd) { Runtime.getRuntime().exec(cmd); } }'
>>> tree = javalang.parse.parse(code)
>>> # 上游会把 exec 错误地放入 selectors 列表
>>> # Ljavalang 正确解析为嵌套的 MethodInvocation 限定符链
```

### Visitor 模式遍历

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

### Token 位置范围

```python
from javalang.tokenizer import tokenize

code = 'int x = 42;'
for token in tokenize(code):
    r = token.position.range
    print(f'{token.value} -> code[{r.start}:{r.stop}] = {code[r]!r}')
# int -> code[0:3] = 'int'
# x -> code[4:5] = 'x'
# = -> code[6:7] = '='
# 42 -> code[8:10] = '42'
```

### AST 节点 end_position

```python
>>> code = 'class T { void m() { try { int x = 1; } catch (Exception e) {} } }'
>>> tree = javalang.parse.parse(code)
>>> tree.types[0].end_position
Position(line=1, column=66, range=slice(65, 66, None))
>>> tree.types[0].body[0].end_position  # MethodDeclaration
Position(line=1, column=64, range=slice(63, 64, None))
```

## 支持的 Java 语法特性

<details>
<summary>完整列表（点击展开）</summary>

### Java 8（上游已支持）
- Lambda 表达式
- 方法引用
- 类型注解
- 接口 default/static 方法
- 通用 try-with-resources
- Receiver parameter（`Inner.this` 参数）

### Java 9
- `try`-with-resources effectively final 变量
- `module-info.java`（module / open module / requires / exports / opens / uses / provides）
- 接口 private 方法
- 匿名类 diamond 操作符

### Java 10-11
- `var` 局部变量类型推断
- `var` 在 for-each / try-with-resources 中
- `var` 在 lambda 参数中

### Java 14
- Switch expression（`case X ->` 箭头语法）
- Switch expression 表达式级别（`return switch(...)` / 赋值右值）
- 多标签 case（`case 1, 2, 3 ->`）
- `yield` 语句
- Pattern matching `instanceof`（`obj instanceof String s`）

### Java 15
- Text block（`"""..."""` 三引号字符串）

### Java 16
- `record` 类声明
- 局部 record / enum（方法体内）
- record 作为类成员

### Java 17
- `sealed` class / interface
- `permits` 子句
- `non-sealed` 修饰符

### Java 21
- Pattern matching switch（`case String s ->`）
- Record pattern 解构（`case Point(int x, int y) ->`）
- 嵌套 record pattern
- `case null` 匹配

### Java 22
- Unnamed variable `_`
- Unnamed lambda 参数

</details>

## 项目结构

```
Ljavalang/
├── pyproject.toml    # 打包配置（PEP 621）
├── javalang/
│   ├── parse.py      # 入口：parse() / parse_expression() 等
│   ├── parser.py     # 递归下降解析器（~2800 行）
│   ├── tokenizer.py  # 词法分析器（~700 行）
│   ├── tree.py       # AST 节点定义（~340 行）
│   ├── visitor.py    # Visitor 模式遍历
│   └── test/         # 测试用例（112 个）
│       ├── test_java_9_syntax.py
│       ├── test_java_10_11_syntax.py
│       ├── test_java_14_15_syntax.py
│       ├── test_java_16_17_syntax.py
│       ├── test_java_21_syntax.py
│       ├── test_upstream_issues.py     # 上游 bug 回归测试
│       └── test_upstream_features.py   # 上游 feature 测试
└── docs/
    ├── changelog.md              # 版本变更记录
    ├── architecture.md           # 架构文档
    ├── java-version-roadmap.md   # 版本支持路线图
    ├── upstream-issues.md        # 151 个上游 issue 分类
    ├── upstream-prs.md           # 43 个上游 PR 分析
    └── issue-fix-progress.md    # 修复进度追踪
```

## 致谢

基于 [c2nes/javalang](https://github.com/c2nes/javalang)（作者 Chris Thunes）开发

## License

MIT License
