import os
import ast

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return
        
    lines = content.split('\n')
    inserts = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == '__init__' and not ast.get_docstring(node):
            inserts.append((node.lineno, '        """Initialize."""'))
            
    inserts.sort(key=lambda x: x[0], reverse=True)
    
    if inserts:
        for lineno, text in inserts:
            lines.insert(lineno, text)
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.py'):
            process_file(os.path.join(root, file))
