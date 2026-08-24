"""
System config file
"""
# path config
import os
from pathlib import Path
resource_dirpath = Path.cwd() / "resources"
dev_read_md = r"README.md"
knowledge_md = r"reference/domain_knowledge.md"
ref_read_md = r"reference/README.md"
equipment_registry_csv = r"data/equipment_registry.csv"
inspection_findings_csv = r"data/inspection_findings.csv"
example_ticket_json = r"reference/example_ticket.json"

result_dirpath = Path.cwd() / "results"
if not result_dirpath.exists():
    result_dirpath.mkdir(parents=True, exist_ok=True)
    
# llm models config
llm_modelname = "llama3.2:latest"
llm_accesspoint = "local" # "local" or "cloud"
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY", None) # for cloud 

