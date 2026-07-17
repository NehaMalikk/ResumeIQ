"""Deterministic conversion of comparison evidence into resume advice."""
from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from ai_engine.recommendations.recommendation_config import DEFAULT_RECOMMENDATION_CONFIG, RecommendationConfig
from ai_engine.recommendations.recommendation_models import Recommendation, RecommendationReport
from ai_engine.recommendations.recommendation_rules import applicable, category_name, clamp_score, clean_strings, has_requirement, metadata_items, read

logger = logging.getLogger(__name__)

_SCORE_FIELDS = {"skills": "skills_score", "experience": "experience_score", "education": "education_score", "projects": "projects_score", "certifications": "certifications_score", "keywords": "keywords_score", "responsibilities": "responsibilities_score", "semantic": "semantic_score"}
_TITLES = {"experience": "Strengthen experience alignment", "education": "Clarify education relevance", "projects": "Add or strengthen relevant projects", "certifications": "Highlight relevant certifications", "keywords": "Use missing job-specific keywords naturally", "responsibilities": "Align experience bullets with role responsibilities"}
_STRENGTH_TITLES = {"experience": "Strong experience alignment", "education": "Education aligns with the role", "projects": "Relevant project alignment", "certifications": "Relevant certifications are aligned", "keywords": "Strong keyword coverage", "responsibilities": "Strong responsibility alignment"}
_ACTIONS = {
    "experience": ("Move the most relevant role or bullet points higher in the experience section.", "Add measurable outcomes where accurate.", "Mention job technologies only where you genuinely used them."),
    "education": ("Include degree details or relevant coursework only if they accurately reflect your education.",),
    "projects": ("Include a project demonstrating required technology only if you have completed one.", "Describe the project problem, implementation, and outcome accurately."),
    "certifications": ("Highlight relevant certifications you already hold; do not claim certifications you have not earned.",),
    "keywords": ("Add relevant terms to experience or project bullets where accurate.", "Use the employer's terminology only when it truthfully describes your experience.", "Avoid keyword stuffing or unnatural repetition."),
    "responsibilities": ("Rewrite relevant bullets using action-oriented language.", "Show ownership of similar responsibilities where accurate.", "Include measurable outcomes where available."),
}


