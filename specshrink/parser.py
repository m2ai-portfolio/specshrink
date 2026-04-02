"""Parsing logic for app specifications."""

from pathlib import Path
from specshrink import SpecMetrics, ParsedSpec


def parse_spec(file_path: str) -> SpecMetrics:
    """
    Parse an app specification file and extract basic metrics.

    Args:
        file_path: Path to the specification file

    Returns:
        SpecMetrics object containing extracted counts

    Rules:
    - Lines starting with "- Feature:" count as features
    - Lines containing "http://" or "https://" count as external dependencies
    - Lines containing "api", "webhook", "database", or "db" (case-insensitive) count as integration points
    - Each line is counted in only ONE category (priority: features > external_deps > integration_points)
    """
    parsed = parse_spec_detailed(file_path)
    return parsed.metrics


def parse_spec_detailed(file_path: str) -> ParsedSpec:
    """
    Parse an app specification file and extract metrics with item details.

    Args:
        file_path: Path to the specification file

    Returns:
        ParsedSpec object containing metrics and lists of item descriptions

    Rules:
    - Lines starting with "- Feature:" count as features
    - Lines containing "http://" or "https://" count as external dependencies
    - Lines containing "api", "webhook", "database", or "db" (case-insensitive) count as integration points
    - Each line is counted in only ONE category (priority: features > external_deps > integration_points)
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Specification file not found: {file_path}")

    feature_items = []
    external_dep_items = []
    integration_items = []

    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            # Check in priority order: features first, then external deps, then integration points
            if line.startswith("- Feature:"):
                feature_items.append(line)
            elif "http://" in line or "https://" in line:
                external_dep_items.append(line)
            else:
                # Check for integration point keywords (case-insensitive)
                line_lower = line.lower()
                if any(keyword in line_lower for keyword in ["api", "webhook", "database", "db"]):
                    integration_items.append(line)

    # Create metrics
    metrics = SpecMetrics(
        features=len(feature_items),
        external_deps=len(external_dep_items),
        integration_points=len(integration_items),
        estimated_iterations=0,  # Placeholder for scorer
        within_limit=True,  # Placeholder for scorer
    )

    return ParsedSpec(
        metrics=metrics,
        feature_items=feature_items,
        external_dep_items=external_dep_items,
        integration_items=integration_items,
    )
