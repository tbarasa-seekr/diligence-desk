#!/usr/bin/env bash
# Proves the pipeline offline with a mock SDK. Run from the package root: bash tests/run_offline.sh
set -u; export PYTHONPATH="$PWD/tests/mock:$PWD"
echo '{"agent_id": "mock-agent"}' > /tmp/ids_mock.json
echo "== G0 on v1.1 demo data (expect FAIL: disclaimers name the other company)"
python3 check_corpus.py --company "Lumera Pay, Inc." --other "Lumera Health" corpus/D1_*.md corpus/D2_*.md corpus/D3_*.md corpus/D4_*.md | tail -4
echo "== G3 golden, 3 runs (expect PASS)"
rm -rf /tmp/o1; python3 run_batch.py --questions testsets/questionnaire_golden.csv --company "Lumera Pay, Inc." --ids /tmp/ids_mock.json \
  --answer-key testsets/answer_key.csv --corpus corpus --runs 3 --concurrency 4 --gate G3 --out /tmp/o1 | grep -E "^# Gate|status_acc|consistency"; echo "exit $?"
echo "== Resume check: same command again should do 0 runs"
python3 run_batch.py --questions testsets/questionnaire_golden.csv --company "Lumera Pay, Inc." --ids /tmp/ids_mock.json \
  --answer-key testsets/answer_key.csv --corpus corpus --runs 3 --gate G3 --out /tmp/o1 > /tmp/resume.txt; head -1 /tmp/resume.txt
echo "== G3 paraphrase (expect PASS)"
rm -rf /tmp/o2; python3 run_batch.py --questions testsets/paraphrase_18.csv --company "Lumera Pay, Inc." --ids /tmp/ids_mock.json \
  --answer-key testsets/answer_key.csv --corpus corpus --gate G3 --out /tmp/o2 | grep -E "^# Gate"
echo "== Fault injection: overclaim on Q2 (expect FAIL and exit 1)"
rm -rf /tmp/o3; MOCK_FAULT=overclaim python3 run_batch.py --questions testsets/questionnaire_golden.csv --company "Lumera Pay, Inc." --ids /tmp/ids_mock.json \
  --answer-key testsets/answer_key.csv --corpus corpus --gate G3 --out /tmp/o3 | grep -E "^# Gate|overclaim_rate \|"; echo "exit ${PIPESTATUS[0]}"
echo "== Adversarial pre_d5 and post_d5"
python3 run_adversarial.py --ids /tmp/ids_mock.json --stage pre_d5 --out /tmp/o4 | tail -1
python3 run_adversarial.py --ids /tmp/ids_mock.json --stage post_d5 --out /tmp/o4 | tail -1
