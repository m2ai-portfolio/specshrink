"""Scoring logic for complexity estimation."""

import math
from specshrink import SpecMetrics


def score_spec(metrics: SpecMetrics, threshold: int = 5) -> SpecMetrics:
    """
    Calculate estimated iterations and determine if within threshold.

    Args:
        metrics: SpecMetrics object from parser
        threshold: Maximum allowed iterations (default: 5)

    Returns:
        Updated SpecMetrics with estimated_iterations and within_limit set

    Scoring formula:
        estimated = features*1 + external_deps*1.5 + integration_points*2
        Convert to integer (truncation for positive numbers)
    """
    # Calculate weighted score
    estimated_raw = (
        metrics.features * 1.0 +
        metrics.external_deps * 1.5 +
        metrics.integration_points * 2.0
    )

    # Convert to integer (truncation)
    estimated_iterations = int(estimated_raw)

    # Check if within threshold
    within_limit = estimated_iterations <= threshold

    # Return new SpecMetrics with updated values
    return SpecMetrics(
        features=metrics.features,
        external_deps=metrics.external_deps,
        integration_points=metrics.integration_points,
        estimated_iterations=estimated_iterations,
        within_limit=within_limit,
    )
