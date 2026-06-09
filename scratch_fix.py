import glob
import re

AGENT_MAPPING = {
    "research_agent.py": "research_agent",
    "fact_verification_agent.py": "fact_verification_agent",
    "outline_agent.py": "outline_architect_agent",
    "writer_agent.py": "writer_agent",
    "editor_agent.py": "editor_agent",
    "reviewer_agent.py": "reviewer_agent",
    "citation_agent.py": "citation_agent",
    "latex_agent.py": "latex_formatter_agent",
    "pdf_agent.py": "pdf_production_agent",
    "qa_agent.py": "qa_agent",
}

for file_path in glob.glob("src/crewai_book/agents/*_agent.py"):
    filename = file_path.split("/")[-1].split("\\")[-1]
    if filename not in AGENT_MAPPING:
        continue
        
    config_key = AGENT_MAPPING[filename]
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # We need to add the import: from ..config.agent_configs import AGENT_CONFIGS
    if "AGENT_CONFIGS" not in content:
        import_stmt = "from ..config.agent_configs import AGENT_CONFIGS"
        # Find the from crewai import Agent
        content = content.replace("from crewai import Agent", f"from crewai import Agent\nfrom ..config.agent_configs import AGENT_CONFIGS")
        
    # We need to replace role="...", goal="...", backstory="..."
    # with role=AGENT_CONFIGS["key"].role etc.
    # It's safer to use regex to find the Agent( block
    
    # We'll regex replace role=..., goal=..., backstory=...
    content = re.sub(r'role\s*=\s*(["\']).*?\1', f'role=AGENT_CONFIGS["{config_key}"].role', content, flags=re.DOTALL)
    
    # For goal and backstory, they might be multiline with parentheses
    content = re.sub(r'goal\s*=\s*(?:["\'][^"\']*["\']|\(.*?\)),?', f'goal=AGENT_CONFIGS["{config_key}"].goal,', content, flags=re.DOTALL)
    content = re.sub(r'backstory\s*=\s*(?:["\'][^"\']*["\']|\(.*?\)),?', f'backstory=AGENT_CONFIGS["{config_key}"].backstory,', content, flags=re.DOTALL)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Updated agents.")
