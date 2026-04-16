

<p align="center">
  <img src="assets/infographic.png" alt="SpecShrink" width="800">
</p>

<h3 align="center">CLI tool that scores app_spec.txt complexity: counts features, external deps, integration points, estimated iteration budget. Flags specs likely to exceed 5 iterations and suggests cuts.</h3>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#features">Features</a> &bull;
  <a href="#examples">Examples</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

## What is this?
SpecShrink is a command‑line utility that reads an `app_spec.txt` file, quantifies its scope, and estimates how many development iterations it will likely require. It is aimed at product leads and engineers who want to catch overly ambitious specifications before they consume CI resources.

```
$ specshrink app_spec.txt
Features: 14
External dependencies: 4
Integration points: 7
Estimated iteration budget: 7
⚠️ Spec likely exceeds 5 iterations
Suggestions:
  - Remove optional feature "advanced analytics"
  - Combine API v1 and v2 clients
  - Use existing auth service instead of custom
```

## Problem
Autonomous build pipelines frequently fail on over-scoped specs, wasting compute and tokens on ideas that were never buildable in 5 iterations. No tool exists to pre-screen spec complexity before committing to a build.

## Features
| Feature | Description |
|---------|-------------|
| Spec parsing | Reads `app_spec.txt` and extracts structured sections |
| Feature counting | Tallies numbered or bullet‑listed features in the spec |
| Dependency detection | Identifies external libraries or services mentioned |
| Integration point analysis | Counts distinct APIs, hooks, or external systems referenced |
| Iteration estimation | Applies a heuristic to predict required development cycles |
| Over‑scope flagging | Emits a warning when the estimated budget exceeds a threshold |
| Improvement suggestions | Generates concrete cuts to bring the spec within limits |
| JSON output | Optional machine‑readable format for CI integration |

## Quick Start
1. Clone the repository:  
   `git clone https://github.com/m2ai-portfolio/SpecShrink.git`
2. Install the package in editable mode:  
   `cd SpecShrink && pip install -e .`
3. Run the tool on a spec file:  
   `specshrink app_spec.txt`

## Examples
### Basic scoring
Run SpecShrink on the example spec included in the repo.  
```
$ specshrink app_spec.txt
Features: 12
External dependencies: 3
Integration points: 5
Estimated iteration budget: 5
✅ Spec fits within 5 iterations
```
### Custom iteration threshold
Adjust the acceptable iteration limit with `--threshold`.  
```
$ specshrink app_spec.txt --threshold 4
Features: 12
External dependencies: 3
Integration points: 5
Estimated iteration budget: 5
⚠️ Spec likely exceeds 4 iterations
Suggestions:
  - Drop the "real‑time dashboard" feature
  - Replace custom WebSocket handler with a managed service
```
### JSON output for automation
Obtain a machine‑readable result for use in scripts or CI pipelines.  
```
$ specshrink app_spec.txt --format json
{"features":12,"external_deps":3,"integration_points":5,"estimated_iterations":5,"over_threshold":false,"suggestions":[]}
```

## File Structure
```
SpecShrink/
  assets/               # Infographic used in the README
  specshrink/           # Core source code
    __init__.py
    cli.py              # Command‑line interface entry point
    parser.py           # Parses app_spec.txt into a data model
    scorer.py           # Computes complexity metrics and iteration budget
    suggester.py        # Generates actionable reduction suggestions
  tests/                # Unit test suite
    fixtures/           # Sample spec files for testing
    test_parser.py
    test_scorer.py
    test_suggester.py
  pyproject.toml        # Project configuration and dependencies
  README.md
  app_spec.txt          # Example specification for demonstration
  init.sh               # Helper script to set up a development environment
```

## Tech Stack
| Technology | Purpose |
|------------|---------|
| Python 3.9+ | Core language implementation |
| Click | Building the CLI interface |
| PyYAML | Parsing YAML‑styled sections in specs (if used) |
| toml | Reading project configuration from pyproject.toml |

## Contributing
Fork the repository, make your changes, run the test suite, and submit a pull request.  
Ensure new features include corresponding unit tests.

## License
MIT

## Author
Matthew Snow -- [M2AI](https://m2ai.co) | [@m2ai-portfolio](https://github.com/m2ai-portfolio)