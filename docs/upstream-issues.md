# Upstream javalang Issues Analysis

Classification of all issues (#1-#151) from [c2nes/javalang](https://github.com/c2nes/javalang).
Each issue was reviewed and categorized into one of: BUG, FEATURE, WONTFIX, or ALREADY_FIXED.

## Classification Summary

- **BUG**: 32 issues
- **FEATURE**: 9 issues
- **WONTFIX**: 49 issues
- **ALREADY_FIXED**: 61 issues

## Issues

### BUG

| # | Title | Description | Status |
|---|-------|-------------|--------|
| #16 | IndexError on empty Javadoc | IndexError on empty Javadoc with blank lines | Pending |
| #19 | Node __equals__ not reflexive | Node __equals__ not reflexive (AST design) | Pending |
| #24 | Method of a casted object not parsed | Method of casted object not parsed correctly | Pending - may be fixed with chain call fix |
| #26 | unary operators parsed but no has no corresponding entity or parameter | Unary operators parsed by tokenizer but not in AST | Pending |
| #43 | Uncaught TypeError: 'in <string>' requires string as left operand, not | TypeError with CR handling in lexer | Pending |
| #58 | String values don't properly handle unicode escapes | String values don't handle unicode escapes properly | Pending |
| #69 | Unable to parse '#' included in a string | Unable to parse # character in string literal | Pending |
| #76 | Can't recognize binary logical operator '!' | Can not recognize logical NOT ! operator in AST | Pending |
| #77 | If a statement has double semicolon in the end, The JavaSyntaxError wa | Double semicolons cause JavaSyntaxError | Pending |
| #78 | 解析lang包里的System.java会出现错误 | Error parsing java.lang.System.java (complex code) | Pending |
| #81 | private List<@Length(min = 0, max = NumberKeys.NUM_128) String> member | Annotation inside generics causes parse error | Pending |
| #82 | Errors occurs when parsing 'i=0' | Tokenizer error on i=0 expression | Pending |
| #84 | userIdList.stream().map(AnonymizeUtil::anonyAll) The anonyAll method i | Method reference parsed as MemberReference instead of MethodInvocation | Pending |
| #87 | JavaSyntaxError raised for unknown reasons | JavaSyntaxError on valid method signature | Pending |
| #90 | `DecimalInteger` inherit `Literal` instead of `Integer` | DecimalInteger inherits Literal instead of Integer type | Pending |
| #99 | Faulty unicode escape handling leads to tokenizing failure | Faulty unicode escape handling causes tokenization failure | Pending |
| #102 | Why does Javalang gives error when calling parse.member_declaration me | member_declaration fails with import statements | Pending |
| #104 | Update parser.py | PR: Fix multi-selectors parsing issue | Pending |
| #106 | Tokenizer cannot distinguish between usage of "<" as separator (e.g. L | Tokenizer can not distinguish < as separator vs operator | Pending |
| #107 | Different value between '\n' and '\u' in string when tokenizing | Different handling of \n vs \u in string values | Pending |
| #111 | Missing token when parsing | Missing token when parsing generic method call | Pending |
| #112 | JavaSyntaxError when using annotation inside generics. | JavaSyntaxError with annotation inside generics | Pending |
| #114 | fix prefix/postfix operators parse issue | PR: Fix prefix/postfix operators parse issue | Pending |
| #117 | Fix typo in DecimalInteger base type | PR: Fix typo in DecimalInteger base type | Pending |
| #127 | Fix a bug when tokenize an InfixExpression ends with a decimal number | PR: Fix tokenizer crash on expression ending with decimal number | Pending |
| #135 | Invalid parsing the following java code | Invalid parsing of ! prefix operator in if condition | Pending |
| #141 | returns None instead of void for return type | Returns None instead of void for return type | Pending |
| #144 | Title: Issue with Parsing Incomplete Code Causing Hang in Javalang | Parser hangs on incomplete Java code | Pending |
| #145 | javalang.tokenizer.tokenize method does not generate the javalang.toke | Tokenizer does not generate Character token type for char literals | Pending |
| #146 | Tokenizer fails on expression ending in integer '0' | Tokenizer fails on expression ending in integer 0 | Pending |
| #147 | javalang无法解析获取/**格式的类注释 | Can not parse Javadoc class comments properly | Pending |
| #150 | Empty Statements (;;) ar ereported as parsing errors | Empty statements (;;) reported as parse errors | Pending |

### FEATURE

| # | Title | Description | Status |
|---|-------|-------------|--------|
| #41 | Unary Operators? | Unary operators should be represented in AST nodes | Pending |
| #51 | Option to ignore errors on tokenization. | PR: Option to ignore errors during tokenization | Pending |
| #60 | Feature request: get number of lines in a block? | Get number of lines in a code block | Pending - partially addressed by end_position |
| #86 | Add the way of restoring original java code by tokens stream. | Restore original Java code from token stream | Pending |
| #88 | Receiver parameter not supported? | Support receiver parameters (Java 8) | Pending |
| #97 | Changeset allowing to parse a large test set | PR: Changeset for parsing large test sets, round-trip parsing | Pending |
| #100 | Expose a token's underlying input range | PR: Expose token underlying input range | Pending |
| #133 | Add a Visitor class | PR: Add a Visitor class for AST traversal | Pending |
| #137 | Update tokenizer.py | PR: Return token index from tokenizer | Pending |

### ALREADY_FIXED

| # | Title | Description | Fix Note |
|---|-------|-------------|----------|
| #1 | Handle multiple author tags while parsing javadoc strings. | PR: Handle multiple author tags in Javadoc | Merged upstream |
| #2 | Expose position information | PR: Expose position information | Merged upstream |
| #3 | Add a __version__ attribute to javalang and | PR: Add __version__ attribute | Merged upstream |
| #4 | Make tokenizer accept (nearly) all identifiers | PR: Accept non-ASCII identifiers in tokenizer | Merged upstream |
| #6 | found a bug | Tokenizer escape_code variable reference bug | Fixed upstream |
| #7 | another bug | Javadoc detection applied to line comments | Fixed upstream (#8 merged) |
| #8 | Issue 7: Only attempt Javadoc detection for block comments | PR: Fix Javadoc detection for block comments only | Merged upstream |
| #9 | In #8 to fix issue #7 broken code was committed. The fix for the broke | PR: Fix broken code from #8 (missing and) | Merged upstream |
| #10 | Add Travis ci support | PR: Add Travis CI support | Merged upstream (CI) |
| #11 | Python 3 support | Python 3 support | Python 3 fully supported in Ljavalang |
| #12 | Minor code fixup | PR: Minor code fixup | Merged upstream |
| #13 | Include javadoc comments on package declarations | PR: Include Javadoc on package declarations | Merged upstream |
| #14 | Include position information in all AST nodes | Position info in all AST nodes | Ljavalang has comprehensive position support |
| #17 | Support java 8 syntax, such as lambda expressions  | Java 8 lambda expressions support | Java 8+ fully supported in Ljavalang |
| #18 | Initial Java 8 support | PR: Initial Java 8 support (lambdas, method refs) | Merged upstream, Java 8+ supported |
| #21 | JavaSyntaxError when using Java 8's stream.toArray | JavaSyntaxError with Stream.toArray (array constructor ref) | Java 8+ method/constructor refs supported |
| #22 | parse_element_values always returns a list with only the last value | PR: Fix parse_element_values returning only last value | Merged upstream |
| #23 | Add support for static and default methods in interfaces (Java 8) | PR: Static/default methods in interfaces (Java 8) | Merged upstream |
| #27 | SuperMethodInvocation mistakenly regarded as SuperMemberReference in c | SuperMethodInvocation misregarded as SuperMemberReference | Fixed upstream (#28 merged) |
| #28 | SuperMethodInvocation on empty args, misregarded as SuperMemberReferen | PR: Fix SuperMethodInvocation on empty args | Merged upstream |
| #29 | Javalang doesn't support Java8 `default` keyword. | Java 8 default keyword in interfaces | Java 8+ supported in Ljavalang |
| #30 | Javalang can not parse interfaces with a body. | Can not parse interfaces with body | Java 8+ interface support in Ljavalang |
| #31 | Allow interfaces to have an optional body, fix #30. | PR: Allow interfaces to have optional body | Merged upstream |
| #32 | Whithout package declaration, set the package name to 'default package | PR: Default package name when no declaration | Merged upstream |
| #38 | Add position information to nodes | PR: Add position information to nodes | Merged upstream |
| #47 | javalang.tree.EnumDeclaration fields and methods properties not workin | EnumDeclaration fields/methods not working | Fixed in upstream (#48 merged) |
| #48 | Fix fields and methods properties on EnumDeclaration | PR: Fix EnumDeclaration fields/methods | Merged upstream |
| #50 | Fix IndexError when reading identifier at the end of a line | PR: Fix IndexError reading identifier at end of line | Merged upstream |
| #53 | JavaSyntaxError parsing method reference | JavaSyntaxError parsing method reference Long[]::new | Java 8+ method refs supported |
| #54 | Error of token position of lines preceded by inline comments | Token position error after inline comments | Fixed upstream (#55 merged) |
| #55 | Error of token position of lines preceded by inline comments (issue #5 | PR: Fix token position after inline comments | Merged upstream |
| #61 | Error parsing line comment in last line with no final line break | Error parsing line comment at EOF without newline | Fixed upstream (#62 merged) |
| #62 | Allow line comments at the end of the file without a final line break | PR: Allow line comments at EOF without newline | Merged upstream |
| #66 | Expose position to TryStatement | PR: Expose position to TryStatement | Position support in Ljavalang |
| #70 | Adds _position field to many entities of the Java language | PR: Add _position field to many entities | Merged upstream |
| #71 | Update .travis.yml | PR: Update Travis CI Python versions | Merged upstream (CI) |
| #72 | Support Switch Expressions | Support Switch Expressions (JEP 361) | Fixed in Ljavalang - Java 9-22 support |
| #73 | `AssertStatement` doesn't have a position | AssertStatement doesn't have position | Position support in Ljavalang |
| #75 | InstanceOf Binary Operator doesn't have code line  | InstanceOf Binary Operator doesn't have code line | Position support in Ljavalang |
| #89 | Problem with chained method call | Chained method call qualifier bug | Fixed in Ljavalang - chain call bug resolved |
| #92 | Add position to ReferenceType | PR: Add position to ReferenceType | Position support in Ljavalang |
| #94 | Start position and End position | PR: Start position and End position | Ljavalang has end_position support |
| #95 | java 11+ support? | Java 11+ support request | Fixed in Ljavalang - Java 9-22 support |
| #96 | Store the unicode string as raw string | PR: Store unicode string as raw string | Fixed in Ljavalang |
| #98 | can't parse java8 lambada Reference to the constructor of the array | Can not parse array constructor reference in lambda | Java 8+ supported in Ljavalang |
| #105 | Unexpected behavior for generic method invocation with explicit typing | Generic method invocation with explicit typing parsed wrong | Fixed in Ljavalang - chain call fix |
| #108 | It cannot parse things like ((Type1) Var1).Method1() | Can not parse ((Type1) Var1).Method1() | Fixed in Ljavalang - chain call/cast fix |
| #109 | Is it possible to make the attribute 'position' of ast node public. | Make position attribute public | Position is public in Ljavalang |
| #120 | Implement end_position for MethodDeclaration() | PR: Implement end_position for MethodDeclaration | Ljavalang has end_position |
| #122 | JavaSyntaxError for Multiline Strings in Annotations | Multiline strings (text blocks) in annotations | Fixed in Ljavalang - Java 9-22 support |
| #126 | Error when parsing something like `Arrays.<Object> asList ( "a" , "b"  | Error parsing Arrays.<Object>asList generic invocation | Fixed in Ljavalang - chain call fix |
| #128 | Error when parsing statements that contain Cast(MemberRef).MethodInvo | Error parsing Cast(MemberRef).MethodInvo | Fixed in Ljavalang - chain call fix |
| #130 | Support records in parse_class_or_interface_declaration method | Support records in parser | Fixed in Ljavalang - record support |
| #131 | Added class end position, constructor end position (also includes prev | PR: Add class/constructor end position | Ljavalang has end_position |
| #138 | fixed tests cases and workflow | PR: Fixed test cases and workflow | Merged upstream (CI) |
| #139 | Error while parsing something like '(Annotation[]::new)' | Error parsing (Annotation[]::new) constructor reference | Java 8+ supported in Ljavalang |
| #142 | missing method invocation  | Missing method invocation in chained cast call | Fixed in Ljavalang - chain call bug resolved |
| #143 | JavaSyntaxError('') for (Enum::toString) & (Annotation[]::new) | JavaSyntaxError for Enum::toString and Annotation[]::new | Java 8+ supported in Ljavalang |
| #148 | feat(end_position): Add end_position for each Node, so it's now easy … | PR: Add end_position for each Node | Ljavalang has end_position |
| #149 | Constructor references  ar enot recongnized by the parser, they are re | Constructor references not recognized by parser | Java 8+ supported in Ljavalang |
| #151 | Update from Java 8 to 17 | PR: Update from Java 8 to 17 | Ljavalang supports Java 9-22 |

### WONTFIX

| # | Title | Description | Reason |
|---|-------|-------------|--------|
| #5 | Consider adding examples or some documentation  | Request for examples/documentation | Documentation request |
| #15 | Release a new version of javalang on pypi | Release new version on PyPI | Release management |
| #20 | Release a new version of javalang on pypi. | Release new version on PyPI (duplicate of #15) | Release management - duplicate |
| #25 | issue  #21(java8 .toArray) and defaults and static methods in interfac | PR: Multiple Java 8 fixes (superseded by other merged PRs) | Superseded |
| #33 | Questions about the library | General questions about the library | Usage question |
| #34 | Release new version? | Release new version with Java 8 support | Release management |
| #35 | SyntaxError: invalid syntax | SyntaxError: invalid syntax (user environment issue) | Out of scope |
| #36 | Full and flattened tree | How to get flattened tree | Usage question |
| #37 | Question : how to render a AST node | How to render AST node to string | Usage question |
| #39 | New Release? | New release for line number changes | Release management |
| #40 | Catching all assignments | How to capture all assignments | Usage question |
| #42 | Checking if two trees are equal | How to check if two trees are equal | Usage question |
| #44 | how to parse java code snippet to AST? | How to parse Java code snippets | Usage question |
| #45 | Is there a way to print a node to string? | How to print node to string | Usage question |
| #46 | How do I get a method's parameter's type? | How to get method parameter type | Usage question |
| #49 | extracting each methods in .java file | How to extract methods from Java file | Usage question |
| #52 | Array argument  | How to handle array arguments in AST | Usage question |
| #56 | How to parse a java file? | How to parse a Java file (beginner question) | Usage question |
| #57 | Is there anything associate the node  with tokens? | Associate nodes with tokens | Usage question |
| #59 | replace method with another  | Replace method with another in Java files | Usage question |
| #63 | Serialize output | Serialize AST to JSON/XML | Usage question |
| #64 | what's the meaning of attibution 'label' of Statement? | Meaning of label attribute on Statement | Usage question |
| #65 | how to traverse all  AST node?  | How to traverse all AST nodes | Usage question |
| #67 | getting line number | How to get line numbers | Usage question |
| #68 | Extracting source code of user defined methods from java file | Extract source code of methods from Java file | Usage question |
| #74 | Replace deprecated test methods | PR: Replace deprecated unittest methods | Test maintenance |
| #79 | Get class from MethodInvocation | Get class from MethodInvocation | Usage question |
| #80 | Get all methods' code | Get all methods code | Usage question |
| #83 | How to associate methods to a class in a java file | Associate methods to class in Java file | Usage question |
| #85 | Extracting all Methods in a Java File (i.e. myFile.Java) | Extract all methods in a Java file | Usage question |
| #91 | Can we use javalang to remove comments form java files? | Remove comments from Java files | Usage question |
| #93 | How to collect all classes in a java file in a hierarchical way? | Collect all classes hierarchically | Usage question |
| #101 | Change Java Source Code with Javalang | Change Java source code with javalang | Usage question |
| #103 | print all nodes  | How to print all nodes | Usage question |
| #110 | Reconstructing the sequence of tokens from abstract syntax tree. | Reconstruct tokens from AST | Usage question |
| #113 | How to get method information in one line code snippet | Get method info from code snippet | Usage question |
| #115 | How to get developer defined tokens from code? | Get developer-defined tokens from code | Usage question |
| #116 | Can I use tokenizer of javalang for C language? | Using javalang tokenizer for C language | Out of scope |
| #118 | get unique id of each node | Get unique ID of each node | Usage question |
| #119 | path between leaf nodes | Get path between leaf nodes | Usage question |
| #121 | Extracting full method declarations and fieldnames | Extract method declarations and field names | Usage question |
| #123 | Documentation on JavaLang | Request for full documentation | Documentation request |
| #124 | Visualizing the parsed tree | Visualize parsed tree | Usage question |
| #125 | Documentation | Request for documentation | Documentation request |
| #129 | Explanation of nodes of javalang.tree | Explanation of javalang.tree node types | Documentation request |
| #132 | How to get the cutoff line number of a method | Get method start/end line number | Usage question - addressed by end_position |
| #134 | How can I get staticblock from java file？ | How to get static blocks from Java file | Usage question |
| #136 | How to map methods to their respective classes? | Map methods to their respective classes | Usage question |
| #140 | how to print a hierarchical view of AST | How to print hierarchical view of AST | Usage question |
