# Diligence Desk

Diligence Desk is a SeekrFlow™ agent that drafts cited answers to a buyer's security questionnaire from one company's own trust documents. Each answer has a status (Yes, Partial, No, or Not covered), a quoted evidence phrase, and a source. When the documents are silent, the agent routes the question to a person instead of guessing.

All companies and figures in the demo data are fictional. Draft responses are for human review. They are not a compliance determination.

## Start here

| You want to | Read |
| --- | --- |
| Build and verify the agent | [Build and Verify Diligence Desk](docs/SOP_Build_and_Verify.md) |
| Train an Operator and set up a company | [Operator Enablement: Diligence Desk](docs/SOP_Operator_Enablement.md) |
| Learn the UI build, with the deck | [Enablement 1: SeekrFlow UI](enablement/ui/README.md) |
| Learn the SDK build | [Enablement 2: SeekrFlow SDK](enablement/sdk/README.md) |
| Share the use case with a customer | [Use Case Brief](enablement/Diligence_Desk_Use_Case_Brief.html) |

## Three levels

| Level | What you do |
| --- | --- |
| **Bronze** | Build the agent in the SeekrFlow UI and test it by hand in the Playground |
| **Silver** | Build the same agent with the SeekrFlow SDK and score every answer with code |
| **Gold** | Run full questionnaire files in bulk, keep an audit record, and attack the agent on purpose |

## What is in this repository

| Path | What it holds |
| --- | --- |
| `docs/` | The two SOPs |
| `enablement/` | The deck, the Use Case Brief, and the UI and SDK learning paths |
| `corpus/lumera-pay/upload/` | The four demo trust documents to upload: two PDFs, one Word file, and one Markdown file |
| `corpus/lumera-pay/` | Markdown copies of the same documents, used by the document check and the scoring |
| `corpus/lumera-health/` | One look-alike company document (PDF in `upload/`, Markdown copy beside it), used to test isolation |
| `agent/` | The agent instructions, the search tool instructions, and the compliance record function |
| `prompts/` | Paste-ready prompts for every bronze test |
| `testsets/` | The answer key and the questionnaires used by the silver and gold checks |
| `check_documents.py` | Document check |
| `create_agent.py` | Creates the agent with the SDK |
| `silver_check.py`, `silver_check.ipynb` | Silver check |
| `run_questionnaire.py` | Runs a questionnaire file in bulk and writes the reviewer spreadsheet and audit log |
| `run_attack_tests.py` | Attack tests |
| `dd_core.py`, `verify.py` | Shared helpers and the scoring rules |
| `tests/` | Practice check that tests the scripts on your computer without calling SeekrFlow |
| `evidence/` | Where screenshots and results go |

Real company documents never go in this repository. Keep them in the `companies/` folder, which Git ignores.
