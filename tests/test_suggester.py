"""Tests for the suggester module (Feature 3)."""

import pytest
from specshrink import SpecMetrics, ParsedSpec
from specshrink.suggester import suggest_cuts


def test_no_suggestions_when_within_limit():
    """Should return empty list when within threshold."""
    metrics = SpecMetrics(
        features=2,
        external_deps=1,
        integration_points=0,
        estimated_iterations=3,  # 2*1 + 1*1.5 = 3.5 -> 3
        within_limit=True,
    )
    parsed_spec = ParsedSpec(
        metrics=metrics,
        feature_items=["- Feature: Login", "- Feature: Dashboard"],
        external_dep_items=["Uses https://api.example.com"],
        integration_items=[],
    )

    suggestions = suggest_cuts(parsed_spec, threshold=5)
    assert suggestions == []


def test_suggest_integration_point_first():
    """Should suggest integration point first (highest savings)."""
    metrics = SpecMetrics(
        features=1,
        external_deps=1,
        integration_points=1,
        estimated_iterations=4,  # 1 + 1.5 + 2 = 4.5 -> 4
        within_limit=False,
    )
    parsed_spec = ParsedSpec(
        metrics=metrics,
        feature_items=["- Feature: Login"],
        external_dep_items=["Uses https://api.example.com"],
        integration_items=["Uses database postgres"],
    )

    suggestions = suggest_cuts(parsed_spec, threshold=3)

    # First suggestion should be integration point (saves 2)
    assert len(suggestions) == 2
    assert suggestions[0] == "Remove integration point: Uses database postgres"
    assert suggestions[1] == "Remove external dependency: Uses https://api.example.com"


def test_suggest_up_to_two_items():
    """Should return at most 2 suggestions."""
    metrics = SpecMetrics(
        features=5,
        external_deps=2,
        integration_points=2,
        estimated_iterations=12,  # 5 + 3 + 4 = 12
        within_limit=False,
    )
    parsed_spec = ParsedSpec(
        metrics=metrics,
        feature_items=[
            "- Feature: Login",
            "- Feature: Dashboard",
            "- Feature: Reports",
            "- Feature: Settings",
            "- Feature: Analytics",
        ],
        external_dep_items=[
            "Uses https://api.a.com",
            "Uses https://api.b.com",
        ],
        integration_items=[
            "Uses database mysql",
            "Uses webhook notifications",
        ],
    )

    suggestions = suggest_cuts(parsed_spec, threshold=5)

    # Should return exactly 2 suggestions
    assert len(suggestions) == 2
    # Both should be integration points (highest savings)
    assert "integration point" in suggestions[0]
    assert "integration point" in suggestions[1]


def test_reverse_file_order_for_equal_savings():
    """When savings are equal, suggest items in reverse file order."""
    metrics = SpecMetrics(
        features=0,
        external_deps=3,
        integration_points=0,
        estimated_iterations=4,  # 3*1.5 = 4.5 -> 4
        within_limit=False,
    )
    parsed_spec = ParsedSpec(
        metrics=metrics,
        feature_items=[],
        external_dep_items=[
            "Uses https://api.a.com",  # index 0
            "Uses https://api.b.com",  # index 1
            "Uses https://api.c.com",  # index 2
        ],
        integration_items=[],
    )

    suggestions = suggest_cuts(parsed_spec, threshold=3)

    # Should suggest last items first (reverse order)
    assert len(suggestions) == 2
    assert suggestions[0] == "Remove external dependency: Uses https://api.c.com"
    assert suggestions[1] == "Remove external dependency: Uses https://api.b.com"


def test_mixed_savings_sorted_correctly():
    """Should sort by savings first, then by reverse index."""
    metrics = SpecMetrics(
        features=2,
        external_deps=2,
        integration_points=1,
        estimated_iterations=8,  # 2 + 3 + 2 = 7
        within_limit=False,
    )
    parsed_spec = ParsedSpec(
        metrics=metrics,
        feature_items=[
            "- Feature: Login",
            "- Feature: Dashboard",
        ],
        external_dep_items=[
            "Uses https://api.a.com",
            "Uses https://api.b.com",
        ],
        integration_items=[
            "Uses database postgres",
        ],
    )

    suggestions = suggest_cuts(parsed_spec, threshold=5)

    # First should be integration (saves 2)
    # Second should be last external dep (saves 1.5)
    assert len(suggestions) == 2
    assert suggestions[0] == "Remove integration point: Uses database postgres"
    assert suggestions[1] == "Remove external dependency: Uses https://api.b.com"


def test_only_one_item_available():
    """Should return only one suggestion if only one item exists."""
    metrics = SpecMetrics(
        features=1,
        external_deps=0,
        integration_points=0,
        estimated_iterations=1,
        within_limit=False,
    )
    parsed_spec = ParsedSpec(
        metrics=metrics,
        feature_items=["- Feature: Login"],
        external_dep_items=[],
        integration_items=[],
    )

    suggestions = suggest_cuts(parsed_spec, threshold=0)

    assert len(suggestions) == 1
    assert suggestions[0] == "Remove feature: - Feature: Login"


def test_spec_example_case():
    """Test the exact example from the spec."""
    metrics = SpecMetrics(
        features=3,
        external_deps=2,
        integration_points=1,
        estimated_iterations=8,  # 3 + 3 + 2 = 8
        within_limit=False,
    )
    parsed_spec = ParsedSpec(
        metrics=metrics,
        feature_items=[
            "- Feature: Login",
            "- Feature: Dashboard",
            "- Feature: Notifications",
        ],
        external_dep_items=[
            "Uses https://api.a.com",
            "Uses https://api.b.com",
        ],
        integration_items=[
            "Uses database postgres",
        ],
    )

    suggestions = suggest_cuts(parsed_spec, threshold=6)

    # Should suggest integration first, then last external dep
    assert len(suggestions) == 2
    assert suggestions[0] == "Remove integration point: Uses database postgres"
    assert suggestions[1] == "Remove external dependency: Uses https://api.b.com"
