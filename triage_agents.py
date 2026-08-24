"""
Inspection Finding Triage System

This module implements an automated inspection ticket triage workflow that leverages
Large Language Models (LLMs) to intelligently categorize and process inspection findings.
The system provides two main operational modes:

1. Design Mode: Generates LLM-assisted design artifacts including triage prompts and
   Pydantic data schemas for inspection workflows.
2. Triage Mode: Executes the full inspection ticket triage pipeline, processing findings
   from CSV files and generating structured tickets with contextual metadata.

The module integrates domain knowledge, equipment registry data, and reference
documentation to support the triage agents in making informed decisions about
inspection findings prioritization and categorization.

Author: Mulugeta WA
Date: 2026-08-24
"""

import os
import json
import csv
from pathlib import Path
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime
from typing import List, Optional
import argparse

import utils
import config as cfg 
from llm_agent_classes import AIDesignAssistant, TicketTriagAgent

class KnowledgeRepo:
    """Central repository for project knowledge and reference datasets used by triage agents.

    This class exposes the configured file paths for development notes, domain
    knowledge, reference documentation, equipment registry data, inspection
    findings, and example tickets. It keeps the triage workflow decoupled from
    hard-coded directory lookups and makes the knowledge assets easy to reuse
    across design and inference tasks.
    """
    dev_read_md = cfg.resource_dirpath / cfg.dev_read_md 
    knowledge_md = cfg.resource_dirpath / cfg.knowledge_md 
    ref_read_md = cfg.resource_dirpath / cfg.ref_read_md 
    equipment_registry_csv = cfg.resource_dirpath / cfg.equipment_registry_csv 
    inspection_findings_csv = cfg.resource_dirpath / cfg.inspection_findings_csv 
    example_ticket_json = cfg.resource_dirpath / cfg.example_ticket_json 
    
def ai_design_assist(**kwargs):
    """Generate LLM design artifacts for inspection triage workflows.

    This helper creates either a triage prompt draft or a pydantic schema draft
    by invoking the AI design assistant with project knowledge and reference
    artifacts. It can optionally persist the generated output to the result
    directory or print it to the console.

    Args:
        **kwargs: Optional overrides for runtime configuration.
            - isave (bool): Save generated output to disk when True.
            - query_type (str): One of "prompt_design" or
              "schema_validator_design".
    """
    query_type = kwargs.get("query_type", "prompt_design")
    llm_modelname = kwargs.get("llm_modelname", cfg.llm_modelname)
    llm_accesspoint = kwargs.get("llm_accesspoint", cfg.llm_accesspoint)
    issave = kwargs.get("isave", True)
    
    llm_modelname_tag = llm_modelname.replace(".", "").replace(":", "_").replace("-", "_")
    if query_type == "prompt_design":
        query = "Design LLM prompt for inspection triaging."
        triage_llm_prompt_draft = AIDesignAssistant(query, knowledge_filepath_list=[KnowledgeRepo.dev_read_md, 
                                                                                    KnowledgeRepo.knowledge_md, 
                                                                                    KnowledgeRepo.ref_read_md, 
                                                                                    KnowledgeRepo.example_ticket_json],
                                                    query_type=query_type,
                                                    llm_model=llm_modelname,
                                                    llm_accesspoint=llm_accesspoint
                                                    ).inference()
        if issave:
            utils.save_textfile(triage_llm_prompt_draft, filepath=cfg.result_dirpath / f"triage_llm_prompt_draft__{llm_modelname_tag}.md")
        else:
            print(triage_llm_prompt_draft)
            
    elif query_type == "schema_validator_design":
        for data_schema_name in ["inspection_findings.csv", "equipment_registry.csv", "example_ticket.json"]:
            query = f"Design pydantic data schema for <{data_schema_name}>."
            pydantic_data_schema_draft = AIDesignAssistant(query, knowledge_filepath_list=[KnowledgeRepo.dev_read_md, 
                                                                                           KnowledgeRepo.knowledge_md, 
                                                                                    KnowledgeRepo.ref_read_md, 
                                                                                    KnowledgeRepo.example_ticket_json],
                                                        query_type=query_type,
                                                        llm_model=llm_modelname,
                                                        llm_accesspoint=llm_accesspoint
                                                        ).inference()  
            if issave:
                utils.save_textfile(pydantic_data_schema_draft, filepath=cfg.result_dirpath / f"{data_schema_name}_pydantic_data_schema_draft__{llm_modelname_tag}.md")
            else:
                print(triage_llm_prompt_draft)
            # break
    
    else:
        print(f"Undefined query_type: {query_type}. Please choose from ['prompt_design', 'schema_validator_design'].")

