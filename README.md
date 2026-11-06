# Diligence Desk SDK package v1.3 (silver and gold)

Shapes verified against docs.seekr.com on Oct 25, 2026: File Search tool, custom functions with RunPython, agent creation,
threads, messages, and runs. Offline suite passes (`bash tests/run_offline.sh`); no run against SeekrFlow yet.

## Run order
1. `pip install --upgrade seekrai pandas openpyxl` and `export SEEKR_API_KEY=...`
2. Gate G0, data readiness: `python check_corpus.py --company "Lumera Pay, Inc." --other "Lumera Health" corpus/D1_*.md corpus/D2_*.md corpus/D3_*.md corpus/D4_*.md`
   The v1.1 demo data fails on purpose (disclaimers name Lumera Health). Record it; apply the staged patch if bronze P-1 or TC-08 fails.
3. Copy the vector store ID from the store's page in the UI, then: `python setup_sdk_agent.py --vector-store-id <ID>`
   Custom-tool variant: `python setup_sdk_agent.py --vector-store-id <ID> --with-facts --name Diligence_Desk_SDK_Facts --tool-name trust_corpus_search_sdk2`
4. Silver, gate G2: open `silver_notebook_v1_3.ipynb` and run all cells.
5. Gold, gate G3: `python run_batch.py --questions testsets/questionnaire_golden.csv --company "Lumera Pay, Inc." --ids ids.json --answer-key testsets/answer_key.csv --runs 3 --gate G3 --out out/golden`
   Then the same with `--questions testsets/paraphrase_18.csv --runs 1 --out out/paraphrase`.
   Real companies: add `--signatures "value1;value2"` with values unique to any other company in the Org.
6. Adversarial before D5: `python run_adversarial.py --ids ids.json --stage pre_d5 --out out/adversarial`
7. Add D5 to the store in the UI, wait for Ready, then `--stage post_d5`, then re-run step 5 golden with `--out out/golden_post_d5`.

## Check during the first live run (not covered by the pages read)
- Whether the SDK agent accepts a reasoning setting and a temperature; record the agent's defaults. Consistency is measured either way.
- That `list_messages(thread_id)[0]` is the newest message, and how chunk_id fields appear in its content.
- Tool names must be unique in the Org; the SDK tool name replaces `trust_corpus_search` in the instructions automatically.
- Inference jobs (/v1/inference/jobs) are documented for batch chat completions; this runner uses agent runs instead, so retrieval and source tracing stay in the loop.

Exit codes: run_batch.py and run_adversarial.py exit 1 when a gate fails, so they can run in CI.
