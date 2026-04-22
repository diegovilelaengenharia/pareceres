# ==========================================
# PARTE 4: MOTOR EMERGENCIAL — GUIA DE USO MANUAL
# ==========================================

> **Use este guia quando o Antigravity estiver com o limite de contexto esgotado.**
> Você pode gerar documentos DOCX e PDF manualmente, sem depender da IA.

---

## PASSO A PASSO EMERGENCIAL

1. Acesse: `3_Treinar_Inteligencia/03_MOTOR_EMERGENCIAL_GEM.py`
2. **Copie** esse arquivo para a **RAIZ do projeto** (`02. Pareceres/`)
3. Cole o JSON do processo em: `1_Colar_JSON_Aqui/nome_processo.json`
4. Abra o terminal na pasta raiz e execute:
   ```
   python 03_MOTOR_EMERGENCIAL_GEM.py
   ```
5. O DOCX e PDF estarão prontos em `2_Documentos_Prontos/`

### Dependências (instalar uma vez)
```bash
pip install python-docx docx2pdf
```

---

## TIPOS DE RELATÓRIO DISPONÍVEIS

O campo `"tipo_relatorio"` no JSON define qual documento será gerado.

### Pareceres Técnicos — com carimbo completo (área, proprietário, etc.)
| Tipo | Uso |
|---|---|
| `alvara_aprovacao` | Aprovação de novo projeto |
| `alvara_regularizacao` | Regularização (As Built) |
| `alvara_ampliacao` | Ampliação de edificação existente |
| `alvara_galpao_comercial` | Galpão / Uso comercial |
| `alvara_reforma_demolicao_ampliacao` | Reforma com demolição parcial |
| `alvara_substituicao_projeto` | Novo projeto sobre alvará existente |
| `regularizacao` | Alias de compatibilidade |

### Pareceres Simples — sem carimbo (certidões, habite-se)
| Tipo | Uso |
|---|---|
| `certidao_desmembramento` | **Exemplo: Processo 4924/2025 (Márcia)** |
| `certidao_retificacao_area` | Retificação registral de área |
| `certidao_averbacao_decadencia` | Averbação com decadência tributária |
| `certidao_numero_2via` | 2ª via de numeração |
| `certidao_nome_rua` | Certidão de logradouro |
| `certidao_localizacao` | Localização do imóvel |
| `certidao_conjunta` | Certidão múltipla |
| `certidao_numero_comercial` | Numeração comercial |
| `certidao_demolicao` | Certidão de demolição |
| `habitese_comum` | Habite-se padrão |
| `habitese_multa` | Habite-se com multa por obra irregular |
| `habitese_2via` | 2ª via de Habite-se |
| `habitese_inclusao_area` | Habite-se com inclusão de área |
| `alvara_renovacao` | Renovação de alvará |
| `alvara_cancelamento` | Cancelamento de alvará |
| `alvara_substituicao_titular` | Troca de titular do alvará |
| `alvara_demolicao` | Alvará de demolição |

### Ofícios
| Tipo | Uso |
|---|---|
| `oficio_meio_ambiente` | Encaminhamento ao CODEMA |
| `parecer_juridico` | Parecer jurídico interno |
| `oficio_juridico_embargo` | Notificação de embargo |
| `oficio_interno_materiais` | Requisição interna de materiais |
| `oficio_decreto_utilidade` | Utilidade pública |

### Comunicados
| Tipo | Uso |
|---|---|
| `comunicado_pendencia` | **Exemplo: Processo 164/2026 (Antonio)** |
| `comunicado_indeferimento` | Comunicado de indeferimento |

### Documentos Finais da Secretaria (balcão)
| Tipo | Uso |
|---|---|
| `alvara_oficial` | Alvará físico para entrega |
| `carta_habitese_oficial` | Carta de Habite-se oficial |
| `certidao_oficial` | Certidão oficial |

---

## ESTRUTURA MÍNIMA DO JSON

```json
{
    "memoria_de_calculo": "[OBRIGATÓRIO: escreva as contas de Taxa de Ocupação, Permeabilidade, fator SERO, etc.]",
    "tipo_relatorio": "certidao_desmembramento",
    "numero_processo": "4924/2025",
    "data_processo": "12/06/2025",
    "assunto": "CERTIDÃO DE DESMEMBRAMENTO (TOPOGRAFIA)",
    "requerente": "NOME DO REQUERENTE",
    "logradouro": "Rua Exemplo, SN",
    "bairro": "BAIRRO",
    "inscricao_municipal": "01.00.000.0000",
    "proprietario": "NOME DO PROPRIETÁRIO",
    "desenhista": "NOME DO DESENHISTA/RESPONSÁVEL",
    "lote": "01",
    "quadra": "A",
    "area_terreno": "200,00m²",
    "area_total_construida": "80,00m²",
    "taxa_ocupacao": "40%",
    "coef_aproveitamento": "0,40",
    "taxa_permeabilidade": "30%",
    "profissional_nome": "NOME DO PROFISSIONAL",
    "paragrafo_abertura": "[Texto formal descrevendo o processo]",
    "considerandos": [
        "Considerando que [fato 1];",
        "Considerando que [fato 2];"
    ],
    "fundamentacao_legal": [
        "__Art. X da Lei Y:__ Explicação de como se aplica ao caso."
    ],
    "conclusao": "Profiro PARECER FAVORÁVEL / DESFAVORÁVEL [fundamentação].",
    "condicoes_pendentes": [],
    "documentos_emitir": [
        {
            "tipo": "Nome completo do documento gerado",
            "obs": "Observações legais, validade, condicionantes."
        }
    ],
    "licao_aprendida": "(OPCIONAL) Situação incomum não prevista nas instruções."
}
```

---

## REGRAS DE BLINDAGEM — SEMPRE INCLUIR

### Cartório (Desmembramento / Desdobro / Unificação)
> **VALIDADE CARTORÁRIA:** Conforme Art. 18 da Lei Federal 6.766/79, a presente Certidão de Aprovação e suas plantas carimbadas possuem validade **improrrogável de 180 (cento e oitenta) dias** para fins de protocolo e registro no Serviço Registral de Imóveis (SRI), sob pena de caducidade automática do ato administrativo.

### SERO / Receita Federal (Habite-se e Alvarás)
> Averbação Cartorária: Este certificado não exime a obrigatoriedade de aferição da obra no sistema SERO da RFB para emissão da CND, documento indispensável para averbação junto ao Cartório de Registro de Imóveis.

### Condomínio de Lotes (LC 270/2020)
> **ADVERTÊNCIA DE INFRAESTRUTURA:** Conforme Art. 3º, §1º da LC 270/2020, vias e áreas de uso comum constituem propriedade exclusiva dos condôminos, sendo terminantemente vedado o repasse de manutenção ao Poder Público.

---

*Arquivo gerado automaticamente em 21/04/2026 — Sistema GEM SMOSU Oliveira/MG v1.0*
