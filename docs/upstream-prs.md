# 上游 PR 全面分析

> 分析 [c2nes/javalang/pulls](https://github.com/c2nes/javalang/pulls) 全部 43 个 PR，评估其对 Ljavalang 的价值。

## 统计

| 状态 | 数量 |
|------|------|
| 已合并 | 22 |
| Open | 19 |
| Closed（未合并） | 2（#138, #148 空 PR） |
| Fork 已删除（无内容） | 2（#151） |

## 已合并 PR（22 个）— 全部已包含在代码基础中

这些 PR 已被上游合并，Ljavalang 的代码基础已包含。

| PR | 标题 | 价值 | 状态 |
|----|------|------|------|
| #1 | Handle multiple author tags in javadoc | 低 | ✅ 已合并 |
| #2 | Expose position information | 中 | ✅ 已合并 |
| #3 | Add __version__ attribute | 低 | ✅ 已合并 |
| #4 | Make tokenizer accept all identifiers | 中 | ✅ 已合并 |
| #8 | Fix Javadoc detection for block comments | 中 | ✅ 已合并 |
| #9 | Fix broken code from #8 | 低 | ✅ 已合并 |
| #10 | Travis CI support | 低 | ✅ 已合并 |
| #11 | Python 3 support | 高 | ✅ 已合并 |
| #12 | Minor code fixup | 低 | ✅ 已合并 |
| #13 | Javadoc on package declarations | 低 | ✅ 已合并 |
| #18 | Initial Java 8 support | 高 | ✅ 已合并 |
| #22 | Fix parse_element_values list bug | 中 | ✅ 已合并 |
| #23 | Static/default methods in interfaces (Java 8) | 高 | ✅ 已合并 |
| #28 | Fix SuperMethodInvocation empty args | 中 | ✅ 已合并 |
| #31 | Allow interfaces to have optional body | 中 | ✅ 已合并 |
| #38 | Add position information to nodes | 高 | ✅ 已合并 |
| #48 | Fix fields/methods on EnumDeclaration | 中 | ✅ 已合并 |
| #50 | Fix IndexError reading identifier at line end | 中 | ✅ 已合并 |
| #51 | Option to ignore tokenization errors | 低 | ✅ 已合并 |
| #55 | Fix token position with inline comments | 中 | ✅ 已合并 |
| #62 | Allow line comments without final newline | 中 | ✅ 已合并 |
| #70 | Add _position to many entities | 高 | ✅ 已合并 |
| #71 | Update .travis.yml | 低 | ✅ 已合并 |

## Open PR（19 个）— 逐个分析

### ✅ PR #114 — fix prefix/postfix operators parse issue
- **改动**：`parser.py` 4 行，保留括号内子表达式的 prefix_operators，保护 postfix_operators
- **价值**：**HIGH** — 修真实 bug，括号内的 `!a` 会被丢掉 prefix
- **Ljavalang 状态**：✅ **已实现**（commit `864cd63`），方案完全一致

### ✅ PR #117 — Fix typo in DecimalInteger base type
- **改动**：`tokenizer.py` 1 行，`DecimalInteger(Literal)` → `DecimalInteger(Integer)`
- **价值**：**HIGH** — 类型继承层级 bug
- **Ljavalang 状态**：✅ **已实现**（commit `65685fd`）

### ✅ PR #100 — Expose a token's underlying input range
- **改动**：`tokenizer.py` 2 行，`Position` namedtuple 加 `range` 字段
- **价值**：**HIGH** — 静态分析工具需要 token 的源码位置范围
- **Ljavalang 状态**：✅ **已实现**（commit `864cd63`），方案完全一致

### ✅ PR #133 — Add a Visitor class
- **改动**：新增 `visitor.py` 265 行，标准 visitor pattern
- **价值**：**MEDIUM** — 方便 AST 遍历，但对核心解析无影响
- **Ljavalang 状态**：✅ **已实现**（commit `864cd63`），精简版

### ✅ PR #137 — Update tokenizer.py
- **改动**：`tokenizer.py` 6 行，tokenize 方法添加 `return_index` 参数
- **价值**：**MEDIUM** — 与 #100 互补，提供原始索引
- **Ljavalang 状态**：✅ **已实现**（commit `864cd63`）

### 🔶 PR #127 — Fix tokenizer bug with decimal number at end
- **改动**：`tokenizer.py` 3 行，`read_integer_or_float` 中 `c_next is None` 时走 decimal 路径
- **价值**：**MEDIUM** — 修复 `42`（输入以数字结尾）的边界 bug
- **Ljavalang 状态**：当前测试通过，但修复是防御性的，**值得合并**

### 🔶 PR #66 — Expose position to TryStatement
- **改动**：`parser.py` 6 行，TryStatement 创建时捕获变量再赋 position
- **价值**：**MEDIUM** — TryStatement 需要 `_position` 信息
- **Ljavalang 状态**：**需要检查**，TryStatement 可能缺失 position

### 🔶 PR #120 — end_position for TryStatement and CatchClause
- **改动**：`parser.py` + `tree.py` 16 行，给 TryStatement/CatchClause 添加 `end_position`
- **价值**：**MEDIUM** — 静态分析需要知道语句结束位置
- **Ljavalang 状态**：**未实现**，但 Ljavalang 的 `_position` 体系已覆盖 start

### 🔶 PR #131 — end position for ClassDeclaration/ConstructorDeclaration
- **改动**：`parser.py` + `tree.py` 22 行，给 ClassDeclaration/ConstructorDeclaration 添加 `end_position`
- **价值**：**MEDIUM** — 与 #120 同系列的 position 改进
- **Ljavalang 状态**：**未实现**

### ⬜ PR #92 — assign MemberReference.member full Keyword + position info
- **改动**：`parser.py` 56 行 + `tree.py` 16 行，将 `parse_identifier` 返回值从 string 改为 `Identifier` 对象，`parse_qualified_identifier` 返回 `QualifiedIdentifier` 对象
- **价值**：**MEDIUM** — 但 **破坏性巨大**（改变所有 `identifier` 返回类型从 str 到对象）
- **Ljavalang 状态**：**不建议合并** — 会破坏所有依赖 string 返回值的下游代码

### ⬜ PR #94 — Fix for empty compilation unit + start/end position
- **改动**：`parser.py` 118 行 + 新增 test 305 行，给所有 AST 节点添加 `start_position`/`end_position`，修复空编译单元 bug
- **价值**：**MEDIUM-HIGH** — position 信息对分析工具很重要
- **Ljavalang 状态**：**部分覆盖**（已有 `_position`/`Position.range`），但 end_position 体系未建立。空编译单元 bug 需验证

### ⬜ PR #96 — Store unicode string as raw string
- **改动**：`tokenizer.py` 删除 60 行 `pre_tokenize` 方法，不再做 unicode 转义替换
- **价值**：**LOW** — 测试显示 Ljavalang 已正常处理 unicode；删除 pre_tokenize 可能引入新问题
- **Ljavalang 状态**：**不建议合并** — 当前 unicode 处理正常

### ⬜ PR #97 — Large changeset for parsing a large test set
- **改动**：6 个文件，566 行新增/265 行删除。核心改动：给 `Node.__init__` 加 `Extraneous arguments` 错误信息、大量 parser 修复
- **价值**：**HIGH** 但 **风险极高** — 改动量太大，无法增量合并
- **Ljavalang 状态**：**后续评估** — 需单独分析每个子修复

### ⬜ PR #104 — Update parser.py (selectors fix)
- **改动**：`parser.py` 6 行，保护 `primary.selectors` 不被空 list 覆盖
- **价值**：**LOW-MEDIUM** — Ljavalang 的链式调用修复已从根本解决了这个问题
- **Ljavalang 状态**：**不需要** — 核心链式调用 bug 已用更好方案解决

### ⬜ PR #25 — Java 8 toArray + interface default/static methods + Position class
- **改动**：5 个文件 209 行，添加 Position 类（start/end）、Java 8 接口方法增强
- **价值**：**LOW** — 依赖上游旧版代码基础，与 Ljavalang 架构冲突（我们用 namedtuple Position）
- **Ljavalang 状态**：**不需要** — Java 8 接口方法已支持，Position 方案不同

### ⬜ PR #51 — Option to ignore errors on tokenization
- **改动**：`tokenizer.py` 存储错误到列表而非抛异常
- **价值**：**LOW** — 掩盖错误不利调试
- **Ljavalang 状态**：**拒绝**

### ⬜ PR #74 — Replace deprecated test methods
- **改动**：`test_package_declaration.py` 15 行，`failUnless` → `assertTrue`
- **价值**：**LOW** — 仅测试风格
- **Ljavalang 状态**：**不需要** — 我们跳过该测试文件

## Closed 未合并 PR（4 个）

### PR #32 — Default package name
- **价值**：LOW — 语义改动，上游拒绝了

### PR #138 — Fixed test cases and workflow
- **价值**：LOW — 空 PR，fork 已删除

### PR #148 — Add end_position for each Node
- **价值**：MEDIUM — 与 #94/#120/#131 同方向，但 fork 已删除无法获取代码

### PR #151 — Update from Java 8 to 17
- **价值**：HIGH — 但 fork 已删除，无法获取代码。Ljavalang 已独立实现了 Java 9-22 支持

## 值得合并到 Ljavalang 的 PR

| PR | 改动 | 优先级 | 说明 |
|----|------|--------|------|
| #127 | tokenizer c_next None 保护 | HIGH | 3 行，防御性修复 |
| #66 | TryStatement position | MEDIUM | 6 行，补齐 position |
| #120 | end_position for TryStatement/Catch | MEDIUM | 16 行 |
| #131 | end_position for Class/Constructor | MEDIUM | 22 行 |
| #94 | 空编译单元 + position 体系 | LOW | 118 行，风险较大 |
| #97 | 大规模修复 | LOW | 566 行，需逐个分析子修复 |
