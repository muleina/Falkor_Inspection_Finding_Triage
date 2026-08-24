#  Inspection Finding Triage (By Mulugeta W.A)

Inspection and maintenance activity on an offshore production platform generates findings: free-text
observations recorded against a piece of equipment by whoever made them. Findings are currently
triaged manually by a duty integrity engineer, who assesses each one, assigns scores, writes a
summary, and raises a ticket for maintenance planning.

Build the system that performs this triage. The input is a CSV containing findings and an equipment registry.
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

