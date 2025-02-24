import ast
import json

class ASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.data = []

    def generic_visit(self, node):
        node_dict = {"type": type(node).__name__}
        if hasattr(node, "lineno"):
            node_dict["lineno"] = node.lineno
        if hasattr(node, "col_offset"):
            node_dict["col_offset"] = node.col_offset
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                node_dict[field] = [self.visit(item) for item in value]
            elif isinstance(value, ast.AST):
                node_dict[field] = self.visit(value)
            else:
                node_dict[field] = value
        #self.data.append(node_dict) #removed from generic visit.
        return node_dict

    def visit_Module(self, node):
        """Specifically handle the Module node (root node)."""
        node_dict = {"type": type(node).__name__}
        self.data.append(node_dict)
        for statement in node.body: #iterate through all statements in the module.
            self.visit(statement) #visit each statement.
        return node_dict

    def visit_Call(self, node):
        """Handle Call nodes to prevent duplicates."""
        node_dict = {"type": type(node).__name__}
        if hasattr(node, "lineno"):
            node_dict["lineno"] = node.lineno
        if hasattr(node, "col_offset"):
            node_dict["col_offset"] = node.col_offset
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                node_dict[field] = [self.visit(item) for item in value]
            elif isinstance(value, ast.AST):
                node_dict[field] = self.visit(value)
            else:
                node_dict[field] = value
        if node_dict not in self.data: #check for duplicates.
            self.data.append(node_dict)
        return node_dict

def analyze_ast(code):
    try:
        tree = ast.parse(code)
        visitor = ASTVisitor()
        visitor.visit(tree)
        ast_json = json.dumps(visitor.data, indent=4)
        return ast_json
    except SyntaxError as e:
        raise Exception(f"Syntax error: {e}")