import os
import re

for root, dirs, files in os.walk('tests'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path, encoding='utf-8') as f:
                content = f.read()
            content = re.sub(r'def (test_[^:]+?)\(\):', r'def \1() -> None:', content)
            content = re.sub(r'def (test_[^:]+?)\(([^)]+)\):', r'def \1(\2) -> None:', content)
            content = re.sub(r'def (mock_[^:]+?)\(\):', r'def \1() -> None:', content)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
