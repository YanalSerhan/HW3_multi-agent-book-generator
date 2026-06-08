import sys

def clean_tex(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Try to find the document boundaries
        start_idx = content.find(r'\documentclass')
        end_idx = content.rfind(r'\end{document}')
        
        if start_idx != -1 and end_idx != -1:
            # We found both boundaries, extract exactly that
            end_idx += len(r'\end{document}')
            content = content[start_idx:end_idx]
        else:
            # Fallback to stripping markdown blocks if boundaries are missing
            if '```latex' in content:
                content = content.split('```latex', 1)[1]
            elif '```tex' in content:
                content = content.split('```tex', 1)[1]
                
            if '```' in content:
                content = content.rsplit('```', 1)[0]
                
            content = content.strip()
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content + '\n')
            
        print(f"Successfully cleaned {filepath}")
    except Exception as e:
        print(f"Failed to clean {filepath}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        clean_tex(sys.argv[1])
    else:
        print("Usage: python clean_tex.py <path_to_tex_file>")
