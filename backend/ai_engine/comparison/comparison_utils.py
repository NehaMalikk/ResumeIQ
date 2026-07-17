"""Small pure helpers for deterministic comparison plugins."""
from __future__ import annotations
from collections.abc import Iterable
from ai_engine.features.feature_utils import EDUCATION_RANKS

def strings(value: object) -> list[str]: return [str(item) for item in value] if isinstance(value, list) else []
def overlap(resume: Iterable[str], required: Iterable[str]) -> tuple[list[str], list[str], list[str]]:
    r, j = {item.casefold(): item for item in resume}, {item.casefold(): item for item in required}
    return [r[key] for key in r.keys() & j.keys()], [j[key] for key in j.keys() - r.keys()], [r[key] for key in r.keys() - j.keys()]
def ratio(actual: float, required: float) -> float: return 100.0 if required <= 0 else round(min(actual / required, 1.0) * 100, 2)
def education_score(resume: str, job: str) -> float:
    required = EDUCATION_RANKS.get(job, 0)
    return 100.0 if required == 0 else ratio(EDUCATION_RANKS.get(resume, 0), required)
