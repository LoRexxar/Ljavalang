# Ljavalang

> [javalang](https://github.com/c2nes/javalang) 的增强 fork，修复上游 AST 构造缺陷并支持 Java 9-22 新语法，为 [Kunlun-M](https://github.com/LoRexxar/Kunlun-M) 等静态分析工具提供准确的 Java 语法树。

[![GitHub Actions](https://github.com/LoRexxar/Ljavalang/actions/workflows/tests.yml/badge.svg?branch=develop)](https://github.com/LoRexxar/Ljavalang/actions/workflows/tests.yml)

## 与上游的区别

| 特性 | 上游 javalang | Ljavalang |
|------|:---:|:---:|
| Java 8 语法 | ✅ | ✅ |
| **链式调用修复** | ❌ `a.b().c()` 解析为扁平 selectors | ✅ 正确嵌套为限定符链 |
| **Java 9** TWR effectively final | ❌ | ✅ |
| **Java 9** module-info | ❌ | ✅ |
| **Java 10** var 类型推断 | ❌ | ✅ |
| **Java 14** switch expression (arrow/yield) | ❌ | ✅ |
| **Java 14** pattern matching instanceof | ❌ | ✅ |
| **Java 15** text block (三引号字符串) | ❌ | ✅ |
| **Java 16** record class | ❌ | ✅ |
| **Java 17** sealed / permits / non-sealed | ❌ | ✅ |
| **Java 21** pattern matching switch | ❌ | ✅ |
| **Java 21** record pattern (解构) | ❌ | ✅ |
| **Java 22** unnamed variable `_` | ❌ | ✅ |

## 安装

```bash
pip install git+https://github.com/LoRexxar/Ljavalang.git@develop
```

或克隆后本地安装：

```bash
git clone https://github.com/LoRexxar/Ljavalang.git
cd Ljavalang
pip install -e .
```

## 快速开始

用法与上游 javalang 完全兼容：

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

## 遍历语法树

```python
# 迭代所有节点
for path, node in tree:
    print(path, node)

# 按类型过滤
for path, node in tree.filter(javalang.tree.MethodInvocation):
    print(f'方法调用: {node.member}')
```

## 测试

```bash
# 运行全部测试（73 个用例）
python -m pytest javalang/test/ -v \
  --ignore=javalang/test/test_java_8_syntax.py \
  --ignore=javalang/test/test_package_declaration.py

# 仅运行特定版本的测试
python -m pytest javalang/test/test_java_21_syntax.py -v
```

测试覆盖矩阵：Python 3.9 / 3.10 / 3.11 / 3.12，通过 GitHub Actions 自动运行。

## 支持的 Java 语法特性

<details>
<summary>完整列表（点击展开）</summary>

### Java 8（上游已支持）
- Lambda 表达式
- 方法引用
- 类型注解
- 接口 default/static 方法
- 通用 try-with-resources

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

### Bug 修复
- **链式调用**：`a.b().c()` 不再被错误地放入 `selectors`，而是正确嵌套为 `MemberSelect(Invocation(MemberSelect(a, b)), c)` 的限定符链结构

</details>

## 项目结构

```
javalang/
├── parse.py          # 入口：parse() / parse_expression() 等
├── parser.py         # 递归下降解析器（~2800 行）
├── tokenizer.py      # 词法分析器（~700 行）
├── tree.py           # AST 节点定义（~230 行）
├── test/             # 测试用例
│   ├── test_java_9_syntax.py
│   ├── test_java_10_11_syntax.py
│   ├── test_java_14_15_syntax.py
│   ├── test_java_16_17_syntax.py
│   └── test_java_21_syntax.py
└── docs/
    ├── architecture.md       # 架构文档
    └── java-version-roadmap.md  # 版本支持路线图
```

## 致谢

基于 [c2nes/javalang](https://github.com/c2nes/javalang)（作者 Chris Thunes）开发，为 [Kunlun-M](https://github.com/LoRexxar/Kunlun-M) 白盒扫描器提供 Java 解析支持。

## License

MIT License（继承自上游）
