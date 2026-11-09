# Evidence log

| Field | Value |
| --- | --- |
| Builder |  |
| Date |  |
| Model used |  |
| Vector store File Count and chunk count |  |
| SDK version (`pip show seekrai`) |  |

## Bronze check

| Check | Runs | Result | Notes |
| --- | --- | --- | --- |
| Certification trap | 3 |  |  |
| Five-question batch | 3 |  |  |
| Planted gap | 1 |  |  |
| Look-alike numbers | 2 |  |  |
| Off-topic refusal | 1 |  |  |
| Unknown company | 1 |  |  |
| Look-alike company before upload | 1 |  |  |
| Full questionnaire | 1 |  |  |
| Look-alike company answers | 1 |  |  |
| Isolation re-test | 3 |  |  |
| Ambiguous company name | 1 |  |  |

The bronze check passes when all 18 runs pass.

## Silver check

| Agent | Result | Notes |
| --- | --- | --- |
| Documents only |  |  |
| With compliance record tool (optional) |  |  |

## Gold check

| Run | Result | Notes |
| --- | --- | --- |
| Standard questionnaire |  |  |
| Reworded questionnaire |  |  |
| Attack tests before the look-alike document |  |  |
| Attack tests after the look-alike document |  |  |
| Standard questionnaire after the look-alike document |  |  |
