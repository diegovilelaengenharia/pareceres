# Technology Stack

**Analysis Date:** 2026-05-01

## Languages

**Primary:**
- Python 3.x - Core engine logic in `_Sistema_Interno/01_Motor_Python/`

**Secondary:**
- HTML/CSS - Used for document previews in `_Sistema_Interno/01_Motor_Python/templates/` and `painel_gem.html`

## Runtime

**Environment:**
- Python Runtime

**Package Manager:**
- pip
- Lockfile: missing (using `requirements.txt`)

## Frameworks

**Core:**
- python-docx - Word document manipulation
- jinja2 - HTML template rendering for previews

**Testing:**
- Custom test runner: `run_tests.py`

**Build/Dev:**
- Windows Batch Scripts (.bat) - Entry point `GERAR_DOCUMENTOS.bat`

## Key Dependencies

**Critical:**
- `python-docx` - Essential for generating the final documents from templates in `0_Modelos_Prontos/`
- `colorama` - Used for terminal output formatting in the motor

## Configuration

**Environment:**
- Centralized in `_Sistema_Interno/01_Motor_Python/config.py`

**Build:**
- No formal build system (interpreted Python)

## Platform Requirements

**Development:**
- Python 3.x
- Windows (implied by `.bat` files and path styles)

**Production:**
- Local execution on Windows workstations

---

*Stack analysis: 2026-05-01*
