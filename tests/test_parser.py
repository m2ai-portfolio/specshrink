"""Tests for the parser module."""

import pytest
from pathlib import Path
from specshrink.parser import parse_spec
from specshrink import SpecMetrics


def test_parse_basic_spec(tmp_path):
    """Test parsing a basic specification with features, deps, and integration points."""
    spec_file = tmp_path / "test_spec.txt"
    spec_file.write_text("""- Feature: User login
- Feature: Export PDF
Uses https://api.payment.com
Uses database mysql
""")

    metrics = parse_spec(str(spec_file))

    assert metrics.features == 2
    assert metrics.external_deps == 1
    assert metrics.integration_points == 1


def test_parse_empty_file(tmp_path):
    """Test parsing an empty specification file."""
    spec_file = tmp_path / "empty.txt"
    spec_file.write_text("")

    metrics = parse_spec(str(spec_file))

    assert metrics.features == 0
    assert metrics.external_deps == 0
    assert metrics.integration_points == 0


def test_parse_features_only(tmp_path):
    """Test parsing a spec with only features."""
    spec_file = tmp_path / "features.txt"
    spec_file.write_text("""- Feature: Dashboard
- Feature: User profile
- Feature: Settings page
""")

    metrics = parse_spec(str(spec_file))

    assert metrics.features == 3
    assert metrics.external_deps == 0
    assert metrics.integration_points == 0


def test_parse_external_deps(tmp_path):
    """Test parsing external dependencies."""
    spec_file = tmp_path / "deps.txt"
    spec_file.write_text("""Call http://api.example.com
Uses https://service.io
Another https://cdn.example.net dependency
""")

    metrics = parse_spec(str(spec_file))

    assert metrics.features == 0
    assert metrics.external_deps == 3
    assert metrics.integration_points == 0


def test_parse_integration_points(tmp_path):
    """Test parsing integration points."""
    spec_file = tmp_path / "integration.txt"
    spec_file.write_text("""Connect to database
Call webhook endpoint
Use API gateway
Store in DB
""")

    metrics = parse_spec(str(spec_file))

    assert metrics.features == 0
    assert metrics.external_deps == 0
    assert metrics.integration_points == 4


def test_parse_mixed_content(tmp_path):
    """Test parsing content with mixed categories."""
    spec_file = tmp_path / "mixed.txt"
    spec_file.write_text("""- Feature: Authentication
Connect to database
Uses https://oauth.provider.com
- Feature: Data export
API integration required
""")

    metrics = parse_spec(str(spec_file))

    assert metrics.features == 2
    assert metrics.external_deps == 1
    assert metrics.integration_points == 2


def test_parse_case_insensitive_integration(tmp_path):
    """Test that integration point keywords are case-insensitive."""
    spec_file = tmp_path / "case.txt"
    spec_file.write_text("""Connect to DATABASE
Use Api gateway
WebHook endpoint
DB connection
""")

    metrics = parse_spec(str(spec_file))

    assert metrics.features == 0
    assert metrics.external_deps == 0
    assert metrics.integration_points == 4


def test_parse_priority_ordering(tmp_path):
    """Test that lines are counted in only one category based on priority."""
    spec_file = tmp_path / "priority.txt"
    spec_file.write_text("""- Feature: API integration with database
Uses https://api.example.com for database
Connect to api
""")

    metrics = parse_spec(str(spec_file))

    # Line 1: Starts with "- Feature:" -> counted as feature (not integration point)
    # Line 2: Contains "https://" -> counted as external dep (not integration point)
    # Line 3: Contains "api" -> counted as integration point
    assert metrics.features == 1
    assert metrics.external_deps == 1
    assert metrics.integration_points == 1


def test_parse_nonexistent_file():
    """Test parsing a non-existent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        parse_spec("nonexistent_file.txt")


def test_parse_blank_lines(tmp_path):
    """Test that blank lines are ignored."""
    spec_file = tmp_path / "blanks.txt"
    spec_file.write_text("""- Feature: Login

- Feature: Logout


Uses database
""")

    metrics = parse_spec(str(spec_file))

    assert metrics.features == 2
    assert metrics.external_deps == 0
    assert metrics.integration_points == 1


def test_parse_returns_spec_metrics(tmp_path):
    """Test that parse_spec returns a SpecMetrics object."""
    spec_file = tmp_path / "test.txt"
    spec_file.write_text("- Feature: Test")

    metrics = parse_spec(str(spec_file))

    assert isinstance(metrics, SpecMetrics)
    assert hasattr(metrics, 'features')
    assert hasattr(metrics, 'external_deps')
    assert hasattr(metrics, 'integration_points')
    assert hasattr(metrics, 'estimated_iterations')
    assert hasattr(metrics, 'within_limit')
