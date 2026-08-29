#  Inspection Finding Triage (By Mulugeta W.A)

Inspection and maintenance activity on an offshore production platform generates findings: free-text
observations recorded against a piece of equipment by whoever made them. Findings are currently
triaged manually by a duty integrity engineer, who assesses each one, assigns scores, writes a
summary, and raises a ticket for maintenance planning.

Build the system that performs this triage. The input is a CSV containing findings and an equipment registry.
Output is a JSON file of tickets. A human still approves the result; the system produces the draft.

<!-- START doctoc -->
**Table of Contents**
- [Installation](https://github.com/muleina/Falkor_Inspection_Finding_Triage#installation)
- [Usage (Inference)](https://github.com/muleina/Falkor_Inspection_Finding_Triage#inference)
  - [CLI](https://github.com/muleina/Falkor_Inspection_Finding_Triage#inference-using-cli)
  - [Docker](https://github.com/muleina/Falkor_Inspection_Finding_Triage#inference-using-docker)
- [Resources](https://github.com/muleina/Falkor_Inspection_Finding_Triage#resources)
- [Design Overview](https://github.com/muleina/Falkor_Inspection_Finding_Triage#design-overview)
- [Results](https://github.com/muleina/Falkor_Inspection_Finding_Triage#results)
<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installation (CLI or Docker)
Make sure you have stored the  Ollama cloud API key in the local environment variable OLLAMA_API_KEY:
    
    export OLLAMA_API_KEY="__your_api_key__" 

### Config using CLI 
    pip install -r requirements.txt
    bash setup_ollama_api_key.sh
    
### Config using Docker
Build Docker Image
    
    docker build -t falkor_triage_agents .
    
## Inference
### Inference using CLI
    bash agent_run.sh
    
### Inference using Docker
Create and Run Docker containers
- PROMPT DESIGN FOR TRIAGE AGENT USING AI DESIGN ASSISTANT

        docker run --rm -e OLLAMA_API_KEY=$OLLAMA_API_KEY falkor_triage_agents -md "design" -la "cloud" -lm "gemma4" -qt "prompt_design"
To save to a local file, e.g., "D:/Falkor/results", change the path to your local directory path
        
        docker run --rm -v D:/Falkor/results:/app/results -e OLLAMA_API_KEY=$OLLAMA_API_KEY falkor_triage_agents -md "design" -la "cloud" -lm "gemma4" -qt "prompt_design" -s 
- VALIDATOR SCHEMA DESIGN FOR TRIAGE AGENT USING AI DESIGN ASSISTANT

      docker run --rm -v D:/Falkor/results:/app/results -e OLLAMA_API_KEY=$OLLAMA_API_KEY falkor_triage_agents -md "design" -la "cloud" -lm "gemma4" -qt "schema_validator_design" -s
- INSPECTION TRIAGE TICKET GENERATION USING TRIAGE AGENT

      docker run --rm -v D:/Falkor/results:/app/results -e OLLAMA_API_KEY=$OLLAMA_API_KEY falkor_triage_agents -md "triage" -la cloud -lm gemma4 -mk "equipment_id" -s
  
## Resources
- resources/data/inspection_findings.csv
- resources/data/equipment_registry.csv
- resources/reference/domain_knowledge.md
- resources/reference/example_ticket.json

## Design Overview
The overall design would include prompt and data validation schema generation for the Triage Agent, Triage Agent Design, and Testing.

### AI-Assisted Prompt and Schema Generation
- This will generate draft LLM system prompts and input/output data validation schema generation for the Triage Agent from the task README.md, knowledge, inspection, and registry documents.
- The draft will be validated and vetted before being integrated into the agent engine. 

### Triage Agent 
- Simple Prompt-based Agent: With and without metadata filtering

## Testing - TODO
- Input/Output Schema Validation - Done
- RAGAS: faithfulness, response relevancy - TODO

## Results
All the generated results using different LLM models are stored in [/Results](https://github.com/muleina/Falkor_Inspection_Finding_Triage/tree/main/results)

### Data Validation Schema using the AI DESIGN ASSISTANT AGENT

Gemma4
- [Schema for equipment_registry.csv using Gemma4](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/equipment_registry.csv_schema_draft__gemma4.md)
- [Schema for inspection_findings.csv using Gemma4](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/inspection_findings.csv_schema_draft__gemma4.md)
- [Schema for example_ticket.json using Gemma4](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/example_ticket.json_schema_draft__gemma4.md)

GPT-OSS:120
- [Schema for equipment_registry.csv using GPT-OSS:120b](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/equipment_registry.csv_schema_draft__gpt_oss_120b.md)
- [Schema for inspection_findings.csv using GPT-OSS:120b](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/inspection_findings.csv_schema_draft__gpt_oss_120b.md)
- [Schema for example_ticket.json using GPT-OSS:120b](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/example_ticket.json_schema_draft__gpt_oss_120b.md)

GPT-OSS:20
- [Schema for equipment_registry.csv using GPT-OSS:20b](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/equipment_registry.csv_schema_draft__gpt_oss_20b.md)
- [Schema for inspection_findings.csv using GPT-OSS:20b](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/inspection_findings.csv_schema_draft__gpt_oss_20b.md)
- [Schema for example_ticket.json using GPT-OSS:20b](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/example_ticket.json_schema_draft__gpt_oss_20b.md)

Llama3.2
- [Schema for equipment_registry.csv using Llama3.2](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/equipment_registry.csv_schema_draft__llama32_latest.md)
- [Schema for inspection_findings.csv using Llama3.2](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/inspection_findings.csv_schema_draft__llama32_latest.md)
- [Schema for example_ticket.json using Llama3.2](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/example_ticket.json_schema_draft__llama32_latest.md)
  
### Ticketing Skill Prompt Draft Auto-generation using the AI DESIGN ASSISTANT AGENT
 Used in the TICKETING AGENT as a prompt.

- [Skill Ticketing Prompt using Gemma4](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/triage_llm_prompt_draft__gemma4.md)
- [Skill Ticketing Prompt using GPT-OSS:120b](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/triage_llm_prompt_draft__gpt_oss_120b.md)
- [Skill Ticketing Prompt using GPT-OSS:20b](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/triage_llm_prompt_draft__gpt_oss_20b.md)
- [Skill Ticketing Prompt using Llama3.2](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/triage_llm_prompt_draft__llama32_latest.md)

### Tickets.Json using the TICKETING AGENT

- [Tickets.JSON using Gemma4](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/tickets_agent_with_metakey_equipment_id__gemma4.json)
- [Tickets.JSON using GPT-OSS:120b](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/tickets_agent_with_metakey_equipment_id__gpt_oss_120b.json)
- [Tickets.JSON using GPT-OSS:20b](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/tickets_agent_with_metakey_equipment_id__gpt_oss_20b.json)
- [Tickets.JSON using Llama3.2](https://github.com/muleina/Falkor_Inspection_Finding_Triage/blob/main/results/tickets_agent_with_metakey_equipment_id__llama32_latest.json)
