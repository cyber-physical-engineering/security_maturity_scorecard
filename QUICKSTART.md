# Quick start

Python 3.10 or later (tested on 3.12).

```bash
pip install -r requirements.txt
streamlit run maturity_app.py
```

Open http://localhost:8501.

## Using it

1. Pick a pack in the sidebar. Five ship: 10, 15, 21, 50 and 53 questions.
2. Answer each question Yes, No or N/A. Every question starts as N/A, and N/A answers are left out of the score.
3. Read the score, the radar chart and the top five gaps.
4. Download the Markdown report. It lists up to ten gaps with recommendations and references, and a 30, 60 and 90-day checklist.

## Adding a pack

Create a YAML file in `question_packs/` with the same fields as the shipped packs (see the README for an example that loads). `weight` defaults to 5 if left out.

## Tests

```bash
pip install pytest
pytest -q
```

Fourteen tests. Thirteen drive the app with Streamlit's AppTest: every pack's count matches its name, nothing is scored before an answer, all-Yes scores 100 and all-No scores 0 for every pack, a mixed answer gives the expected weighted percentage, and no MFA question cites 45 CFR 164.312(a)(2)(i). One calls the report function directly: when CRITICAL gaps fill the top ten, the 60-day list still carries HIGH gaps.
