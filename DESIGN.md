# Assumptions

- The available knowledge resources are limited, and a simple LLM Agent call has been adopted instead of adding the further complexity of RAG or Agentic AI.
- Metadata filtering has been employed based on equipment ID during ticketing to avoid contamination of info from other equipment.
- LLM inference temperature = 0 has been set to limit hallucinations and force the LLMs to focus on the factual data provided in the prompt.
- For LLM inference, I have employed Ollama with local and cloud configuration setup, as provided in the setup bash script. 
- The code and orchestration are my own work; no external AI coding, support, or external source has been employed, except for the cases explained below under AI assistance.

# AI assistance

- I have AI assistance (developed local code for it) to generate prompt drafts and data schema Pydantic validators for the ticketing LLL agent.
- The drafts were compared and curated before finally being employed in the ticket triaging agent. 
- Owing to limited time, I have not explored the prompt, but rather supplied the knowledge sources during ticketing inference to improve performance.

    python triage_agents.py -md "design" -la "$LLM_ACCESSPOINT" -lm "$LLM_MODELNAME" -qt "prompt_design" -s

    python triage_agents.py -md "design" -la "$LLM_ACCESSPOINT" -lm "$LLM_MODELNAME" -qt "schema_validator_design" -s 

# A. Structured output

I have added schema validation to the LLM in three stages: TICKET_SCHEMA format in the LLM prompt, output formatting using pydantic during the Ollama call, and after retrieving the response.
Currently, failed tickets are skipped with error notification on the terminal, but could have been handled better with LOGGER setup.

# B. Domain knowledge

Currently, the knowledge (small context) and inspection comments are supplied directly to the LLM prompt. 
In case of a discrepancy between summary instructions (drafted by the AI Design Assistance Agent) and the knowledge, the prompt can be modified to flag the discrepancy, trigger regeneration of new summary instructions, or assist the agent with an override instruction (how to handle the situation)

# C. Urgency derivation

I believe this should be done with experts during system design decisions on how to handle overriding rules and corner cases. The agent can follow the instructions, e.g., to auto-infer rules and flag the cases. 
I have included extracted knowledge in the draft prompts generated using different LLMs, such as GPT-OSS:20b, Gemma4, GPT-OSS:20b, and GPT-OSS:20b. 
The summary knowledge can be explored in the provided 'triage_llm_prompt_draft.md'text files.

# D. Limits 

The current system is built to achieve the desired task with minimal complexity. 

I did not spend much effort assessing the extracted knowledge in detail, as this submission focuses on building an operations orchestration with minor oversight on the domain knowledge. 
Thus, I have provide four tickets.json for each of the four LLMs, "tickets_agent_with_metakey_equipment_id__[LLM_NAME].json".

I have decided not to use knowledge context retrieval through semantic RAG and a reasoning Agent for the following reasons: 

- The knowledge text is very small; most of the content is relevant for ticketing and can fully fit into the LLM context window. 
- Metadata filtering has been employed with per-ticket inference for enhanced accuracy. The drawback is the repeated calls to the agent for every ticket, instead of handling the CSV file directly and inferring once.
- ReACt (with tool and actions) could be a better alternative for modular orchestration using tool calling to handle the full pipeline. I have not included it in the submission, due to the limited time and restrictions on dev tools for the task.
- Once again, I wish I had added a ticket evaluator Agent using RAGAS. It would have been a great addition.
- A Docker container and test scripts (e.g., pytest) would have been a great addition to the repo. But a simple requirements.txt along with installation and execution scripts has been provided. A Python package checker has been added to the GitHub workflow.

