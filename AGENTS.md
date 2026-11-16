# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## What this is

A learning/study repo (`Codex-quickstart`) of small, standalone Python scripts exercising the `anthropic` Python SDK against the Codex Messages API. There is no application, package, or build — each file is a runnable example script demonstrating one API concept. Code comments and narration are in Portuguese; API content in prompts is generally English.

## Environment & running scripts

- Managed with `uv`: Python 3.12 (`.python-version`), direct dependencies in `pyproject.toml`, full lock in `uv.lock`. Add packages with `uv add <pkg>` (never edit `uv.lock` by hand, and don't use pip directly). See `RUNBOOK.md` for setup, auth, and troubleshooting.
- Run any script with `uv run` from the repo root (it syncs `.venv` automatically), e.g.:
  ```
  uv run src/base/chamada_input_output.py
  ```
- Scripts call `anthropic.Anthropic()` / `Anthropic()` with no explicit API key. The SDK uses `ANTHROPIC_API_KEY` if set, otherwise the `ant` CLI OAuth profile (`ant auth login`).
- No test suite, linter, or CI config in this repo.

## Structure

- `src/base/` — one script per core Messages API concept: basic call (`chamada_input_output.py`), multi-turn conversation (`turnos_input_output.py`), vision/image input (`imagem.py`), structured output via `client.messages.parse` + Pydantic (`output_formatada_analisada.py`, `output_formatada2.py`) vs. raw `output_config.format.json_schema` (`output_formatada.py`), and the four `stop_reason` values (`stop_reason1_ok.py` = `end_turn`, `stop_reason2_max_token.py` = `max_tokens`, `stop_reason3_stop_sequence.py` = `stop_sequence`, `stop_reason4_tool_use.py` = `tool_use`).
- `src/tools/` — tool-use (function calling) examples, e.g. `tool1.py` shows the full round trip: define a tool, get a `tool_use` block back, execute locally, and send a `tool_result` back to get the final answer.

## Conventions to follow when adding examples

- Keep each new concept in its own small standalone script rather than growing a shared module — that's the existing pattern across `src/base` and `src/tools`.
- Model name used throughout is `Codex-opus-5`; match existing scripts unless the example specifically needs to demonstrate model choice.
- Guard `stop_reason`/`block.type` checks the way existing scripts do (e.g. `if response.stop_reason == "tool_use":`, `if block.type == "text":`) rather than assuming response shape.
