# Ljavalang 项目架构文档

> 本文档基于 `develop` 分支（commit `b7e339f`），对 Ljavalang 的项目结构、核心模块、数据流进行梳理。
> Ljavalang 是 [javalang](https://github.com/c2nes/javalang) 的 fork，目标是修复上游的 AST 构造缺陷，为 Kunlun-M 的 Java 静态分析提供准确的语法树。

---

## 1. 项目概览

| 属性 | 值 |
|------|-----|
| 版本 | 0.13.0 |
| 语言 | Python 3 |
| 依赖 | `six` |
| 目标 | Java 8 源码解析（词法分析 + 语法分析 → AST） |
| 源码总行数 | ~3,800 行（不含测试） |

**与上游 javalang 的关系**：
- 上游 `c2nes/javalang` 自 2018 年起停止维护
- Ljavalang 在 develop 分支上修复链式调用 AST 嵌套问题
- master 分支与上游保持一致

---

## 2. 目录结构

```
Ljavalang/
├── javalang/                  # 核心包
│   ├── __init__.py            # 包入口（8行），导出 parser/parse/tokenizer/javadoc，版本号
│   ├── ast.py                 # AST 基础设施（86行），Node 元类 + 树遍历
│   ├── tree.py                # AST 节点定义（280行），所有 Java 语法节点的类声明
│   ├── tokenizer.py           # 词法分析器（637行），Java 源码 → Token 流
│   ├── parser.py              # 语法分析器（2,452行），Token 流 → AST
│   ├── parse.py               # 高层 API（53行），便捷解析函数
│   ├── javadoc.py             # Javadoc 解析器（120行）
│   ├── util.py                # 工具类（165行），LookAhead 迭代器
│   └── test/                  # 测试
│       ├── test_java_8_syntax.py    # Java 8 语法测试（241行）
│       ├── test_tokenizer.py        # 词法分析测试（192行）
│       ├── test_util.py             # 工具类测试（69行）
│       ├── test_package_declaration.py  # 包声明测试（61行）
│       ├── test_javadoc.py          # Javadoc 测试（14行）
│       └── source/                  # 测试用 Java 源文件
├── setup.py                   # 包安装配置
├── requirements.txt           # 依赖声明
├── LICENSE.txt                # MIT 许可证
├── README.rst                 # 说明文档
└── .travis.yml                # CI 配置
```

---

## 3. 核心模块详解

### 3.1 `tokenizer.py` — 词法分析器（637行）

**职责**：将 Java 源码字符串转换为 Token 流。

**Token 类型继承体系**：
```
JavaToken
├── EndOfInput               # 输入结束
├── Keyword                  # 关键字（50个，如 class/if/return）
│   ├── Modifier             # 修饰符（abstract/public/static 等）
│   └── BasicType            # 基本类型（int/boolean/char 等）
├── Literal                  # 字面量
│   ├── Integer → Decimal/Octal/Binary/Hex
│   ├── FloatingPoint → Decimal/Hex
│   ├── Boolean / Character / String / Null
├── Separator                # 分隔符（括号、逗号、分号等）
├── Operator                 # 运算符（算术、关系、逻辑、赋值等）
├── Annotation               # 注解标记（@）
└── Identifier               # 标识符
```

**核心类 `JavaTokenizer`**：
- `tokenize(source)` → 顶层函数，返回 Token 迭代器
- 基于 `re` 正则匹配逐字符扫描
- 每个 Token 携带 `value`、`position=(line, column)`、`javadoc`

### 3.2 `parser.py` — 语法分析器（2,452行）

**职责**：将 Token 流递归下降解析为 AST。

**这是整个项目最核心、最复杂的模块，占源码总量的 65%。**

#### 类结构

```
JavaParserBaseException
├── JavaSyntaxError          # 语法错误（含 description + at 位置）
└── JavaParserError          # 解析器内部错误

Parser                       # 核心解析器类
```

#### 关键方法分组

| 分组 | 方法 | 作用 |
|------|------|------|
| **入口** | `parse()` | 解析编译单元（CompilationUnit） |
| **声明** | `parse_class_or_interface_declaration` / `parse_enum_declaration` / `parse_normal_class_declaration` / `parse_normal_interface_declaration` / `parse_annotation_type_declaration` | 类/接口/枚举/注解声明 |
| **成员** | `parse_member_declaration` / `parse_method_or_field_declaraction` / `parse_constructor_declarator_rest` | 方法/字段/构造器声明 |
| **类型** | `parse_type` / `parse_reference_type` / `parse_basic_type` / `parse_type_arguments` / `parse_type_parameters` | 类型系统（含泛型） |
| **语句** | `parse_statement` / `parse_block` / `parse_if/for/while/do/switch/try/catch` | 各种控制流语句 |
| **表达式** | `parse_expression` → `parse_expressionl` → `parse_expression_2` → `parse_expression_3` | 表达式优先级递归（赋值→三元→二元→一元/主表达式） |
| **主表达式** | `parse_primary` / `parse_literal` / `parse_creator` | 字面量、对象创建、标识符 |
| **选择器** | `parse_selector` / `parse_identifier_suffix` | 方法调用后缀 `.method()` / `.field` / `[index]` |

#### 表达式解析优先级（从低到高）

```
parse_expression      → 赋值表达式（=, +=, ...）
parse_expressionl     → 三元表达式（? :）
parse_expression_2    → 二元运算（||, &&, |, ^, &, ==, <, >, +, *, ...）
parse_expression_3    → 一元前缀 + 主表达式 + 后缀（selectors/postfix）
parse_primary         → 字面量 / 标识符 / new / this / super / (expr) / lambda
```

#### develop 分支修复：链式调用 AST 嵌套（第 1888-1919 行）

**问题**：`parse_expression_3()` 中，链式方法调用（如 `a.b().c()`）的 `.b()` 和 `.c()` 被追加到 `primary.selectors` 列表，而非嵌套为 `qualifier`。导致 `filter(MethodInvocation)` 只能找到最外层调用，丢失内部方法。

**修复位置**：`parse_expression_3()` 方法末尾，return 之前。

**修复逻辑**：
1. 检测 `primary.selectors` 是否非空
2. 保存 `saved_selectors`，清空 `primary.selectors = []`
3. 依次遍历 `saved_selectors`，将每个 selector 的 `qualifier` 设为前一个结果节点
4. 返回最终的嵌套节点（最外层调用）
5. `selectors` 保留为空列表以保持向后兼容

```
修复前: Primary(qualifier="a", selectors=[MI("b"), MI("c")])
修复后: MI("c", qualifier=MI("b", qualifier=MemberRef("a")))
```

### 3.3 `tree.py` — AST 节点定义（280行）

**职责**：定义所有 Java 语法结构的 AST 节点类型。

**节点继承体系**：

```
Node（来自 ast.py）
├── CompilationUnit          # 编译单元（package + imports + types）
├── Import                   # 导入声明
├── PackageDeclaration       # 包声明
│
├── TypeDeclaration ← Declaration ← Documented
│   ├── ClassDeclaration     # 类声明
│   ├── EnumDeclaration      # 枚举声明
│   ├── InterfaceDeclaration # 接口声明
│   └── AnnotationDeclaration # 注解声明
│
├── Type
│   ├── BasicType            # int/boolean/char 等
│   └── ReferenceType        # 引用类型（含泛型参数和子类型）
│
├── Statement                # 语句基类
│   ├── IfStatement / WhileStatement / DoStatement / ForStatement
│   ├── ReturnStatement / ThrowStatement / BreakStatement / ContinueStatement
│   ├── TryStatement / SwitchStatement / SynchronizedStatement
│   ├── BlockStatement / StatementExpression / AssertStatement
│   └── CatchClause
│
├── Expression               # 表达式基类
│   ├── Assignment           # 赋值
│   ├── TernaryExpression    # 三元
│   ├── BinaryOperation      # 二元运算
│   ├── Cast                 # 类型转换
│   ├── MethodReference      # 方法引用（ClassName::method）
│   └── LambdaExpression     # Lambda 表达式
│
├── Primary ← Expression     # 主表达式（链式调用的核心）
│   ├── Literal              # 字面量
│   ├── This                 # this
│   ├── MemberReference      # 字段引用（obj.field）
│   ├── Invocation           # 方法调用基类
│   │   ├── MethodInvocation       # 方法调用（obj.method()）
│   │   ├── SuperMethodInvocation  # super.method()
│   │   ├── ExplicitConstructorInvocation  # new MyClass()
│   │   └── SuperConstructorInvocation      # super()
│   ├── SuperMemberReference # super.field
│   ├── Creator              # 对象创建基类
│   │   ├── ClassCreator     # new MyClass(args)
│   │   ├── InnerClassCreator # new Outer.Inner(args)
│   │   └── ArrayCreator     # new int[n]
│   ├── ClassReference       # MyClass.class
│   └── ArraySelector        # array[index]（Expression，不是 Primary）
│
├── VariableDeclaration / LocalVariableDeclaration / FieldDeclaration
├── FormalParameter / InferredFormalParameter
├── Annotation / ElementValuePair / ElementArrayValue
├── ForControl / EnhancedForControl
├── TryResource
├── SwitchStatementCase
├── EnumBody / EnumConstantDeclaration
└── AnnotationMethod
```

**Primary 的关键属性**（链式调用的核心）：

```python
class Primary(Expression):
    attrs = ("prefix_operators", "postfix_operators", "qualifier", "selectors")
```

- `qualifier`：调用者/所属对象（字符串或嵌套节点）
- `selectors`：后续的 `.method()` / `.field` / `[index]` 列表
- **develop 修复后**：`selectors` 为空，链式调用通过嵌套 `qualifier` 表达

### 3.4 `ast.py` — AST 基础设施（86行）

**职责**：提供 AST 节点的元编程基础设施。

| 组件 | 作用 |
|------|------|
| `MetaNode` (metaclass) | 自动收集继承链上的 `attrs`，子类无需重复声明父类属性 |
| `Node` | 所有 AST 节点的基类，提供 `__init__`/`__repr__`/`__iter__`/`filter`/`children` |
| `walk_tree(root)` | 深度优先遍历 AST，yield `(path, node)` 元组 |
| `dump(ast, file)` / `load(file)` | AST 序列化/反序列化（pickle） |

**核心方法**：
- `node.filter(SomeType)` → 遍历所有子节点，yield 匹配类型的节点
- `list(node)` → 遍历所有 `(path, node)` 对
- `node.children` → 返回所有属性值列表

### 3.5 `parse.py` — 高层 API（53行）

**职责**：提供便捷的解析入口函数。

| 函数 | 输入 | 输出 |
|------|------|------|
| `parse(s)` | 完整 Java 源码 | `CompilationUnit` |
| `parse_expression(exp)` | Java 表达式字符串 | `Expression` 节点 |
| `parse_member_signature(sig)` | 方法/字段签名 | `MethodDeclaration` / `FieldDeclaration` |
| `parse_constructor_signature(sig)` | 构造器签名 | `ConstructorDeclaration` |
| `parse_type(s)` | 类型字符串 | `Type` 节点 |
| `parse_type_signature(sig)` | 类型签名 | `ClassDeclaration` / `InterfaceDeclaration` |

### 3.6 `util.py` — 迭代器工具（165行）

**职责**：为 Parser 提供带 lookahead 和回溯能力的 Token 迭代器。

| 类 | 特点 |
|----|------|
| `LookAheadIterator` | 基于生成器的 lookahead，支持 push/pop marker（回溯） |
| `LookAheadListIterator` | 基于列表的 lookahead，随机访问更快，同支持 marker 回溯 |

**核心操作**：
- `look(i=0)` → 向前看第 i 个 token，不消耗
- `next()` → 消耗并返回下一个 token
- `push_marker()` / `pop_marker(reset)` → 保存/恢复读取位置（用于尝试性解析）

### 3.7 `javadoc.py` — Javadoc 解析器（120行）

**职责**：解析 Javadoc 注释为结构化的 `DocBlock` 对象。

支持的 Javadoc 标签：`@param`、`@return`、`@throws`/`@exception`、`@author`、`@deprecated`，以及任意自定义标签。

---

## 4. 数据流

```
Java 源码字符串
       │
       ▼
  tokenizer.py
  tokenize(source)
       │
       ▼
  Token 流 (Iterator[JavaToken])
       │
       ▼
  parser.py
  Parser(tokens).parse()
       │
       ▼
  CompilationUnit AST
  (tree.py 定义的节点树)
       │
       ├─→ ast.py: node.filter(MethodInvocation) 遍历
       ├─→ ast.py: walk_tree() 深度优先遍历
       └─→ ast.py: dump/load 序列化
```

**调用示例**：
```python
import javalang

# 完整编译单元
tree = javalang.parse.parse("class Foo { void bar() { Runtime.getRuntime().exec(cmd); } }")

# 单表达式
expr = javalang.parse.parse_expression("Runtime.getRuntime().exec(cmd)")

# 遍历所有方法调用
for path, node in tree.filter(javalang.tree.MethodInvocation):
    print(node.member, node.qualifier)
```

---

## 5. develop 分支变更

| 文件 | 变更 | 说明 |
|------|------|------|
| `parser.py` | +31 行（第 1888-1919 行） | 链式调用 AST 嵌套修复 |
| 其余文件 | 无变更 | 与 master 完全一致 |

**修复 commit**：`b7e339f` — fix(parser): 链式调用 AST 嵌套修复

---

## 6. 已知限制

1. **Java 版本**：仅支持 Java 8 语法，不支持 Java 9+ 的 module/var/record/sealed class 等
2. **`parse_primary` 的标识符处理**：`obj.field.method()` 中 `obj.field` 被解析为字符串 qualifier `"obj.field"`，而非嵌套的 `MemberReference`，这是 `parse_primary` 的设计选择（第 1989-2007 行），非 develop 分支引入
3. **Lambda 类型推断**：不支持 Lambda 参数的类型推断（`InferredFormalParameter`）
4. **注解处理**：仅解析注解语法，不处理注解语义

---

## 7. 与 Kunlun-M 的关系

```
Kunlun-M (requirements.txt: javalang>=0.13.0)
    │
    ├─ PyPI javalang 0.13.0（默认）
    │   └─ selectors 扁平列表
    │   └─ Kunlun-M parser.py 的 _flatten_chained_calls() 处理
    │
    └─ Ljavalang develop（可选替换）
        └─ selectors 嵌套为 qualifier
        └─ Kunlun-M _flatten_chained_calls() 返回单节点（selectors 为空）
```

当前 Kunlun-M 默认使用 PyPI javalang，链式调用兼容性由 Kunlun-M 侧的 `_flatten_chained_calls()` 保证。Ljavalang 的修复作为上游改进独立维护，未来可合并回 javalang 或直接作为依赖。
