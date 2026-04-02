

# SpecShrink


## Overview
SpecShrink is a command‑line utility that analyzes formal specification files, scores their quality, and provides actionable suggestions for improvement. It is aimed at software engineers, architects, and technical writers who need to keep large specification documents clear, consistent, and maintainable.

## Problem Statement
Large technical specifications often suffer from redundancy, ambiguous wording, and inconsistent formatting, making them hard to review and evolve. Manual inspection is time‑consuming and error‑prone. SpecShrink automates the detection of these issues, quantifies spec health, and recommends concrete refactorings to shrink the spec while preserving its intent.

## Features
- **Spec parsing** – robustly reads structured specification files (`.spec`, `.txt`, etc.).
- **Quality scoring** – computes metrics such as redundancy, clarity, and conformance to style guides.
- **Improvement suggestions** – generates concise, actionable rewrites to reduce size and improve readability.
- **CLI interface** – simple commands for parsing, scoring, and suggesting.
- **Extensible design** – modular parser, scorer, and suggester components can be replaced or extended.
- **Test suite** – includes unit tests for core functionality to ensure reliability.
- **Packaging** – modern `pyproject.toml` based distribution installable via `pip`.

## Tech Stack
- **Language**: Python 3.9+
- **Packaging**: `setuptools` via `pyproject.toml`
- **CLI building**: `argparse` (in `cli.py`)
- **Testing**: `pytest` (tests under `tests/`)
- **Other**: standard library only; no external dependencies required.

## Quick Start / Installation

```bash
# Clone the repository
git clone <repo-url>
cd metroplex-ideaforge-135-r2

# Install in editable mode (recommended for development)
pip install -e .

# Or install from built distribution
pip install .
```

After installation, the `specshrink` command is available:

```bash
specshrink --help
```

## Usage

```bash
# Parse a spec file and show a summary
specshrink parse path/to/spec.txt

# Score the spec (outputs a numeric quality score)
specshrink score path/to/spec.txt

# Generate improvement suggestions
specshrink suggest path/to/spec.txt

# Run the test suite
pytest
```

## Architecture

```
specshrink/
├── __init__.py
├── cli.py        # Entry point; defines subcommands parse, score, suggest
├── parser.py     # Reads and normalizes specification files into an internal AST
├── scorer.py     # Computes quality metrics from the AST
└── suggester.py  # Produces rewrite suggestions based on scorer output
```

- **cli.py** dispatches user commands to the appropriate module.  
- **parser.py** turns raw text into a structured representation (e.g., sections, requirements, diagrams).  
- **scorer.py** walks the AST and calculates scores for redundancy, vagueness, formatting, etc.  
- **suggester.py** uses the scores to propose specific edits (e.g., merge duplicate requirements, reword ambiguous clauses).

## License

MIT

© 2025 SpecShrink Contributors. See `LICENSE` for details.