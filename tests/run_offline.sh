#!/usr/bin/env bash
# Practice run on your own computer with a pretend SeekrFlow. It proves the scripts work. It does not test the AI.
# Run from the repository folder:  bash tests/run_offline.sh
set -u
cd "$(dirname "$0")/.." || exit 1
export PYTHONPATH="$PWD/tests/mock:$PWD"
TMP="$(mktemp -d)"; echo '{"agent_id": "practice-agent"}' > "$TMP/agent_ids.json"
FAIL=0
expect() { if [ "$1" = "$2" ]; then echo "  ok: $3"; else echo "  NOT OK: $3 (got $1, wanted $2)"; FAIL=1; fi; }

echo "1. Document check on the Lumera Pay documents (expect PASS)"
python3 check_documents.py --company "Lumera Pay, Inc." --other "Lumera Health" corpus/lumera-pay/*.md > "$TMP/doc.txt"; expect $? 0 "documents pass"
echo "2. Document check on the look-alike company (expect PASS)"
python3 check_documents.py --company "Lumera Health, Inc." --other "Lumera Pay" corpus/lumera-health/*.md > "$TMP/doc2.txt"; expect $? 0 "look-alike documents pass"
echo "3. Gold check, standard questionnaire, 3 runs (expect PASS)"
python3 run_questionnaire.py --questions testsets/standard_questionnaire.csv --company "Lumera Pay, Inc." --agent-ids "$TMP/agent_ids.json" \
  --answer-key testsets/answer_key.csv --documents corpus/lumera-pay --runs 3 --concurrency 4 --check gold --out "$TMP/standard" > "$TMP/s.txt"; expect $? 0 "standard questionnaire passes"
echo "4. Resume: the same command again should find all work done"
python3 run_questionnaire.py --questions testsets/standard_questionnaire.csv --company "Lumera Pay, Inc." --agent-ids "$TMP/agent_ids.json" \
  --answer-key testsets/answer_key.csv --documents corpus/lumera-pay --runs 3 --check gold --out "$TMP/standard" > "$TMP/r.txt"; head -1 "$TMP/r.txt"
grep -q "^0 agent runs to do" "$TMP/r.txt"; expect $? 0 "nothing left to run"
echo "5. Gold check, reworded questionnaire (expect PASS)"
python3 run_questionnaire.py --questions testsets/reworded_questionnaire.csv --company "Lumera Pay, Inc." --agent-ids "$TMP/agent_ids.json" \
  --answer-key testsets/answer_key.csv --documents corpus/lumera-pay --check gold --out "$TMP/reworded" > "$TMP/w.txt"; expect $? 0 "reworded questionnaire passes"
echo "6. Planted mistake: the agent says Yes to the certification question (expect the check to FAIL)"
MOCK_FAULT=overclaim python3 run_questionnaire.py --questions testsets/standard_questionnaire.csv --company "Lumera Pay, Inc." --agent-ids "$TMP/agent_ids.json" \
  --answer-key testsets/answer_key.csv --documents corpus/lumera-pay --check gold --out "$TMP/fault" > "$TMP/f.txt"; expect $? 1 "overclaim is caught"
echo "6b. A real company: --signatures none must be accepted (expect PASS)"
python3 run_questionnaire.py --questions testsets/standard_questionnaire.csv --company "Lumera Pay, Inc." --agent-ids "$TMP/agent_ids.json" \
  --answer-key testsets/answer_key.csv --documents corpus/lumera-pay --check gold --signatures none --out "$TMP/none" > "$TMP/n.txt"; expect $? 0 "signatures none accepted"
echo "7. Attack tests, before and after the look-alike document"
python3 run_attack_tests.py --agent-ids "$TMP/agent_ids.json" --stage before_look_alike --out "$TMP/attack" > "$TMP/a1.txt"; expect $? 0 "attack tests before"
python3 run_attack_tests.py --agent-ids "$TMP/agent_ids.json" --stage after_look_alike --out "$TMP/attack" > "$TMP/a2.txt"; expect $? 0 "attack tests after"
echo; if [ $FAIL -eq 0 ]; then echo "Practice run: PASS"; else echo "Practice run: FAIL"; fi
rm -rf "$TMP"; find . -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null; exit $FAIL
