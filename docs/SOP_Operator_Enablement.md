# Operator enablement: Diligence Desk

## 1. Document control

| Title | Operator Enablement: Diligence Desk |
| --- | --- |
| Effective date | November 2026 |
| Owner | Seekr |
| Audience | OneValley Operators |

**Jump to:** [Training path](#5-training-path) | [Modules 1 to 5](#6-modules-1-to-5-learn-the-build) | [Module 6: Onboard a company](#7-module-6-onboard-a-company) | [Module 7: Operate](#8-module-7-operate-and-support) | [Certification](#9-operator-certification)

## 2. Purpose and scope

This SOP trains OneValley Operators to build, verify, and operate Diligence Desk, and to set it up for a portfolio company. Diligence Desk drafts cited answers to a buyer's security questionnaire from one company's own trust documents. A person approves every answer.

An Operator who finishes this SOP can build the agent from scratch, prove that it answers correctly, and hand a verified build to a company's reviewer.

**In scope:** the training path, onboarding a real company, and the operating routine.

**Out of scope:**

* Creating customer Orgs and opening tickets with Seekr Support. Follow the OneValley Operator SOP: Opening Tickets with Seekr Support.
* Billing and consumption reporting.
* Legal or compliance determinations. Draft responses are for human review.

## 3. Roles and responsibilities

| Role | Responsibilities |
| --- | --- |
| **Operator** | Completes the modules. Builds and verifies each company's agent. Delivers level 1 (L1) and level 2 (L2) support. |
| **Trainer** | Watches Modules 2 and 3 without helping. Records every question the Operator asks. Signs the certification. |
| **Company reviewer** | Works at the portfolio company. Approves or edits every drafted row. |
| **Document owner** | Supplies the company's customer-shareable documents. Confirms the answer key. |
| **Seekr Support** | Resolves level 3 (L3) issues. Open a ticket as described in the OneValley Operator SOP. |

## 4. How the training works

* Do the modules in order. Finish Modules 1 to 5 on the demo company before you touch a real company's documents.
* Every module has a goal, a time, the steps, and a **Complete when** line. Move on only when it is true.
* The steps for Modules 2 to 5 live in the [Build and Verify SOP](SOP_Build_and_Verify.md). This SOP tells you which steps to follow and what to prove.
* Keep your screenshots. The Build and Verify SOP names every one.
* Never commit a real company's documents to this repository. It is public.

## 5. Training path

| Module | Goal | Time | Do | Complete when |
| --- | --- | --- | --- | --- |
| 1. Understand Diligence Desk | Know what each part does and why | 20 minutes | Read Module 1 below | You can answer the two questions in Module 1 aloud |
| 2. Build the bronze agent | A working agent, no code | 30 minutes | Build and Verify SOP, Steps 2.1 to 2.5 | The agent is Active and the certification trap returns Partial |
| 3. Verify the bronze agent | Prove it on every trap | 45 to 60 minutes | Build and Verify SOP, Steps 2.6 to 2.9 | 18 of 18 runs pass and the screenshots are saved |
| 4. Build and check silver | The same agent from code, scored automatically | 60 to 90 minutes | Build and Verify SOP, Part 1 and Part 3 | Silver check: PASS |
| 5. Run gold | Full questionnaires in bulk, with an audit trail | About 60 minutes | Build and Verify SOP, Part 4 | Gold check: PASS and the attack tests pass |
| 6. Onboard a company | A verified build for a real company | An afternoon, plus 24 to 72 hours if the company needs an Org | Module 6 below | Company release check passes |
| 7. Operate and support | Keep the build correct over time | Ongoing | Module 7 below | The routine is scheduled and the escalation path is known |

## 6. Modules 1 to 5: learn the build

### Module 1: Understand Diligence Desk

**Goal:** know what each part does before you click anything. **Time:** 20 minutes.

| Part | What it does | In the demo |
| --- | --- | --- |
| File storage | Holds the documents you upload | Four Lumera Pay documents, plus one look-alike company |
| Vector store | Splits documents into searchable pieces so the agent can find them by meaning | One store per company |
| File Search tool | Lets the agent query one store, with Top K and a Score Threshold | `trust_corpus_search`, Top K 5, Score Threshold 0.3 |
| Agent | Instructions, a model, and tools working as one assistant | `Diligence_Desk` on `openai/gpt-oss-120b` |
| Playground and Run Source Trace | Where you test, and where you see which passages shaped an answer | Every check in Part 2 |

**What every answer looks like:**

1. One row per question, in the buyer's order: #, Question, Answer, Status, Evidence, Source.
2. Status is exactly one of **Yes**, **Partial**, **No**, or **Not covered**.
3. Evidence is a word-for-word phrase from the document, under 15 words. No quote means Not covered.
4. Numbers, durations, and dates are copied exactly, with units.
5. A certification that is in progress is never answered as held.
6. Only passages whose company line names the requested company are used.
7. Every reply ends with "NEEDS HUMAN: ..." and a reminder that a person approves each answer.

**Complete when:** you can answer both questions aloud.

1. Why does the demo add a near-identical second company to the store halfway through testing?
2. Why is "Not covered" better than a plausible guess?

### Modules 2 to 5: build and verify

For each module, follow the steps named in the training path. After each module, write one sentence in your evidence log about the step that took longest or confused you. The Trainer reviews these notes after Module 3.

**Trainer observation, Modules 2 and 3:** the Trainer watches the Operator build and verify the bronze agent without helping. The Trainer times each step and records each question the Operator asks. Each question marks a place where the SOP needs more detail.

## 7. Module 6: Onboard a company

**Goal:** a verified build that a company's reviewer can rely on. **Time:** an afternoon, plus 24 to 72 hours if the company needs its own Org.

One company gets one vector store, one search tool, and one agent. This isolates each company's documents.

| Step | Who acts | Action | Trigger for next step |
| --- | --- | --- | --- |
| 6.1 | Operator | Request an Org if the company needs one | Seekr confirms the Org |
| 6.2 | Operator and document owner | Collect customer-shareable documents | Documents received |
| 6.3 | Operator | Convert to Markdown and add company lines | Files saved in `companies/COMPANY/documents/` |
| 6.4 | Operator | Run the document check | Document check: PASS |
| 6.5 | Operator | Create the vector store | Every file Ready |
| 6.6 | Operator | Create the tool and agent | Agent Active |
| 6.7 | Operator and document owner | Build the answer key | Key confirmed by the document owner |
| 6.8 | Operator | Run the company release check | Company release check passes |
| 6.9 | Operator and reviewer | Hand off | Reviewer named and refresh date set |

Replace `COMPANY` with a short lowercase name, such as `acme`. Replace `LEGAL NAME` with the company's exact legal name, such as `Acme Robotics, Inc.`

### Step 6.1: Request an Org if the company needs one

1. Follow Workflow A in the OneValley Operator SOP: Opening Tickets with Seekr Support.
2. Allow 24 to 72 hours.

**Complete when:** Seekr confirms the Org and the OneValley Admin account can sign in. Skip this step if the company already has an Org.

### Step 6.2: Collect customer-shareable documents

1. Ask the document owner for the company's security policy, data handling standard, subprocessor list, and business continuity summary.
2. Take only documents the company shares with customers. Leave out internal runbooks, incident details, and anything under NDA. The agent drafts text that leaves the building.

**Complete when:** you hold the documents and the document owner has confirmed they are shareable.

### Step 6.3: Convert to Markdown and add company lines

1. Convert each document to Markdown (`.md`). Check every table and heading by eye. Automatic conversion can break tables and detach text from its heading.
2. Name each file after the document's title, in lowercase with hyphens, such as `security-policy.md`. The scoring uses this name to check sources.
3. Add a version, effective date, or last-updated line near the top of each file.
4. Add a company line as the first line under every `##` heading:

```
Company: LEGAL NAME | Security Policy | Section 3 of 6
```

5. Remove every mention of any other company from the files.
6. Create the folder and save the files in it. The `companies` folder is ignored by Git, so real documents stay off the public repository:

```
mkdir -p companies/COMPANY/documents
```

Security policies are the most boilerplate-heavy documents there are. A passage without its company name can be attributed to the wrong company.

**Complete when:** every section starts with a company line and you have saved the files.

### Step 6.4: Run the document check

1. Run:

```
python3 check_documents.py --company "LEGAL NAME" --other "SIMILAR COMPANY NAME" companies/COMPANY/documents/*.md
```

Use `--other` once for each similarly named company in the same Org. Leave it out if there is none.

**Expect:** `PASS` beside each file, then `Document check: PASS`.

**Complete when:** the last line reads `Document check: PASS`.

### Step 6.5: Create the vector store

1. In **Data Engine**, **Storage**, upload the files as **Raw Data**.
2. Create a vector store named `Trust Corpus - COMPANY` and add the files. Leave the settings on their defaults.
3. Wait until every file shows **Ready**. Copy the store ID.

**Complete when:** every file shows Ready.

### Step 6.6: Create the tool and agent

1. Run:

```
python3 create_agent.py --vector-store-id YOUR_STORE_ID --name Diligence_Desk_COMPANY --tool-name trust_corpus_search_company --output agent_ids_company.json
```

Replace `COMPANY` and `company` with your short name. The script builds the File Search tool and the agent with the standard instructions, then waits for Status Active.

To build in the UI instead, follow Steps 2.3 and 2.4 of the Build and Verify SOP with the company's names. If the company shares an Org with other companies, add the company name to the store, tool, and agent names, and replace `trust_corpus_search` in the pasted instructions with your tool name.

**Expect:** `saved agent_ids_company.json`.

**Complete when:** the agent is Active.

### Step 6.7: Build the answer key

1. Take 10 to 18 questions from the company's real buyer questionnaire.
2. Save them as `companies/COMPANY/questions.csv` with the columns `qnum,question`.
3. Save the expected answers as `companies/COMPANY/answer_key.csv` with the columns `qnum,expected_status,evidence_substring,source_doc`. Use `testsets/answer_key.csv` as the model.
4. For each question, write the expected status (Yes, Partial, No, or Not covered), a short phrase copied word for word from the document, and the document file name without `.md`.
5. Include one question the documents cannot answer, with the expected status Not covered.
6. Build the key from the documents, not from memory. The document owner confirms it.

**Complete when:** the document owner confirms the key.

### Step 6.8: Run the company release check

1. Choose values that belong only to other companies in the same Org, such as a retention period or a hosting provider only they use. Separate them with semicolons. If there are no other companies, use `none`.
2. Run:

```
python3 run_questionnaire.py --questions companies/COMPANY/questions.csv --company "LEGAL NAME" --agent-ids agent_ids_company.json --answer-key companies/COMPANY/answer_key.csv --documents companies/COMPANY/documents --runs 3 --check silver --signatures "VALUE ONE;VALUE TWO" --out out/company
```

Always set `--signatures` for a real company. Without it, the check looks for the demo company's values.

**Expect:** `# Silver check: PASS` or `FAIL`, and `out/company/responses.xlsx`.

**Complete when:** the report reads `PASS`. If it fails, use the troubleshooting table in the Build and Verify SOP, change one thing at a time, and run the check again.

### Step 6.9: Hand off

1. Name the reviewer who approves every row.
2. Save `out/company/check_report.md` and `responses.xlsx` where the company can reach them.
3. Agree a refresh date with the document owner, such as every quarter.
4. Give the reviewer the Gaps sheet. Every question marked Not covered needs a person.

**Complete when:** the reviewer is named, the report is saved, and the refresh date is set.

**Company release check passes when:** the document check is clean, the company's answer key clears the silver bar, and Step 6.9 is complete.

## 8. Module 7: Operate and support

**Goal:** keep each company's build correct over time.

### 8.1 Operating routine

| When | Do |
| --- | --- |
| A company changes a document | Create a new store named with the month, such as `Trust Corpus - COMPANY 2026-12`. Run the document check, run the company release check, and confirm the contamination values. Retire the old store once the new one passes. |
| Every week | Take 5 rows a reviewer approved. Confirm each still matches its document. |
| Every month | Run the standard questionnaire, the reworded questionnaire, and the attack tests on the demo build. This catches changes in the platform or the model. |
| A reviewer corrects a row | Add the question and the correct answer to that company's answer key. |

### 8.2 Support

| Level | Owner | Covers |
| --- | --- | --- |
| **L1 and L2** | OneValley | Build, configuration, and test questions. How-to help. Reading error messages. Reviewing a company's setup. |
| **L3** | Seekr | Issues that need Seekr-side telemetry, a platform fix, or Seekr-managed services. |

Before you escalate, work through L1 and L2 first. Then follow the OneValley Operator SOP to open the ticket. Include:

- [ ] The agent, tool, and vector store names
- [ ] The exact prompt and the full reply
- [ ] The run ID from the audit log or the Playground
- [ ] The latest check report
- [ ] What you already tried
- [ ] Screenshots, with secrets removed

Never include your API key in a ticket.

## 9. Operator certification

The Trainer signs off when the Operator has done all of the following without help:

- [ ] Built the bronze agent and passed 18 of 18 runs (Modules 2 and 3)
- [ ] Explained why the demo adds a look-alike company and why Not covered beats a guess (Module 1)
- [ ] Passed the silver check (Module 4)
- [ ] Passed the gold check and the attack tests, and found one run in the audit log (Module 5)
- [ ] Passed the document check on a real company's documents (Step 6.4)
- [ ] Passed the company release check for a real company (Step 6.8)
- [ ] Named the reviewer and set the refresh date (Step 6.9)
- [ ] Described the weekly and monthly routine (Module 7)
- [ ] Described what to include in an escalation ticket (Module 7)

| Operator | Trainer | Date |
| --- | --- | --- |
|  |  |  |
