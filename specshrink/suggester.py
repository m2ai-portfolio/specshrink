"""Suggestion logic for scope reduction."""

from specshrink import ParsedSpec
from typing import List, Tuple


def suggest_cuts(parsed_spec: ParsedSpec, threshold: int) -> List[str]:
    """
    Suggest cuts to bring the estimate under the threshold.

    Args:
        parsed_spec: ParsedSpec object with metrics and item lists
        threshold: Maximum allowed iterations

    Returns:
        List of up to 2 suggestion strings

    Rules:
    - Only active when estimate exceeds threshold (within_limit is False)
    - Each feature saves 1 iteration
    - Each external dependency saves 1.5 iterations
    - Each integration point saves 2 iterations
    - Sort items by descending savings (integration > deps > features)
    - When savings are equal, suggest items in reverse file order (last first)
    - Return up to 2 suggestions
    - Format: "Remove <type>: <description>"
    """
    # Only suggest cuts if over the limit
    if parsed_spec.metrics.within_limit:
        return []

    # Build list of (savings, type_name, description, original_index)
    candidates: List[Tuple[float, str, str, int]] = []

    # Add features (savings = 1)
    for idx, item in enumerate(parsed_spec.feature_items):
        candidates.append((1.0, "feature", item, idx))

    # Add external deps (savings = 1.5)
    for idx, item in enumerate(parsed_spec.external_dep_items):
        candidates.append((1.5, "external dependency", item, idx))

    # Add integration points (savings = 2)
    for idx, item in enumerate(parsed_spec.integration_items):
        candidates.append((2.0, "integration point", item, idx))

    # Sort by:
    # 1. Descending savings (higher savings first)
    # 2. Descending index (reverse file order when savings are equal)
    candidates.sort(key=lambda x: (-x[0], -x[3]))

    # Generate up to 2 suggestions
    suggestions = []
    for savings, type_name, description, _ in candidates[:2]:
        suggestions.append(f"Remove {type_name}: {description}")

    return suggestions
