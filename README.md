#  Inspection Finding Triage

Inspection and maintenance activity on an offshore production platform generates findings: free-text
observations recorded against a piece of equipment by whoever made them. Findings are currently
triaged manually by a duty integrity engineer, who assesses each one, assigns scores, writes a
summary and raises a ticket for maintenance planning.

Build the system that performs this triage. Input is a CSV of findings plus an equipment registry.
Output is a JSON file of tickets. A human still approves the result; the system produces the draft.

## Installation
    pip install -r requirement.txt
    bash setup_ollama_api_key.sh
## Inference
    bash agent_run.sh

## Resources
- resources/data/inspection_findings.csv
- resources/data/equipment_registry.csv
- resources/reference/domain_knowledge.md
- resources/reference/example_ticket.json

## Designs - TODO

The overall design would include prompt and data validation schema generation for the Triage Agent, Triage Agent Design, and Testing.

### AI-Assisted Prompt and Schema Generation
- This will generate a draft LLM system prompts and input/output data validation schema generation for the Triage Agent from task README.md, knowledge, inspection and registry documents.
- 
Draft will be validated and corrected before integrated into the agent engine. 

### Triage Agent 
- Simple Prompt-based Agent: With and without metadata filtering
- RAG-based Agent: Keyword Search (keyword and semantic)

### Testing
 - Schema Validation
 - RAGAS: faithfulness, response relevancy 
 - Edge case and output validation

