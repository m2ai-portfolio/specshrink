"""SpecShrink - App specification analyzer and scope reduction tool."""

from dataclasses import dataclass
from typing import List


@dataclass
class SpecMetrics:
    """Metrics extracted from an app specification."""
    features: int
    external_deps: int
    integration_points: int
    estimated_iterations: int
    within_limit: bool


@dataclass
class ParsedSpec:
    """Full parsed specification with metrics and item lists."""
    metrics: SpecMetrics
    feature_items: List[str]
    external_dep_items: List[str]
    integration_items: List[str]


__version__ = "0.1.0"
