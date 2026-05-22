# Changelog

All notable changes to Ljavalang are documented in this file.

## [v2.0.0] - 2026-05-22

### Java 9-22 语法支持

从上游 javalang 仅支持 Java 8，扩展到完整支持 Java 9 至 Java 22 的所有主要语法特性。

**Java 9**
- TWR effectively final 变量（`try (x) { ... }`）
- `module-info.java`（module / open module / requires / exports / opens / uses / provides）
- 接口 private 方法
- 匿名类 diamond 操作符

**Java 10-11**
- `var` 局部变量类型推断
- `var` 在 for-each / try-with-resources / lambda 参数中

**Java 14**
- Switch expression（`case X ->` 箭头语法 + 多标签 + `yield` 语句）
- Switch expression 表达式级（`return switch(...)` / `int y = switch(...)`）
- Pattern matching `instanceof`（`obj instanceof String s`）

**Java 15**
- Text block（`"""..."""` 三引号字符串）

**Java 16**
- `record` 类声明
- 局部 record / enum（方法体内定义）
- record 作为类成员声明

**Java 17**
- `sealed` class / interface + `permits` 子句
- `non-sealed` 修饰符

**Java 21**
- Pattern matching switch（`case String s ->`）
- Record pattern 解构（`case Point(int x, int y) ->`）
- 嵌套 record pattern
- `case null` 匹配

**Java 22**
- Unnamed variable `_`
- Unnamed lambda 参数

### 核心架构修复

- **链式调用 bug 修复**：`a.b().c()` 不再被错误地放入 `selectors` 扁平列表，而是正确嵌套为 `MethodInvocation` 限定符链。这是 Ljavalang 的核心改进，解决了静态分析工具（Kunlun-M）中大量 sink 漏报问题。

### 上游 Issue 全面修复

分析 c2nes/javalang 全部 151 个 issue，分类处理：

**已修复的 Bug（6 项，代码变更）**
- `#90`/`#117` — `DecimalInteger` 继承层级：改为继承 `Integer` 而非跳级 `Literal`
- `#145` — char 字面量 `'a'` 生成 `Character` token 类型
- `#81`/`#112` — 泛型内注解 `List<@NotNull String>` 解析支持（JSR 308 Type Annotations）
- `#141` — void 方法 `return_type` 返回 `'void'` 而非 `None`
- `#89`/`#142` — 链式方法调用丢失
- `#114`/`#41`/`#26` — prefix/postfix 一元运算符在括号子表达式中丢失

**已验证无需修复（26 项）**
- 包括 `#76`/`#135`（`!` 运算符）、`#77`/`#150`（空语句）、`#19`（`__equals__` 自反性）、`#107`（转义差异 by design）等——在 Ljavalang 中均不重现。

**已实现的 Feature（5 项）**
- `#88` — Java 8 receiver parameter 支持（`Inner.this` 参数）
- `#133` — 新增 `javalang.visitor.JavaVisitor` 类（标准 visitor pattern）
- `#100` — `Position` namedtuple 添加 `range` 字段（`slice(start, stop)`）
- `#137` — `tokenize()` 添加 `return_index` 参数
- `#114`/`#41` — prefix/postfix operators 保留

**已拒绝（2 项）**
- `#51` — tokenization 错误忽略选项（掩盖错误不利调试）
- `#86` — Token 流还原代码（超出解析器职责）

**后续评估（1 项）**
- `#97` — 大测试集变更（巨型重构 PR，需独立规划）

### 测试与 CI

- 新增 112 个测试用例，覆盖 Java 8-22 全版本语法、上游 issue 回归、feature 验证
- GitHub Actions CI：Python 3.9 / 3.10 / 3.11 / 3.12 矩阵，每次 commit/PR 自动运行
- 全版本回归测试 36/36 通过（100%）

### 文档

- 中文 README.md（对比表、新语法示例、项目结构）
- 架构文档 `docs/architecture.md`
- 版本路线图 `docs/java-version-roadmap.md`
- 上游 issue 分类 `docs/upstream-issues.md`（151 项完整分析）
- 修复进度追踪 `docs/issue-fix-progress.md`

---

## [v1.0.0] — 基于上游 javalang

上游 c2nes/javalang 最后版本，支持 Java 8 语法。
