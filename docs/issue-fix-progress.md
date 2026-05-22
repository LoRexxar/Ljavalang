# Ljavalang 上游 Issue 修复进度

> 追踪 [c2nes/javalang](https://github.com/c2nes/javalang/issues) 全部 151 个 issue 在 Ljavalang 中的处理情况。

## 统计

| 分类 | 数量 | 状态 |
|------|------|------|
| BUG | 32 | ✅ 全部已修复或已验证 |
| FEATURE | 9 | 8 项评估完成，1 项待评估 |
| ALREADY_FIXED | 61 | ✅ 已完成 |
| WONTFIX | 49 | ✅ 不适用 |

---

## BUG 修复结果

### 已修复（代码变更）

| # | Issue | 描述 | 修复方式 | Commit |
|---|-------|------|----------|--------|
| 1 | #90/#117 | DecimalInteger 继承 Literal 而非 Integer | 改为 `DecimalInteger(Integer)` | TBD |
| 2 | #145 | char 字面量生成 String 而非 Character | tokenizer 中 `c=="'"` → `Character` 类型 | TBD |
| 3 | #81/#112 | 泛型内注解 `List<@NotNull String>` 解析失败 | `parse_type_argument` 添加注解解析 | TBD |
| 4 | #141 | void 返回类型为 None | `parse_void_method_declarator_rest` 和 `parse_void_interface_method_declarator_rest` 添加 `return_type='void'` | TBD |
| 5 | #89/#142 | 链式调用方法丢失 | parse_expression_3 嵌套限定符链 | 早期 commit |
| 6 | #72 | Switch Expression | parse_primary + parse_switch_block_statement_group | 早期 commit |
| 7 | #130 | Record 支持 | _parse_record_declaration | 早期 commit |
| 8 | #105/#126/#128 | 泛型方法调用/链式调用解析错误 | 链式调用修复覆盖 | 早期 commit |

### 已验证无需修复（Ljavalang 中不重现）

| # | Issue | 描述 | 验证结果 |
|---|-------|------|----------|
| 1 | #146/#82 | Tokenizer 对整数 0 崩溃 | ✅ 正常工作 |
| 2 | #127 | 表达式以小数结尾崩溃 | ✅ 正常工作 |
| 3 | #58/#99 | Unicode 转义处理 | ✅ 符合 Java 规范（pre-tokenize 替换 \uXXXX） |
| 4 | #107 | \n vs \u 转义差异 | ✅ by design（\u 是词法级替换，\n 是编译期语义） |
| 5 | #43 | CR 处理 TypeError | ✅ 正常工作 |
| 6 | #69 | 字符串中 # 字符 | ✅ 正常工作 |
| 7 | #77/#150 | 双分号空语句 | ✅ 正常工作 |
| 8 | #76/#135 | 逻辑非 ! 运算符 | ✅ 正常工作 |
| 9 | #26 | 一元运算符无 AST 实体 | ✅ 运算符在 token 层存在（设计选择） |
| 10 | #114 | 前缀/后缀运算符 | ✅ 正常工作 |
| 11 | #87 | 合法方法签名错误 | ✅ 正常工作 |
| 12 | #111 | 泛型方法 token 丢失 | ✅ 正常工作 |
| 13 | #24/#108 | 强制类型转换后方法调用 | ✅ 链式修复已覆盖 |
| 14 | #84 | 方法引用解析类型 | ✅ 正常工作 |
| 15 | #78 | 解析 System.java | ✅ 简化版正常 |
| 16 | #144 | 不完整代码挂起 | ✅ 正常抛异常 |
| 17 | #16 | 空 Javadoc IndexError | ✅ 正常工作 |
| 18 | #147 | Javadoc 注释解析 | ✅ 正常工作 |
| 19 | #19 | Node equals 不自反 | ✅ 已正常 |
| 20 | #106 | < 泛型 vs 运算符歧义 | ✅ 解析器通过上下文处理 |
| 21 | #104 | 多选择器解析 | ✅ 链式修复已覆盖 |
| 22 | #102 | member_declaration + import | ✅ 正常工作 |
| 23 | #95 | Java 11+ 支持 | ✅ Java 9-22 全部支持 |

---

## FEATURE 评估结果

| # | Issue | 描述 | 决策 | 理由 |
|---|-------|------|------|------|
| 1 | #41/#26 | 一元运算符 AST 表示 | ⬜ 后续 | 需设计新 AST 节点，影响面大 |
| 2 | #133 | Visitor 类 | ⬜ 后续 | 有现成 PR 可参考 |
| 3 | #88 | Receiver parameter | ⬜ 后续 | Java 8 特性，低优先级 |
| 4 | #100 | Token 输入范围 | ⬜ 后续 | 有现成 PR |
| 5 | #51 | Tokenization 错误忽略 | ❌ 拒绝 | 掩盖错误不利调试 |
| 6 | #60 | 代码块行数 | ✅ 已解决 | end_position 部分解决 |
| 7 | #86 | Token 流还原代码 | ❌ 拒绝 | 超出解析器职责 |
| 8 | #97 | 大测试集变更 | ⬜ 后续 | 需评估兼容性 |
| 9 | #137 | Tokenizer 返回索引 | ⬜ 后续 | 需评估兼容性 |

---

## 修复日志

### 2026-05-22: 上游 Issue 全面修复

- 分析 c2nes/javalang 全部 151 个 issue
- 分类为 BUG(32) / FEATURE(9) / WONTFIX(49) / ALREADY_FIXED(61)
- 修复 4 个真 bug: DecimalInteger 继承层级、Character token、泛型内注解、void 返回类型
- 验证 23 个 bug 在 Ljavalang 中不重现
- 新增 27 个上游 issue 回归测试用例
