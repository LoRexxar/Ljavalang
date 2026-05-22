"""Java AST Visitor pattern implementation.

Provides a base visitor class for traversing javalang AST nodes.
Subclass JavaVisitor and override visit_* methods for specific node types.

Usage:
    class MyVisitor(JavaVisitor):
        def visit_ClassDeclaration(self, node):
            print(f'Found class: {node.name}')
            self.generic_visit(node)

    tree = javalang.parse.parse(code)
    MyVisitor().visit(tree)
"""


class JavaVisitor(object):
    """Base visitor class for javalang AST traversal.

    Implements the standard visitor pattern. For each AST node type,
    dispatches to a visit_{ClassName} method. If no specific method is
    found, falls back to generic_visit which recursively visits children.

    Override visit_{ClassName} methods to add custom behavior for
    specific node types. Call generic_visit(node) to continue traversal.
    """

    def visit(self, node):
        """Visit a node by dispatching to the appropriate visit_* method."""
        class_name = node.__class__.__name__
        visitor = getattr(self, 'visit_' + class_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Default visitor that recursively visits all children of a node."""
        from . import tree

        if isinstance(node, tree.Node):
            for attr_name in node.attrs:
                value = getattr(node, attr_name, None)
                if value is None:
                    continue
                if isinstance(value, tree.Node):
                    self.visit(value)
                elif isinstance(value, (list, tuple)):
                    for item in value:
                        if isinstance(item, tree.Node):
                            self.visit(item)
