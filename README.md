#  Inspection Finding Triage (By Mulugeta W.A)

Inspection and maintenance activity on an offshore production platform generates findings: free-text
observations recorded against a piece of equipment by whoever made them. Findings are currently
triaged manually by a duty integrity engineer, who assesses each one, assigns scores, writes a
summary, and raises a ticket for maintenance planning.

Build the system that performs this triage. The input is a CSV containing findings and an equipment registry.
Output is a JSON file of tickets. A human still approves the result; the system produces the draft.

## Installation (CLI or Docker)
Make sure you have stored the  Ollama cloud API key in the local environment variable OLLAMA_API_KEY:
 
     export OLLAMA_API_KEY="__your_api_key__" 
### CLI 
    pip install -r requirements.txt
    bash setup_ollama_api_key.sh
### Docker
Build Docker Image
    
    docker build -t falkor_triage_agents .
## Inference
### CLI
    bash agent_run.sh
### Docker
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

## Designs
The overall design would include prompt and data validation schema generation for the Triage Agent, Triage Agent Design, and Testing.

### AI-Assisted Prompt and Schema Generation
- This will generate draft LLM system prompts and input/output data validation schema generation for the Triage Agent from the task README.md, knowledge, inspection, and registry documents.
- The draft will be validated and vetted before being integrated into the agent engine. 

### Triage Agent 
- Simple Prompt-based Agent: With and without metadata filtering

### Testing - TODO
- Input/Output Schema Validation - Done
- RAGAS: faithfulness, response relevancy - TODO

