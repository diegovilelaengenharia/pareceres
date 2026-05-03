# External Integrations

**Analysis Date:** 2026-05-01

## APIs & External Services

**None:**
- O sistema opera de forma local e offline para processamento de JSON.

## Data Storage

**Databases:**
- N/A (JSON files used as data sources)

**File Storage:**
- Local filesystem only.
  - Entradas: `1_Colar_JSON_Aqui/`
  - Saídas: `2_Documentos_Prontos/`
  - Modelos: `0_Modelos_Prontos/`

**Caching:**
- None

## Authentication & Identity

**Auth Provider:**
- None (Local access)

## Monitoring & Observability

**Error Tracking:**
- Custom logger in `_Sistema_Interno/01_Motor_Python/logger.py`
- Persistent log file in `_Sistema_Interno/01_Motor_Python/motor.log`

**Logs:**
- Console output via `colorama`
- File logging in `motor.log`

## CI/CD & Deployment

**Hosting:**
- Local Windows Machine

**CI Pipeline:**
- None (Manual testing via `run_tests.py`)

## Environment Configuration

**Required env vars:**
- N/A (Configuration is file-based in `config.py`)

**Secrets location:**
- N/A (No secrets detected)

## Webhooks & Callbacks

**Incoming:**
- None

**Outgoing:**
- None

---

*Integration audit: 2026-05-01*
