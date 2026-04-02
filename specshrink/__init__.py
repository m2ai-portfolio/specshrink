"""SpecShrink - App specification analyzer and scope reduction tool."""

from dataclasses import dataclass


@dataclass
class SpecMetrics:
    """Metrics extracted from an app specification."""
    features: int
    external_deps: int
    integration_points: int
    estimated_iterations: int
    within_limit: bool


__version__ = "0.1.0"
