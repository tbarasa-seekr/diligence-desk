# Gold check: FAIL

- company: Lumera Pay, Inc.
- agent_id: agent-90c785dd-24eb-49f9-a996-f87d4c145651
- questions: 18
- runs: 3
- agent_calls_ok: 54
- latency_p50_s: 14.0
- latency_p95_s: 22.9
- rows: 18
- completion: 1.0
- status_acc: 0.889
- overclaim_rate: 0.0
- fabrication_rate: 0.0
- abstain_recall: 1.0
- abstain_precision: 1.0
- quote_in_source: 0.765
- source_acc: 0.778
- contaminated_rows: 0
- row_pass_rate: 0.667
- consistency: 0.944
- audit_complete: 1.0

| Measure | Value | Required | Pass |
| --- | --- | --- | --- |
| status_acc | 0.889 | >= 0.94 | NO |
| overclaim_rate | 0.0 | <= 0.0 | yes |
| fabrication_rate | 0.0 | <= 0.0 | yes |
| quote_in_source | 0.765 | >= 1.0 | NO |
| source_acc | 0.778 | >= 0.94 | NO |
| contaminated_rows | 0.0 | <= 0 | yes |
| consistency | 0.944 | >= 1.0 | NO |
| completion | 1.0 | >= 1.0 | yes |
| audit_complete | 1.0 | >= 1.0 | yes |
