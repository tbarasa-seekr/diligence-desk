"""Create the SDK version of the Diligence Desk agent: a File Search tool on your vector store, plus the agent.

python create_agent.py --vector-store-id YOUR_STORE_ID
python create_agent.py --vector-store-id YOUR_STORE_ID --with-facts
python create_agent.py --vector-store-id YOUR_STORE_ID --name Diligence_Desk_ACME --tool-name trust_corpus_search_acme --output agent_ids_acme.json

Uses CreateFileSearch + FileSearchConfig(file_search_index, top_k, score_threshold),
custom_functions.create(file_path), CreateRunPython + RunPythonConfig(function_ids),
and CreateAgentRequest(name, instructions, model_id, tool_ids).
Writes agent_ids.json (or agent_ids_facts.json with --with-facts).
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

def tool_description():
    """Use the same tool instructions as the bronze build, so both levels search the same way."""
    p = pathlib.Path("agent/tool-instructions.txt")
    return p.read_text().strip() if p.exists() else TOOL_DESC

def wait_active(client, agent_id, timeout_s=900):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        status = str(client.agents.retrieve(agent_id).status).lower()
        if status.endswith("active") and "inactive" not in status:
            return status
        time.sleep(5)
    raise TimeoutError("The agent did not become Active. Check its page in Agent Builder.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vector-store-id", required=True)
    ap.add_argument("--model", default="openai/gpt-oss-120b")
    ap.add_argument("--name", help="agent name (default Diligence_Desk_SDK, or Diligence_Desk_SDK_Facts with --with-facts)")
    ap.add_argument("--tool-name", help="search tool name (default trust_corpus_search_sdk, or trust_corpus_search_sdk_facts)")
    ap.add_argument("--with-facts", action="store_true", help="also create the compliance record tool")
    ap.add_argument("--output", help="file that receives the new IDs (default agent_ids.json, or agent_ids_facts.json with --with-facts)")
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--score-threshold", type=float, default=0.2)
    a = ap.parse_args()
    name = a.name or ("Diligence_Desk_SDK_Facts" if a.with_facts else "Diligence_Desk_SDK")
    tool_name = a.tool_name or ("trust_corpus_search_sdk_facts" if a.with_facts else "trust_corpus_search_sdk")
    client = SeekrFlow()
    fs = client.tools.create(CreateFileSearch(name=tool_name, description=tool_description(),
            config=FileSearchConfig(file_search_index=a.vector_store_id, top_k=a.top_k, score_threshold=a.score_threshold)))
    tool_ids, ids = [fs.id], {"file_search_tool_id": fs.id, "vector_store_id": a.vector_store_id}
    instructions = pathlib.Path("agent/agent-instructions.txt").read_text().replace("trust_corpus_search", tool_name)
    if a.with_facts:
        fn = client.agents.custom_functions.create(file_path="agent/get_company_fact.py")
        rp = client.tools.create(CreateRunPython(name="company_facts", description="Exact compliance facts for a named company.",
                                                 config=RunPythonConfig(function_ids=[fn.id])))
        tool_ids.append(rp.id); ids.update(function_id=fn.id, facts_tool_id=rp.id)
        instructions += FACTS_ADDENDUM
    agent = client.agents.create(CreateAgentRequest(name=name, instructions=instructions, model_id=a.model, tool_ids=tool_ids))
    ids.update(agent_id=agent.id, model=a.model, with_facts=a.with_facts, top_k=a.top_k, score_threshold=a.score_threshold)
    print("agent created:", agent.id, "status:", agent.status)
    ids["status"] = wait_active(client, agent.id)
    out = pathlib.Path(a.output or ("agent_ids_facts.json" if a.with_facts else "agent_ids.json"))
    out.write_text(json.dumps(ids, indent=2))
    print("saved", out, ids)

if __name__ == "__main__":
    main()
