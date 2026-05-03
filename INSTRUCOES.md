# 🏛️ Projeto Pareceres GEM — SMOSU Oliveira/MG

Sistema de Inteligência Artificial para automação de pareceres técnicos e gestão documental da Secretaria Municipal de Obras e Serviços Urbanos.

---

## 🚀 Como Usar (Guia Rápido)

1. **Iniciar o Sistema:**
   Dê um duplo clique no arquivo `GERAR_DOCUMENTOS.bat` na raiz do projeto. Isso abrirá o Painel de Controle.

2. **Fluxo de Trabalho:**
   - **Modelos:** Se precisar de um ponto de partida, copie um arquivo da pasta `Modelos/` para a pasta `Entrada/`.
   - **Edição:** Renomeie o arquivo na pasta `Entrada/` (ex: `processo_1234_2026.json`) e preencha os dados necessários.
   - **Geração:** Através do Painel (que abre no navegador), você pode validar e compilar os documentos.
   - **Resultado:** Os documentos finais (`.docx` e `.pdf`) serão salvos automaticamente na pasta `Saida/`.

---

## 📂 Organização de Pastas

Para manter a simplicidade, você só precisa interagir com estas três pastas:

- 📥 **`Entrada/`**: Coloque aqui os arquivos JSON dos processos que deseja gerar.
- 📤 **`Saida/`**: Onde os documentos prontos e assinados aparecerão.
- 📋 **`Modelos/`**: Modelos de referência para cada tipo de parecer ou alvará.

> **Dica:** O sistema técnico, códigos e inteligência estão organizados dentro da pasta `Sistema/`. Não é necessário mexer neles para o uso diário.

---

## ⚖️ Base Legal
O sistema aplica automaticamente regras da **Lei 1.544/86** (Código de Obras), **LC 267/2019** (Uso e Ocupação do Solo) e o **Decreto 4.149/2019**.

---

## 👨‍💻 Suporte Técnico
Documentação técnica detalhada, logs de treinamento de IA e guias de troubleshooting podem ser encontrados em `Sistema/docs/`.

---
**Engenheiro Responsável:** Diego Tarcísio Nunes Vilela  
**Prefeitura Municipal de Oliveira/MG**
