# Ljavalang 高版本 Java 语法支持计划

## 当前支持现状

### 已支持（无需修改）
| 特性 | Java 版本 | 说明 |
|------|----------|------|
| private interface methods | Java 9 | 解析器已允许 private 修饰接口方法 |
| underscore identifier `_` | Java 8+ | 作为普通标识符处理（Java 9 起应为关键字错误） |
| diamond operator in anonymous class | Java 9 | `new ArrayList<>(){}` 已能解析 |
| var 局部变量类型推断 | Java 10 | `var` 不在关键字列表中，作为标识符正常解析 |
| var in lambda | Java 11 | `(var x) -> ...` 正常解析 |

### 需要新增支持
| 特性 | Java 版本 | 复杂度 | 涉及文件 |
|------|----------|--------|---------|
| **try-with-resources effectively final** | Java 9 | ⭐ 低 | parser.py |
| **module-info 解析** | Java 9 | ⭐⭐⭐ 高 | tokenizer.py, parser.py, tree.py |
| **switch expression (arrow + yield)** | Java 14 | ⭐⭐⭐ 高 | tokenizer.py, parser.py, tree.py |
| **pattern matching instanceof** | Java 14/16 | ⭐⭐ 中 | parser.py, tree.py |
| **text block (三引号字符串)** | Java 15 | ⭐⭐ 中 | tokenizer.py |
| **record class** | Java 16 | ⭐⭐ 中 | parser.py, tree.py |
| **sealed class / permits** | Java 17 | ⭐⭐ 中 | tokenizer.py, parser.py, tree.py |
| **pattern matching switch** | Java 21 | ⭐⭐⭐ 高 | parser.py, tree.py |

---

## 实施路线

### Phase 1: Java 9（预计改动：~150 行）

#### 1.1 try-with-resources effectively final（低复杂度）
**语法**：`try (existingVar) { ... }` — 不声明新变量，直接使用已存在的 effectively final 变量

**当前行为**：解析器期望 `try (` 后跟类型声明，遇到标识符时报错

**修改方案**：
- `parse_resource()` (第 1603 行)：增加分支，当遇到 `Identifier` 且后面没有 `=` 或类型声明时，直接解析为变量引用

#### 1.2 module-info 解析（高复杂度）
**语法**：
```java
module com.example.app {
    requires java.base;
    requires transitive java.sql;
    exports com.example.api;
    exports com.example.internal to com.example.client;
    opens com.example.model;
    uses com.example.Service;
    provides com.example.Service with com.example.Impl;
}
```

**修改方案**：
- **tokenizer.py**：新增关键字 `module`, `requires`, `transitive`, `exports`, `opens`, `to`, `uses`, `provides`, `with`
- **tree.py**：新增节点 `ModuleDeclaration`, `RequiresDirective`, `ExportsDirective`, `OpensDirective`, `UsesDirective`, `ProvidesDirective`
- **parser.py**：新增 `parse_module_declaration()` 及子方法，在 `parse_compilation_unit()` 中检测 module 关键字

#### 1.3 underscore 关键字（低复杂度，可选）
**说明**：Java 9 起 `_` 是保留关键字，不能作为标识符。当前作为标识符解析。

**修改方案**：
- **tokenizer.py**：将 `_` 识别为特殊 token 或在 parser 中增加校验
- 此项优先级低，不影响 AST 正确性

---

### Phase 2: Java 14（预计改动：~200 行）

#### 2.1 switch expression（高复杂度）
**语法**：
```java
// arrow style
int result = switch(x) {
    case 1 -> 10;
    case 2, 3 -> 20;
    default -> 0;
};
// colon style with yield
int result = switch(x) {
    case 1: yield 10;
    default: yield 0;
};
```

**修改方案**：
- **tokenizer.py**：新增关键字 `yield`，运算符 `->`
- **tree.py**：新增 `SwitchExpression`, `SwitchExpressionCase`
- **parser.py**：
  - 新增 `parse_switch_expression()`
  - `parse_expression_2()` 中将 switch 识别为表达式
  - 支持 `->` case label
  - 支持 `yield` 语句

#### 2.2 pattern matching instanceof（中复杂度）
**语法**：`if (obj instanceof String s) { ... }`

**修改方案**：
- **tree.py**：给 instanceof 操作增加可选的 pattern 变量（`ReferenceType` 已有 `name`，需扩展或新增 `TypeTestPattern` 节点）
- **parser.py**：`parse_expression_2()` 中 instanceof 后允许跟类型 + 标识符

---

### Phase 3: Java 15（预计改动：~50 行）

#### 3.1 text block 三引号字符串
**语法**：`String s = """hello\nworld""";`

**修改方案**：
- **tokenizer.py**：在字符串字面量解析中识别 `"""` 开头，读取到匹配的 `"""` 为止

---

### Phase 4: Java 16（预计改动：~100 行）

#### 4.1 record class
**语法**：`record Point(int x, int y) { }`

**修改方案**：
- **tokenizer.py**：新增关键字 `record`
- **tree.py**：新增 `RecordDeclaration` 节点
- **parser.py**：`parse_type_declaration()` 中识别 `record`，新增 `parse_record_declaration()`

---

### Phase 5: Java 17（预计改动：~80 行）

#### 5.1 sealed class / permits
**语法**：
```java
sealed class Shape permits Circle, Square {}
non-sealed class Circle extends Shape {}
final class Square extends Shape {}
```

**修改方案**：
- **tokenizer.py**：新增关键字 `sealed`, `non-sealed`, `permits`
- **tree.py**：`ClassDeclaration` 增加 `permits` 属性
- **parser.py**：解析类声明时识别 sealed/non-sealed 修饰符和 permits 子句

---

### Phase 6: Java 21+（预计改动：~150 行）

#### 6.1 pattern matching switch
**语法**：
```java
switch(obj) {
    case Integer i -> ...
    case String s when s.length() > 5 -> ...
    default -> ...
}
```

**修改方案**：
- **tree.py**：新增 `GuardPattern`（case with guard condition）
- **parser.py**：扩展 switch case 解析支持类型模式 + guard

---

## 总览

| Phase | 版本 | 核心特性 | 预计改动量 |
|-------|------|---------|-----------|
| 1 | Java 9 | module-info + try-with-resources | ~150 行 |
| 2 | Java 14 | switch expression + pattern instanceof | ~200 行 |
| 3 | Java 15 | text block | ~50 行 |
| 4 | Java 16 | record | ~100 行 |
| 5 | Java 17 | sealed class | ~80 行 |
| 6 | Java 21 | pattern matching switch | ~150 行 |

**建议实施顺序**：Phase 1 → Phase 4 → Phase 5 → Phase 2 → Phase 3 → Phase 6
（先做简单且独立的特性，再做复杂的 switch expression）