def inspection_ticket_triage(**kwargs):
    """Run the inspection-finding triage workflow and optionally save its tickets.

    The function creates a :class:`TicketTriagAgent` using the configured domain
    knowledge and equipment registry, processes inspection findings from a CSV
    file, and writes the generated ticket data to the configured results
    directory when saving is enabled.

    Args:
        **kwargs: Optional runtime overrides. Supported keys include
            ``llm_modelname``, ``llm_accesspoint``,
            ``domain_knowledge_filepath``, ``equipment_registry_filepath``,
            ``metafilter_key``, ``inspection_finding_csv_filepath``, and
            ``isave``.
    """
    llm_modelname = kwargs.get("llm_modelname", cfg.llm_modelname)
    llm_accesspoint = kwargs.get("llm_accesspoint", cfg.llm_accesspoint)
    domain_knowledge_filepath = kwargs.get("domain_knowledge_filepath", KnowledgeRepo.knowledge_md)
    equipment_registry_filepath = kwargs.get("equipment_registry_filepath", KnowledgeRepo.equipment_registry_csv)
    inspection_finding_csv_filepath = kwargs.get("inspection_finding_csv_filepath", KnowledgeRepo.inspection_findings_csv)
    metafilter_key = kwargs.get("metafilter_key", "equipment_id")
    issave = kwargs.get("isave", True)
    
    agentInspect = TicketTriagAgent(domain_knowledge_filepath=domain_knowledge_filepath, 
                              equipment_registry_filepath=equipment_registry_filepath,
                              metafilter_key=metafilter_key,
                              llm_model=llm_modelname,
                              llm_accesspoint=llm_accesspoint
                              )
    tickets_json = agentInspect.ticket_triage_from_csv(inspection_finding_csv_filepath=inspection_finding_csv_filepath)
    if issave:
        llm_modelname_tag = llm_modelname.replace(".", "").replace(":", "_").replace("-", "_")
        utils.save_json(tickets_json, filepath=cfg.result_dirpath / f"tickets_agent_with_metakey_{metafilter_key}__{llm_modelname_tag}.json")
    else:
        print(tickets_json)

if __name__ == '__main__':
    """Main entry point for the inspection triage system.
    
    Supports two operational modes:
    - 'design': Generate LLM-assisted design artifacts (prompts, schemas)
    - 'triage': Execute the inspection ticket triage workflow
    
    Command-line arguments:
        -md/--mode: Execution mode ('design' or 'triage')
        -la/--llm_accesspoint: LLM source ('local' or 'cloud')
        -lm/--llm_modelname: Name of the LLM model to use
        -qt/--query_type: Design query type ('prompt_design' or 'schema_validator_design')
        -mk/--metafilter_key: Key for metadata filtering (default: 'equipment_id')
        -if/--inspection_csv_filepath: Path to inspection findings CSV file
        -s/--issave: Flag to save outputs to disk
    """
    parser = argparse.ArgumentParser(description="Inspection Triage Project")
    parser.add_argument('-md', '--mode', type=str, default="triage", choices=["design", "triage"])
    parser.add_argument('-la', '--llm_accesspoint', type=str, default="local", choices=["local", "cloud"])
    parser.add_argument('-lm', '--llm_modelname', type=str, default="llama3.2:latest")
    parser.add_argument('-qt', '--query_type', type=str, default="prompt_design", choices=["prompt_design", "schema_validator_design"])
    parser.add_argument('-mk', '--metafilter_key', type=str, default="equipment_id")
    parser.add_argument('-if', '--inspection_csv_filepath', type=str)
    parser.add_argument('-s', '--issave', default=False, action="store_true")
    
    print("#"*70)
    args =  vars(parser.parse_args())
    if args["mode"] == "design":
        ai_design_assist(**args)    
    elif args["mode"] == "triage":
        inspection_ticket_triage(**args)
    print("\n")
    print("#"*70)

# PROMPT DESIGN FOR TIAGE AGENT USING AI DESGIN ASSISTANT
# python triage_agents.py -md "design" -la "local" -lm "llama3.2:latest" -qt "prompt_design" -s

# VALIDATOR SCHEMA DESIGN FOR TIAGE AGENT USING AI DESGIN ASSISTANT
# python triage_agents.py -md "design" -la "local" -lm "llama3.2:latest" -qt "schema_validator_design" -s 

# INSPECTION TRIAGE TOCKET GENERATION USING TICKEET TIAGE AGENT
# python triage_agents.py -md "triage" -la "local" -lm "llama3.2:latest" -mk "equipment_id" -s
