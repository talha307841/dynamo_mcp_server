import ast
def static_sanity_check(code: str) -> None:
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            name = getattr(node, 'module', None)
            if name and name.startswith('mcp'):
                continue
            raise SyntaxError(f"Import not allowed in generated tools: {ast.dump(node)}")