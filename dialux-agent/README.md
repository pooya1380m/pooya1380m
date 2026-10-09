# dialux-agent

Python tools for an AI agent that assists with DIALux evo lighting design.
DIALux evo has no public API, so this works on exchange files and calculations.

- `photometry.py` – parse LDT (Eulumdat) / IES files: flux, power, efficacy
- `calc.py` – lumen-method luminaire count estimate (approximate utilance)
- `compliance.py` – subset of EN 12464-1 targets (verify against the standard)
- `cli.py` – CLI; `TOOLS` dict can be registered with any tool-calling LLM

```
python -m dialux_agent.cli parse luminaire.ldt
python -m dialux_agent.cli estimate --lux 500 --length 6 --width 5 --height 2 --flux 4000
python -m dialux_agent.cli check office --em 520 --u0 0.65
python -m pytest
```

Estimates are pre-calculations; validate against DIALux results.
Not yet implemented: RAG knowledge base, C# plugin bridge, pywinauto driver.
