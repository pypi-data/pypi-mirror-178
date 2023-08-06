## pyproject-tag-check

I always forget to bump poetry version in pyproject.toml files. That's why I build this simple package. It is pre-commit hook which check that version in pyproject.toml is not used as a tag for given repo URL.

## Usage:


Put it in `.pre-commit.config.yaml` repos and argument must be URL to repo on GH (for example https://github.com/rafsaf/Tribal-Wars-Planer).

```yml
repos:
  - repo: https://github.com/rafsaf/pyproject-tag-check
    rev: "0.1.0"
    hooks:
      - id: pyproject-tag-check
        args:
          - https://github.com/rafsaf/Tribal-Wars-Planer

```
