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

CONCEPT_GROUPS = {
    "reusable components": ("reusable", "modular", "component"),
    "performance and scalability": ("optimiz", "performance", "page load", "bottleneck", "scalab"),
    "REST API": ("rest api", "restful api", "api integration", "integrated api"),
    "collaboration": ("collaborat", "cross-functional", "backend engineer", "qa tester", "designer"),
    "maintainability": ("maintainab", "clean code", "modular code"),
}

def concept_matches(evidence: Iterable[str], requirements: Iterable[str]) -> tuple[list[str], list[str], dict[str, str]]:
    sources = [str(item) for item in evidence]
    matched, missing, support = [], [], {}
    for requirement in requirements:
        lower = requirement.casefold()
        concepts = [name for name, terms in CONCEPT_GROUPS.items() if any(term in lower for term in terms)]
        found = next((source for source in sources if any(any(term in source.casefold() for term in CONCEPT_GROUPS[name]) for name in concepts)), None)
        if found: matched.append(requirement); support[requirement] = found
        else: missing.append(requirement)
    return matched, missing, support