class RecommendationEngine:
    """Generate stable, evidence-backed recommendations without generative AI."""

    def __init__(self, config: RecommendationConfig | None = None) -> None:
        if config is not None and not isinstance(config, RecommendationConfig):
            raise TypeError("config must be a RecommendationConfig.")
        self._config = config or DEFAULT_RECOMMENDATION_CONFIG

    def generate(self, comparison_result: Any, ats_score: Any) -> RecommendationReport:
        """Produce a frontend-ready report from comparison and finalized score output."""
        if comparison_result is None:
            raise TypeError("comparison_result is required.")
        if ats_score is None or not any(hasattr(ats_score, field) or (isinstance(ats_score, Mapping) and field in ats_score) for field in ("overall_score", "skills_score", "score_breakdown")):
            raise TypeError("ats_score must provide ATS score fields.")
        logger.info("Recommendation generation started")
        warnings = list(clean_strings(read(ats_score, "warnings", ())))
        metrics = self._metrics(comparison_result, warnings)
        scores = self._scores(ats_score, warnings)
        missing_skills = self._items(metrics.get("skills"), ("missing_items",), ("missing_skills", "unmatched_skills"))[:self._config.max_missing_skills]
        keywords = self._items(metrics.get("keywords"), ("missing_items",), ("missing_keywords", "unmatched_keywords"))[:self._config.max_keyword_suggestions]
        improvements: list[Recommendation] = []
        strengths: list[Recommendation] = []
        feedback: dict[str, list[str]] = {}
        for category, score in scores.items():
            metric = metrics.get(category)
            if category == "semantic":
                if self._semantic_unavailable(metric):
                    warnings.append("Semantic similarity was not included in this analysis.")
                continue
            if metric is None:
                continue
            if category in ("education", "certifications") and not self._meaningful_optional(metric):
                continue
            generated = self._category_recommendation(category, score, metric, missing_skills, keywords)
            if generated is None:
                continue
            if generated.priority == "positive":
                strengths.append(generated)
                feedback.setdefault(category, []).append(self._strength_feedback(category))
            else:
                improvements.append(generated)
                feedback.setdefault(category, []).append(self._weak_feedback(category, missing_skills, keywords))
        improvements = self._dedupe_recommendations(improvements)
        strengths = self._dedupe_recommendations(strengths)
        improvements.sort(key=lambda rec: self._rank(rec, scores))
        strengths.sort(key=lambda rec: self._rank(rec, scores))
        displayed, truncated = self._limit(improvements, self._config.max_recommendations)
        if truncated:
            warnings.append("Additional important recommendations were omitted from the displayed list.")
        strengths = strengths[:self._config.max_strengths]
        report = RecommendationReport.build(
            summary=self._summary(self._overall(ats_score, warnings), displayed, strengths),
            overall_score=self._overall(ats_score, warnings), confidence=self._confidence(ats_score, warnings),
            recommendations=tuple(displayed), strengths=tuple(strengths), missing_skills=missing_skills,
            keyword_suggestions=keywords, section_feedback={key: clean_strings(value) for key, value in feedback.items()},
            warnings=clean_strings(warnings),
        )
        logger.info("Recommendation generation completed")
        return report

    def _metrics(self, result: Any, warnings: list[str]) -> dict[str, Any]:
        raw = read(result, "metrics", None)
        if not isinstance(raw, (list, tuple)):
            warnings.append("Comparison data was incomplete, so some recommendations may be limited.")
            return {}
        metrics: dict[str, Any] = {}
        for metric in raw:
            category = category_name(read(metric, "name"))
            if category not in _SCORE_FIELDS:
                if category:
                    warnings.append("An unsupported comparison category was ignored.")
                else:
                    warnings.append("Comparison data was incomplete, so some recommendations may be limited.")
                continue
            if category in metrics:
                warnings.append(f"Duplicate {category} comparison data was ignored.")
                continue
            if clamp_score(read(metric, "score")) is None:
                warnings.append(f"{category.capitalize()} comparison data was incomplete, so related recommendations may be limited.")
                continue
            metrics[category] = metric
        return metrics

    def _scores(self, ats_score: Any, warnings: list[str]) -> dict[str, float]:
        values: dict[str, float] = {}
        for category, field in _SCORE_FIELDS.items():
            score = clamp_score(read(ats_score, field))
            if score is not None:
                values[category] = score
            elif category != "semantic":
                warnings.append(f"{category.capitalize()} score was unavailable.")
        return values

    def _category_recommendation(self, category: str, score: float, metric: Any, missing_skills: tuple[str, ...], keywords: tuple[str, ...]) -> Recommendation | None:
        priority = self._priority(score)
        if priority == "positive":
            return Recommendation(f"strong_{category}_alignment", category, priority, _STRENGTH_TITLES.get(category, f"Strong {category} alignment"), f"Your {category} evidence is strongly aligned with this role.", "Strong alignment can improve recruiter relevance.", (), ())
        if category == "skills":
            if missing_skills:
                evidence = tuple(f"Missing skill: {item}" for item in missing_skills)
                actions = tuple(f"Mention {item} in skills, experience, or projects only if you have genuinely used it." for item in missing_skills)
                return Recommendation("missing_skills", category, priority, "Add missing required skills", "Your resume does not currently demonstrate several skills requested in the job description.", "Missing required skills can lower ATS compatibility and recruiter relevance.", evidence, actions + ("Do not add a skill solely to increase the score.",))
            return Recommendation("weak_skill_alignment", category, priority, "Improve skill alignment", "Your demonstrated skills have limited alignment with this role.", "Better-aligned skills can improve ATS compatibility.", (), ("Emphasize relevant skills only where they accurately reflect your experience.",))
        if category == "keywords" and not keywords and score >= self._config.medium_threshold:
            return None
        evidence = self._evidence(metric, category, keywords)
        return Recommendation(f"weak_{category}_alignment", category, priority, _TITLES[category], f"Your {category} evidence has limited alignment with this role.", f"Improving relevant {category} evidence can strengthen ATS compatibility and recruiter relevance.", evidence, _ACTIONS[category])

    def _items(self, metric: Any, direct_keys: tuple[str, ...], metadata_keys: tuple[str, ...]) -> tuple[str, ...]:
        if metric is None:
            return ()
        for key in direct_keys:
            items = clean_strings(read(metric, key, ()))
            if items:
                return items
        return metadata_items(metric, metadata_keys)

    def _evidence(self, metric: Any, category: str, keywords: tuple[str, ...]) -> tuple[str, ...]:
        if category == "keywords":
            return tuple(f"Missing keyword: {item}" for item in keywords)
        missing = self._items(metric, ("missing_items",), ())
        if missing:
            return tuple(f"Missing {category.rstrip('s')}: {item}" for item in missing)
        details = read(metric, "details", "")
        return (details,) if isinstance(details, str) and details.strip() else ()

    def _meaningful_optional(self, metric: Any) -> bool:
        return applicable(metric) and (has_requirement(metric) or bool(self._items(metric, ("missing_items", "matched_items"), ())))

    @staticmethod
    def _semantic_unavailable(metric: Any) -> bool:
        if metric is None or clamp_score(read(metric, "confidence")) in (None, 0.0):
            return True
        metadata = read(metric, "metadata", {})
        return isinstance(metadata, Mapping) and metadata.get("implemented") is False

    def _priority(self, score: float) -> str:
        if score < self._config.critical_threshold: return "critical"
        if score < self._config.high_threshold: return "high"
        if score < self._config.medium_threshold: return "medium"
        if score >= self._config.positive_threshold: return "positive"
        return "low"

    def _rank(self, rec: Recommendation, scores: Mapping[str, float]) -> tuple[int, int, float, str]:
        return (self._config.priority_order.index(rec.priority), self._config.category_order.index(rec.category), scores.get(rec.category, 100.0), rec.id)

    @staticmethod
    def _dedupe_recommendations(items: list[Recommendation]) -> list[Recommendation]:
        seen: set[str] = set(); output: list[Recommendation] = []
        for item in items:
            if item.id not in seen: output.append(item); seen.add(item.id)
        return output

    @staticmethod
    def _limit(items: list[Recommendation], maximum: int) -> tuple[list[Recommendation], bool]:
        return items[:maximum], len(items) > maximum

    @staticmethod
    def _weak_feedback(category: str, skills: tuple[str, ...], keywords: tuple[str, ...]) -> str:
        if category == "skills" and skills: return "Several required skills were not found."
        if category == "keywords" and keywords: return "Some job-specific keywords were not found."
        return f"{category.capitalize()} alignment could be strengthened."

    @staticmethod
    def _strength_feedback(category: str) -> str:
        return f"{category.capitalize()} evidence is strongly aligned with the role."

    def _overall(self, ats_score: Any, warnings: list[str]) -> float:
        score = clamp_score(read(ats_score, "overall_score"))
        if score is None:
            warnings.append("Overall score was unavailable; a safe zero score was used.")
            return 0.0
        return score

    @staticmethod
    def _confidence(ats_score: Any, warnings: list[str]) -> float:
        value = clamp_score(read(ats_score, "confidence"))
        if value is None: warnings.append("Score confidence was unavailable."); return 0.0
        return min(1.0, value)

    @staticmethod
    def _summary(score: float, recommendations: list[Recommendation], strengths: list[Recommendation]) -> str:
        category = recommendations[0].category if recommendations else (strengths[0].category if strengths else "general")
        labels = {"skills": "Skills", "keywords": "keyword coverage", "experience": "experience", "responsibilities": "responsibility alignment"}
        focus = labels.get(category, category)
        if score >= 90: return "Your resume has excellent alignment with this role."
        if score >= 75: return f"Your resume is strongly aligned with this role, with a few targeted {focus} improvements available."
        if score >= 60: return f"Your resume currently has moderate alignment. {focus.capitalize()} should be improved first."
        if score >= 40: return f"Your resume has weak alignment with this role. Prioritize {focus} gaps before applying."
        return f"Your resume has poor alignment with this role. Prioritize the largest {focus} gaps before applying."
