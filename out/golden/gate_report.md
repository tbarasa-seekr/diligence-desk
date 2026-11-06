# Gate G3: FAIL

- company: Lumera Pay, Inc.
- agent_id: agent-f63a77fa-6870-4c60-8c7a-0eddfba34d41
- questions: 18
- runs: 3
- agent_calls_ok: 54
- latency_p50_s: 11.1
- latency_p95_s: 19.6
- rows: 18
- completion: 1.0
- status_acc: 1.0
- overclaim_rate: 0.0
- fabrication_rate: 0.0
- abstain_recall: 1.0
- abstain_precision: 1.0
- quote_in_source: 0.706
- source_acc: 0.889
- contaminated_rows: 0
- row_pass_rate: 0.556
- consistency: 1.0
- audit_complete: 1.0

| Check | Value | Threshold | Pass |
| --- | --- | --- | --- |
| status_acc | 1.0 | >= 0.94 | yes |
| overclaim_rate | 0.0 | <= 0.0 | yes |
| fabrication_rate | 0.0 | <= 0.0 | yes |
| quote_in_source | 0.706 | >= 1.0 | NO |
| source_acc | 0.889 | >= 0.94 | NO |
| contaminated_rows | 0.0 | <= 0 | yes |
| consistency | 1.0 | >= 1.0 | yes |
| completion | 1.0 | >= 1.0 | yes |
| audit_complete | 1.0 | >= 1.0 | yes |
