

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

SpecShrink is a command‑line utility that reads an `app_spec.txt` file, quantifies its scope, and predicts whether it can be built within a five‑iteration limit. It is aimed at developers and autonomous pipelines that need a fast pre‑screen to avoid wasting compute on over‑scoped ideas.

```
$ specshrink specs/example_app_spec.txt
Features: 10   External deps: 3   Integration points: 5   Est. iterations: 7
Result: EXCEEDS threshold (5) – Suggested cuts: remove feature “auto‑export”, merge “validation” and “sanitization”
```

## Problem

Autonomous build pipelines frequently fail on over-scoped specs, wasting compute and tokens on ideas that were never buildable in 5 iterations. No tool exists to pre-screen spec complexity before committing to a build.

## Features

| Feature | Description |
|---------|-------------|
| Spec parsing | Reads `app_spec.txt` and extracts feature statements, dependency declarations, and integration markers. |
| Feature counting | Tallies distinct features to gauge functional scope. |
| External dependency detection | Identifies third‑party libraries or services referenced in the spec. |
| Integration point analysis | Counts interfaces with external systems, APIs, or hardware. |
| Iteration budget estimation | Computes an estimated number of development iterations based on weighted complexity factors. |
| Threshold flagging | Highlights specs that exceed the default five‑iteration limit. |
| Cut suggestion engine | Recommends concrete removals or simplifications to bring the spec under the limit. |
| CLI interface | Provides a simple `specshrink` command with help, version, and configurable options. |

## Quick Start

1. Clone the repository  
   ```bash
   git clone https://github.com/m2ai-portfolio/SpecShrink.git
   cd SpecShrink
   ```
2. Install the package (editable mode recommended for development)  
   ```bash
   pip install -e .
   ```
3. Run the tool on a spec file  
   ```bash
   specshrink path/to/your_app_spec.txt
   ```

## Examples

**Basic scoring**  
```bash
$ specshrink fixtures/test_spec.txt
Features: 6   External deps: 1   Integration points: 2   Est. iterations: 4
Result: WITHIN threshold (5)
```
*Interpretation:* The spec is small enough to likely be completed in five iterations.

**Custom iteration threshold**  
```bash
$ specshrink fixtures/over_spec.txt --max-iters 3
Features: 14   External deps: 4   Integration points: 6   Est. iterations: 9
Result: EXCEEDS threshold (3) – Suggested cuts: drop “real‑time analytics”, combine “login” and “session‑store”, remove optional “export‑PDF”
```
*Interpretation:* With a stricter three‑iteration goal, the tool proposes three specific cuts.

**Using the suggester module directly**  
```bash
$ python -m specshrink.suggester fixtures/test_spec_2.txt
Suggested cuts:
  - Remove feature “legacy import”
  - Merge “error handling” and “logging”
  - Defer feature “batch processing” to v2
```
*Interpretation:* The suggester outputs a concise list of refactorings without the surrounding scoring metadata.

## File Structure

```
SpecShrink/
├── specshrink/              # Core source code
│   ├── __init__.py
│   ├── cli.py               # CLI entry point
│   ├── parser.py            # Spec parsing logic
│   ├── scorer.py            # Complexity scoring and threshold check
│   └── suggester.py         # Cut suggestion engine
├── tests/                   # Test suite
│   ├── fixtures/            # Sample spec files for testing
│   ├── test_parser.py
│   ├── test_scorer.py
│   └── test_suggester.py
├── pyproject.toml           # Project configuration and build system
├── README.md
└── app_spec.txt             # Example specification file
```

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.9+ | Implementation language |
| pytest     | Unit testing framework |
| setuptools | Packaging and distribution |

## Contributing

1. Fork the repository.  
2. Make your changes on a topic branch.  
3. Run the test suite (`pytest`) to ensure nothing breaks.  
4. Submit a pull request with a clear description of the fix or feature.

## License

MIT

## Author

Matthew Snow -- [M2AI](https://m2ai.co) | [@m2ai-portfolio](https://github.com/m2ai-portfolio)