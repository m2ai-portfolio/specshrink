"""Parsing logic for app specifications."""

from pathlib import Path
from specshrink import SpecMetrics


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
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Specification file not found: {file_path}")

    features = 0
    external_deps = 0
    integration_points = 0

    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            # Check in priority order: features first, then external deps, then integration points
            if line.startswith("- Feature:"):
                features += 1
            elif "http://" in line or "https://" in line:
                external_deps += 1
            else:
                # Check for integration point keywords (case-insensitive)
                line_lower = line.lower()
                if any(keyword in line_lower for keyword in ["api", "webhook", "database", "db"]):
                    integration_points += 1

    # For now, estimated_iterations and within_limit are placeholders
    # These will be implemented in Feature 2 (scorer.py)
    return SpecMetrics(
        features=features,
        external_deps=external_deps,
        integration_points=integration_points,
        estimated_iterations=0,  # Placeholder for Feature 2
        within_limit=True,  # Placeholder for Feature 2
    )
