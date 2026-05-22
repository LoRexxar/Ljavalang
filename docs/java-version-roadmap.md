# Ljavalang 高版本 Java 语法支持计划

## 当前支持现状

### 已支持（无需修改）
| 特性 | Java 版本 | 说明 |
|------|----------|------|
| private interface methods | Java 9 | 解析器已允许 private 修饰接口方法 |

### 已实现（develop 分支）
| 特性 | Java 版本 | 修改文件 | Commit |
|------|----------|---------|--------|
| try-with-resources effectively final | Java 9 | parser.py | `279ce89` |
| module-info 完整解析 | Java 9 | tokenizer.py, tree.py, parser.py | `279ce89` |
| switch arrow 语法 + yield | Java 14 | parser.py, tokenizer.py | `b3c414d` |
| pattern matching instanceof | Java 14 | parser.py | `98fc2f9` |
| text block 三引号字符串 | Java 15 | tokenizer.py | `c51d835` |
| record class | Java 16 | tree.py, parser.py | `279ce89` |
| sealed class/interface + permits | Java 17 | tokenizer.py, tree.py, parser.py | `279ce89` |
| non-sealed 修饰符 | Java 17 | parser.py | `d47f3ed` |
| pattern matching switch (语句级) | Java 21 | parser.py | `de0e7d6` |

### 待实现
| 特性 | Java 版本 | 说明 |
|------|----------|------|
| switch expression (表达式级) | Java 14 | `return switch(x) { ... }` 需修改 parse_primary |
| pattern matching switch (表达式级) | Java 21 | 依赖 switch expression |
| var 局部变量类型推断 | Java 10 | parser 中 var 识别为类型 |
| anonymous record | Java 16 | 较少使用 |
| deconstruction pattern | Java 21+ | preview feature |

## 新增 AST 节点

| 节点 | 父类 | 用途 |
|------|------|------|
| ModuleDeclaration | Node | Java 9 module 声明 |
| RequiresDirective | ModuleDirective | module requires 指令 |
| ExportsDirective | ModuleDirective | module exports 指令 |
| OpensDirective | ModuleDirective | module opens 指令 |
| UsesDirective | ModuleDirective | module uses 指令 |
| ProvidesDirective | ModuleDirective | module provides 指令 |
| RecordDeclaration | TypeDeclaration | Java 16 record 类 |
| SwitchExpression | Expression | Java 14 switch 表达式 |
| YieldStatement | Statement | Java 14 yield 语句 |
| TypeTestPattern | Node | Java 14/21 类型测试模式 |

## 新增关键字

| 关键字 | 类型 | Java 版本 |
|--------|------|----------|
| module | Keyword | Java 9 |
| requires | Keyword | Java 9 |
| exports | Keyword | Java 9 |
| opens | Keyword | Java 9 |
| to | Keyword | Java 9 |
| uses | Keyword | Java 9 |
| provides | Keyword | Java 9 |
| with | Keyword | Java 9 |
| transitive | Keyword | Java 9 |
| yield | Keyword | Java 14 |
| record | Keyword | Java 16 |
| sealed | Modifier | Java 17 |
| permits | Keyword | Java 17 |
| non-sealed | (三 token 组合) | Java 17 |

## 回归测试结果

36 项测试，34 项通过（94%）。2 项失败为 switch expression（表达式级别），属于后续任务。
