"""Tests for the scorer module (Feature 2)."""

import pytest
from specshrink.scorer import score_spec
from specshrink import SpecMetrics


def test_score_basic_spec():
    """Test scoring a basic specification."""
    # Create metrics: 2 features, 1 external dep, 1 integration point
    # Score: 2*1 + 1*1.5 + 1*2 = 2 + 1.5 + 2 = 5.5, int = 5
    metrics = SpecMetrics(
        features=2,
        external_deps=1,
        integration_points=1,
        estimated_iterations=0,
        within_limit=True
    )

    scored = score_spec(metrics, threshold=5)

    assert scored.features == 2
    assert scored.external_deps == 1
    assert scored.integration_points == 1
    assert scored.estimated_iterations == 5
    assert scored.within_limit == True  # 5 <= 5


def test_score_with_default_threshold():
    """Test scoring with default threshold of 5."""
    metrics = SpecMetrics(
        features=3,
        external_deps=0,
        integration_points=0,
        estimated_iterations=0,
        within_limit=True
    )

    scored = score_spec(metrics)  # Default threshold = 5

    assert scored.estimated_iterations == 3
    assert scored.within_limit == True  # 3 <= 5


def test_score_within_limit():
    """Test a specification that passes the threshold."""
    # 1 feature, 1 dep, 0 integration: 1 + 1.5 = 2.5, int = 2
    metrics = SpecMetrics(
        features=1,
        external_deps=1,
        integration_points=0,
        estimated_iterations=0,
        within_limit=True
    )

    scored = score_spec(metrics, threshold=5)

    assert scored.estimated_iterations == 2
    assert scored.within_limit == True


def test_score_exceeds_limit():
    """Test a specification that fails the threshold."""
    # 3 features, 2 deps, 2 integration: 3 + 3 + 4 = 10
    metrics = SpecMetrics(
        features=3,
        external_deps=2,
        integration_points=2,
        estimated_iterations=0,
        within_limit=True
    )

    scored = score_spec(metrics, threshold=5)

    assert scored.estimated_iterations == 10
    assert scored.within_limit == False


def test_score_exactly_at_limit():
    """Test a specification that exactly meets the threshold."""
    # 5 features, 0 deps, 0 integration: 5
    metrics = SpecMetrics(
        features=5,
        external_deps=0,
        integration_points=0,
        estimated_iterations=0,
        within_limit=True
    )

    scored = score_spec(metrics, threshold=5)

    assert scored.estimated_iterations == 5
    assert scored.within_limit == True  # 5 <= 5


def test_score_empty_spec():
    """Test scoring an empty specification."""
    metrics = SpecMetrics(
        features=0,
        external_deps=0,
        integration_points=0,
        estimated_iterations=0,
        within_limit=True
    )

    scored = score_spec(metrics, threshold=5)

    assert scored.estimated_iterations == 0
    assert scored.within_limit == True


def test_score_features_only():
    """Test scoring with only features."""
    # 4 features: 4*1 = 4
    metrics = SpecMetrics(
        features=4,
        external_deps=0,
        integration_points=0,
        estimated_iterations=0,
        within_limit=True
    )

    scored = score_spec(metrics, threshold=5)

    assert scored.estimated_iterations == 4
    assert scored.within_limit == True


def test_score_deps_only():
    """Test scoring with only external dependencies."""
    # 2 deps: 2*1.5 = 3
    metrics = SpecMetrics(
        features=0,
        external_deps=2,
        integration_points=0,
        estimated_iterations=0,
        within_limit=True
    )

    scored = score_spec(metrics, threshold=5)

    assert scored.estimated_iterations == 3
    assert scored.within_limit == True


def test_score_integration_only():
    """Test scoring with only integration points."""
    # 2 integration points: 2*2 = 4
    metrics = SpecMetrics(
        features=0,
        external_deps=0,
        integration_points=2,
        estimated_iterations=0,
        within_limit=True
    )

    scored = score_spec(metrics, threshold=5)

    assert scored.estimated_iterations == 4
    assert scored.within_limit == True


def test_score_truncation():
    """Test that scoring truncates fractional results."""
    # 1 dep: 1*1.5 = 1.5, int truncates to 1
    metrics = SpecMetrics(
        features=0,
        external_deps=1,
        integration_points=0,
        estimated_iterations=0,
        within_limit=True
    )

    scored = score_spec(metrics, threshold=5)

    assert scored.estimated_iterations == 1  # Truncated from 1.5


def test_score_with_low_threshold():
    """Test scoring with a very low threshold."""
    # 2 features: 2
    metrics = SpecMetrics(
        features=2,
        external_deps=0,
        integration_points=0,
        estimated_iterations=0,
        within_limit=True
    )

    scored = score_spec(metrics, threshold=1)

    assert scored.estimated_iterations == 2
    assert scored.within_limit == False  # 2 > 1


def test_score_with_high_threshold():
    """Test scoring with a very high threshold."""
    # 5 features, 3 deps, 2 integration: 5 + 4.5 + 4 = 13.5, int = 13
    metrics = SpecMetrics(
        features=5,
        external_deps=3,
        integration_points=2,
        estimated_iterations=0,
        within_limit=True
    )

    scored = score_spec(metrics, threshold=20)

    assert scored.estimated_iterations == 13
    assert scored.within_limit == True  # 13 <= 20


def test_score_preserves_original_counts():
    """Test that scoring preserves the original feature/dep/integration counts."""
    original_metrics = SpecMetrics(
        features=2,
        external_deps=1,
        integration_points=1,
        estimated_iterations=0,
        within_limit=True
    )

    scored = score_spec(original_metrics, threshold=5)

    # Original counts should be preserved
    assert scored.features == original_metrics.features
    assert scored.external_deps == original_metrics.external_deps
    assert scored.integration_points == original_metrics.integration_points
