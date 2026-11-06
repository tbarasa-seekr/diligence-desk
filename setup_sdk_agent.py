"""Create the SDK twin of the bronze agent. Shapes verified against docs.seekr.com, Oct 25, 2026:
CreateFileSearch + FileSearchConfig(file_search_index, top_k, score_threshold); custom_functions.create(file_path);
CreateRunPython + RunPythonConfig(function_ids); CreateAgentRequest(name, instructions, model_id, tool_ids).

Usage: python setup_sdk_agent.py --vector-store-id <ID from the store's page> [--with-facts]
"""
import argparse, json, pathlib, time
from seekrai import SeekrFlow
from seekrai.types import (CreateAgentRequest, CreateFileSearch, CreateRunPython, FileSearchConfig,
                           RunPythonConfig)

TOOL_DESC = ("Searches the company's customer-shareable trust documents. Every section starts with a company line "
             "such as 'Company: Lumera Pay, Inc. | Information Security Policy | Section 3 of 6'. Query with the "
             "company's full name plus the question's topic keywords. Results may include other companies; keep only "
             "passages whose company line names the requested company exactly.")
FACTS_ADDENDUM = ("\n\n---\n\n## Compliance record tool\nYou also have `company_facts`, which calls get_company_fact(company, fact_key). "
                  "Use it only to confirm an exact figure after file search found the topic. Never quote it as Evidence. "
                  "If it returns NO RECORD, rely on the documents alone.")

def wait_active(client, agent_id, timeout_s=900):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        status = str(client.agents.retrieve(agent_id).status).lower()
        if status.endswith("active") and "inactive" not in status:
            return status
        time.sleep(5)
    raise TimeoutError("agent did not become Active; check its page in Agent Builder")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vector-store-id", required=True)
    ap.add_argument("--model", default="openai/gpt-oss-120b")
    ap.add_argument("--name", default="Diligence_Desk_SDK")
    ap.add_argument("--tool-name", default="trust_corpus_search_sdk")
    ap.add_argument("--with-facts", action="store_true")
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--score-threshold", type=float, default=0.3)
    a = ap.parse_args()
    client = SeekrFlow()
    fs = client.tools.create(CreateFileSearch(name=a.tool_name, description=TOOL_DESC,
            config=FileSearchConfig(file_search_index=a.vector_store_id, top_k=a.top_k, score_threshold=a.score_threshold)))
    tool_ids, ids = [fs.id], {"file_search_tool_id": fs.id, "vector_store_id": a.vector_store_id}
    instructions = pathlib.Path("C2_Agent_Instructions.txt").read_text().replace("trust_corpus_search", a.tool_name)
    if a.with_facts:
        fn = client.agents.custom_functions.create(file_path="get_company_fact.py")
        rp = client.tools.create(CreateRunPython(name="company_facts", description="Exact compliance facts for a named company.",
                                                 config=RunPythonConfig(function_ids=[fn.id])))
        tool_ids.append(rp.id); ids.update(function_id=fn.id, facts_tool_id=rp.id)
        instructions += FACTS_ADDENDUM
    agent = client.agents.create(CreateAgentRequest(name=a.name, instructions=instructions, model_id=a.model, tool_ids=tool_ids))
    ids.update(agent_id=agent.id, model=a.model, with_facts=a.with_facts, top_k=a.top_k, score_threshold=a.score_threshold)
    print("agent created:", agent.id, "status:", agent.status)
    ids["status"] = wait_active(client, agent.id)
    out = pathlib.Path("ids_facts.json" if a.with_facts else "ids.json")
    out.write_text(json.dumps(ids, indent=2)); print("saved", out, ids)

if __name__ == "__main__":
    main()
