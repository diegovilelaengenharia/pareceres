# ============================================================
#  sincronizar.ps1 -- Sincroniza arquivos para upload no GEM
#  Uso: powershell -ExecutionPolicy Bypass -File _GEM_Conhecimento\sincronizar.ps1
# ============================================================

$base         = Split-Path $PSScriptRoot -Parent
$dest         = $PSScriptRoot
$prompts      = Join-Path $base "Prompts para GEM"
$conhecimento = Join-Path $base "_engine\_base_conhecimento"

$arquivos = @(
    @{ src = Join-Path $prompts      "GEM_INSTRUCOES_COMPLETAS.txt";       dst = "01_GEM_INSTRUCOES.txt";      freq = "RARO"   },
    @{ src = Join-Path $conhecimento "codex_legal.json";                   dst = "02_codex_legal.json";         freq = "RARO"   },
    @{ src = Join-Path $conhecimento "leis_referencia.md";                 dst = "03_leis_referencia.md";       freq = "RARO"   },
    @{ src = Join-Path $conhecimento "tabela_valores_e_regras_2025.md";    dst = "04_tabela_valores_multas.md"; freq = "ANUAL"  },
    @{ src = Join-Path $conhecimento "bairros_zoneamento_ipm.md";          dst = "05_bairros_zoneamento.md";    freq = "RARO"   },
    @{ src = Join-Path $conhecimento "historico_memoria_gem.md";           dst = "06_historico_memoria.md";     freq = "SEMPRE" },
    @{ src = Join-Path $conhecimento "padroes_recorrentes.md";             dst = "07_padroes_recorrentes.md";   freq = "SEMPRE" }
)

Write-Host ""
Write-Host "============================================================"
Write-Host "  SINCRONIZANDO ARQUIVOS DE CONHECIMENTO DO GEM"
Write-Host "============================================================"
Write-Host ""

$atualizados = 0
$ignorados   = 0

foreach ($a in $arquivos) {
    $destPath = Join-Path $dest $a.dst
    $srcItem  = Get-Item $a.src -ErrorAction SilentlyContinue

    if (-not $srcItem) {
        Write-Host ("  ERRO  " + $a.dst + "  origem nao encontrada") -ForegroundColor Red
        continue
    }

    $changed = $true
    if (Test-Path $destPath) {
        $destItem = Get-Item $destPath
        $changed  = ($srcItem.LastWriteTime -gt $destItem.LastWriteTime)
    }

    if ($changed) {
        Copy-Item -Path $a.src -Destination $destPath -Force
        if ($a.freq -eq "SEMPRE") {
            Write-Host ("  *** ATUALIZADO  " + $a.dst) -ForegroundColor Green
        } else {
            Write-Host ("      atualizado  " + $a.dst) -ForegroundColor Cyan
        }
        $atualizados++
    } else {
        Write-Host ("  --- sem mudanca  " + $a.dst) -ForegroundColor DarkGray
        $ignorados++
    }
}

Write-Host ""
Write-Host "------------------------------------------------------------"
Write-Host ("  " + $atualizados + " arquivo(s) atualizado(s)  |  " + $ignorados + " sem alteracao")
Write-Host "------------------------------------------------------------"

if ($atualizados -gt 0) {
    Write-Host ""
    Write-Host "  PROXIMOS PASSOS:" -ForegroundColor Yellow
    Write-Host "  1. Abra o GEM no Gemini"
    Write-Host "  2. Editar Gem > Conhecimento"
    Write-Host "  3. Substitua os arquivos marcados com *** acima"
    Write-Host "  Dica: arquivos 06 e 07 mudam apos cada parecer"
}

# ── Copia os 2 arquivos de retroalimentacao para _ATUALIZAR_GEM ─────────────
$pastaRapida = Join-Path $base "_ATUALIZAR_GEM"
if (Test-Path $pastaRapida) {
    $retro = @(
        @{ src = Join-Path $conhecimento "historico_memoria_gem.md"; nome = "historico_memoria_gem.md" },
        @{ src = Join-Path $conhecimento "padroes_recorrentes.md";   nome = "padroes_recorrentes.md"   }
    )
    Write-Host ""
    Write-Host "  Atualizando _ATUALIZAR_GEM..." -ForegroundColor Cyan
    foreach ($r in $retro) {
        Copy-Item -Path $r.src -Destination (Join-Path $pastaRapida $r.nome) -Force
        Write-Host ("  OK  " + $r.nome)
    }
}

Write-Host ""

