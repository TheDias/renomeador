# renomeador

Script Python para renomeação de arquivos em lote. Suporta prefixo, sufixo e numeração sequencial, com filtro por extensão e modo simulação.

## Comandos

```bash
py renomeador.py <pasta> [opções]   # roda o script
py -m pytest test_renomeador.py -v  # executa os testes
```

## Opções da CLI

| Opção | Descrição |
|---|---|
| `--prefixo TEXTO` | Adiciona TEXTO antes do nome do arquivo |
| `--sufixo TEXTO` | Adiciona TEXTO após o nome, antes da extensão |
| `--numerar` | Adiciona número sequencial como prefixo (`001_`, `002_`, …) |
| `--inicio N` | Número inicial da sequência (padrão: 1) |
| `--separador SEP` | Separador entre número e nome (padrão: `_`) |
| `--extensao EXT` | Filtra arquivos por extensão (ex: `jpg`, `.pdf`) |
| `--dry-run` | Simula sem alterar arquivos — mostra o que seria feito |

Ao menos uma de `--prefixo`, `--sufixo` ou `--numerar` é obrigatória.

## Exemplos

```bash
# Adicionar prefixo a todos os arquivos
py renomeador.py ./fotos --prefixo "viagem_"

# Adicionar sufixo antes da extensão
py renomeador.py ./fotos --sufixo "_editado"

# Numeração sequencial (001_, 002_, …)
py renomeador.py ./fotos --numerar

# Prefixo + numeração a partir de 10
py renomeador.py ./fotos --prefixo "foto_" --numerar --inicio 10

# Separador diferente
py renomeador.py ./fotos --numerar --separador "-"

# Apenas arquivos .jpg, sem alterar nada (simulação)
py renomeador.py ./fotos --numerar --extensao jpg --dry-run
```

## Estrutura

```
renomeador/
├── renomeador.py       # script principal + CLI
├── test_renomeador.py  # testes com pytest
└── CLAUDE.md           # este arquivo
```

## Funções principais (`renomeador.py`)

- `listar_arquivos(pasta, extensao)` — retorna arquivos da pasta, com filtro opcional por extensão
- `gerar_novos_nomes(arquivos, prefixo, sufixo, numerar, inicio, separador)` — retorna lista de tuplas `(original, novo_caminho)` sem tocar no disco
- `renomear_arquivos(pasta, ...)` — orquestra listagem + geração + renomeação; aceita `dry_run=True` para simulação

A separação entre `gerar_novos_nomes` (pura, sem I/O) e `renomear_arquivos` facilita testes.
