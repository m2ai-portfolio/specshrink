# SpecShrink

A Python CLI tool that reads app_spec.txt files, quantifies complexity, and tells developers whether the specification fits within a 5-iteration autonomous build pipeline.

## Tech Stack

- Python 3.11+
- Click (CLI framework)
- Rich (terminal formatting)

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Usage

### Parse a specification file

```bash
specshrink parse <file>
```

Parses the app_spec.txt file and displays the complexity breakdown.

### Score a specification file

```bash
specshrink score <file>
```

Scores the specification and determines if it fits within a 5-iteration autonomous build pipeline.

## Environment Variables

- `SPECSHRINK_THRESHOLD` - Complexity threshold for 5-iteration pipeline (default: 5)
- `SPECSHRINK_VERBOSE` - Enable verbose output (default: false)

## Quick Start

```bash
./init.sh
specshrink parse app_spec.txt
specshrink score app_spec.txt
```
