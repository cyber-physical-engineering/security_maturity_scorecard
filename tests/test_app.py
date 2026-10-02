"""App tests: every pack loads, scoring is right, and nothing is scored before an answer."""

from __future__ import annotations

import ast
import re
from datetime import datetime
from pathlib import Path

import pytest
import yaml
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
APP = str(ROOT / "maturity_app.py")
PACKS = sorted((ROOT / "question_packs").glob("*.yaml"))
LABEL = {"yes": "✅ Yes", "no": "❌ No", "n/a": "⊘ N/A (Optional)"}


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


def questions(pack: dict) -> list[dict]:
    return [q for d in pack["domains"] for q in d["questions"]]


def score_card(at: AppTest) -> str:
    for m in at.markdown:
        if 'class="score-number"' in m.value:
            return re.search(r'class="score-number">([^<]+)<', m.value).group(1)
    raise AssertionError("no score card")


def answer_all(at: AppTest, pack_name: str, answer) -> AppTest:
    at.sidebar.selectbox[0].set_value(pack_name)
    at.run()
    for radio in at.sidebar.radio:
        radio.set_value(LABEL[answer(radio)])
    at.run()
    return at


@pytest.mark.parametrize("path", PACKS, ids=lambda p: p.stem)
def test_pack_question_count_matches_its_name(path: Path) -> None:
    pack = load(path)
    stated = int(re.search(r"\((\d+) Questions\)", pack["name"]).group(1))
    assert len(questions(pack)) == stated


def test_first_screen_shows_no_score_and_no_alarm() -> None:
    at = AppTest.from_file(APP, default_timeout=60)
    at.run()
    assert not at.exception
    assert score_card(at) == "Not scored"
    assert not any("Score under 50" in m.value for m in at.markdown)


@pytest.mark.parametrize("path", PACKS, ids=lambda p: p.stem)
def test_all_yes_scores_100_and_all_no_scores_0(path: Path) -> None:
    name = load(path)["name"]
    at = AppTest.from_file(APP, default_timeout=60)
    at.run()
    assert score_card(answer_all(at, name, lambda r: "yes")) == "100.0/100"
    assert score_card(answer_all(at, name, lambda r: "no")) == "0.0/100"
    assert not at.exception


def test_weighted_score_counts_weights_not_questions() -> None:
    path = ROOT / "question_packs" / "quick_10.yaml"
    pack = load(path)
    qs = questions(pack)
    first, second = qs[0], qs[1]
    expected = first["weight"] / (first["weight"] + second["weight"]) * 100

    at = AppTest.from_file(APP, default_timeout=60)
    at.run()
    labels = {q["text"]: q["id"] for q in qs}

    def answer(radio) -> str:
        qid = labels.get(radio.label)
        return {first["id"]: "yes", second["id"]: "no"}.get(qid, "n/a")

    assert score_card(answer_all(at, pack["name"], answer)) == f"{expected:.1f}/100"


def test_mfa_questions_cite_person_or_entity_authentication() -> None:
    for path in PACKS:
        for q in questions(load(path)):
            if "MFA" in q["text"] or "multi-factor" in q["text"].lower():
                hipaa = q.get("compliance_refs", {}).get("hipaa", [])
                assert "164.312(a)(2)(i)" not in hipaa, (path.stem, q["id"])


def report_functions() -> dict:
    """Load the scoring and report functions from the app without running the page."""
    tree = ast.parse(Path(APP).read_text())
    wanted = {"calculate_weighted_score", "generate_markdown_report"}
    body = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in wanted]
    ns: dict = {"datetime": datetime}
    exec(compile(ast.Module(body=body, type_ignores=[]), APP, "exec"), ns)
    return ns


def test_report_plan_keeps_high_gaps_when_critical_gaps_fill_the_top_ten() -> None:
    ns = report_functions()
    for stem in ("enterprise_50", "trust_stack_50"):
        pack = load(ROOT / "question_packs" / f"{stem}.yaml")
        responses = {q["id"]: "no" for q in questions(pack)}
        score, domains, gaps, *_ = ns["calculate_weighted_score"](responses, pack)
        report = ns["generate_markdown_report"](pack["name"], pack, responses, score, domains, gaps)
        assert "## Top 10 gaps" in report, stem
        plan_60 = report.split("### Short-term (60 Days)")[1].split("###")[0]
        assert "No HIGH gaps" not in plan_60, stem
        assert plan_60.count("- [ ]") == 3, stem
