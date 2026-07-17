"""Small pure helpers used by :mod:`recommendation_engine`."""
from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from typing import Any


ALIASES = {"skill": "skills", "keyword": "keywords", "project": "projects", "certification": "certifications", "responsibility": "responsibilities"}


def category_name(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip().lower()
    return ALIASES.get(normalized, normalized) or None


def read(value: object, name: str, default: object = None) -> object:
    return value.get(name, default) if isinstance(value, Mapping) else getattr(value, name, default)


def clamp_score(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        numeric = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    return max(0.0, min(100.0, numeric)) if math.isfinite(numeric) else None


def clean_strings(value: object) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple, set)):
        return ()
    output: list[str] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, str):
            continue
        cleaned = " ".join(item.split())
        key = cleaned.casefold()
        if cleaned and key not in seen:
            output.append(cleaned)
            seen.add(key)
    return tuple(output)


def metadata_items(metric: object, keys: Iterable[str]) -> tuple[str, ...]:
    metadata = read(metric, "metadata", {})
    if not isinstance(metadata, Mapping):
        return ()
    for key in keys:
        items = clean_strings(metadata.get(key))
        if items:
            return items
    return ()


def has_requirement(metric: object) -> bool:
    metadata = read(metric, "metadata", {})
    if not isinstance(metadata, Mapping):
        return False
    return bool(metadata.get("required") or metadata.get("required_certification") or metadata.get("preferred") or metadata.get("preferred_certification"))


def applicable(metric: object) -> bool:
    metadata = read(metric, "metadata", {})
    return not isinstance(metadata, Mapping) or metadata.get("applicable", True) is not False
