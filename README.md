# Security Maturity Scorecard

A Streamlit questionnaire that scores answers to healthcare cybersecurity questions stored in YAML packs. The score is the share of weighted controls answered Yes. It is a self-assessment, not a measured maturity level.

**Status: prototype.** 14 tests pass (13 through Streamlit's AppTest and one on the report function), and the app starts headless (October 2, 2026; Python 3.12.15, Apple Silicon Mac).

James Thornton set the architecture and requirements. The code was written with AI-assisted development in late 2025. The tests and checks were re-run in October 2026.

## What it does

- Loads every YAML file in `question_packs/` and shows each question as a Yes, No or N/A radio button in the sidebar. Every question starts as N/A.
- Scores the answers as a weighted percentage: the weights of the questions answered Yes, divided by the weights of the questions not marked N/A, times 100. Nothing is scored until at least one question is answered Yes or No.
- Draws a radar chart of per-domain percentages. A domain with only N/A answers reads "not scored".
- Lists up to five questions answered No, ordered by the pack's risk label (CRITICAL, HIGH, MEDIUM) and then by weight, each with the pack's recommendation.
- Downloads a Markdown report with up to ten gaps, each gap's recommendation and stored references, and a 30, 60 and 90-day checklist built from the gaps.

Five packs ship:

| File | Questions | Domains |
|---|---|---|
| `quick_10.yaml` | 10 | 3 |
| `hipaa_15.yaml` | 15 | 3 |
| `standard_20.yaml` | 21 | 4 |
| `trust_stack_50.yaml` | 50 | 5 (Secure, Control, Comply, Verify, Prove) |
| `enterprise_50.yaml` | 53 | 11 |

Weights are set in the YAML by the pack's author; the shipped packs use 6 to 10. The score bands are 0 to 49 CRITICAL RISK, 50 to 69 HIGH RISK, 70 to 84 MODERATE RISK, and 85 to 100 ROBUST POSTURE.

## Quick start

Python 3.10 or later (tested on 3.12).

```bash
git clone https://github.com/cyber-physical-engineering/security_maturity_scorecard.git
cd security_maturity_scorecard
pip install -r requirements.txt
streamlit run maturity_app.py
```

The app opens at http://localhost:8501.

Run the tests:

```bash
pip install pytest
pytest -q
```

## Writing a pack

A pack is a YAML file in `question_packs/` with the same fields as the shipped packs. `weight` defaults to 5 if left out; `description` and `version` have defaults too. This example loads and scores:

```yaml
name: "Your Custom Assessment"
description: "Description here"
version: "1.0"
domains:
  - name: "Security Domain"
    questions:
      - id: "custom_01"
        text: "Your question here?"
        weight: 8
        risk_if_no: "HIGH"
        recommendation: "What to do if answer is No"
        compliance_refs:
          hipaa: ["164.308(a)(1)"]
          nist_csf: ["PR.AC-1"]
```

## About the references

Each question lists HIPAA Security Rule paragraphs and NIST Cybersecurity Framework subcategory IDs. The IDs are CSF 1.1; eleven of them sit in categories CSF 2.0 removed. FDA items are tagged "premarket" or "postmarket", and GxP items are keywords. The references point to related sections of those documents. They are a starting point for a reviewer, not a compliance determination. The references appear in the downloaded report, not on screen.

## Limits

- The score is the share of weighted Yes answers. It is not a measured maturity level and not a risk measurement.
- Weights and risk labels are the pack author's judgment.
- The citations point to related sections; about a quarter of them are loose fits, and none makes a finding.
- One pack at a time; there is no history, benchmark or comparison.
- The app runs on your machine. There is no hosted instance.

## License

MIT. See [LICENSE](LICENSE).
