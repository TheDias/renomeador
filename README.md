# renomeador

Script Python para renomeação de arquivos em lote. Adiciona prefixo, sufixo ou numeração sequencial aos nomes dos arquivos, com suporte a filtro por extensão e modo de simulação.

## Instalação

Requer Python 3.10+ e pytest (apenas para os testes).

```bash
git clone https://github.com/TheDias/renomeador.git
cd renomeador
pip install pytest   # opcional, somente para testes
```

Nenhuma outra dependência externa é necessária.

## Como usar

```
py renomeador.py <pasta> [opções]
```

Ao menos uma das opções `--prefixo`, `--sufixo` ou `--numerar` é obrigatória.

### Opções

| Opção | Descrição |
|---|---|
| `--prefixo TEXTO` | Adiciona TEXTO antes do nome do arquivo |
| `--sufixo TEXTO` | Adiciona TEXTO após o nome, antes da extensão |
| `--numerar` | Adiciona número sequencial como prefixo (`001_`, `002_`, …) |
| `--inicio N` | Número inicial da sequência (padrão: `1`) |
| `--separador SEP` | Separador entre número e nome (padrão: `_`) |
| `--extensao EXT` | Filtra arquivos por extensão (ex: `jpg`, `.pdf`) |
| `--dry-run` | Simula a operação sem alterar nenhum arquivo |

---

## Exemplos

### Prefixo

Adiciona um texto fixo antes do nome de todos os arquivos.

```bash
py renomeador.py ./fotos --prefixo "viagem_"
```

```
foto1.jpg  ->  viagem_foto1.jpg
foto2.jpg  ->  viagem_foto2.jpg
```

---

### Sufixo

Adiciona um texto fixo após o nome, mas antes da extensão.

```bash
py renomeador.py ./fotos --sufixo "_editado"
```

```
foto1.jpg  ->  foto1_editado.jpg
foto2.jpg  ->  foto2_editado.jpg
```

---

### Numeração sequencial

Numera os arquivos em ordem alfabética com zero-padding automático.

```bash
py renomeador.py ./fotos --numerar
```

```
foto1.jpg  ->  001_foto1.jpg
foto2.jpg  ->  002_foto2.jpg
```

#### Número inicial customizado

```bash
py renomeador.py ./fotos --numerar --inicio 10
```

```
foto1.jpg  ->  010_foto1.jpg
foto2.jpg  ->  011_foto2.jpg
```

#### Separador customizado

```bash
py renomeador.py ./fotos --numerar --separador "-"
```

```
foto1.jpg  ->  001-foto1.jpg
foto2.jpg  ->  002-foto2.jpg
```

#### Prefixo + numeração

```bash
py renomeador.py ./fotos --prefixo "trip_" --numerar
```

```
foto1.jpg  ->  trip_001_foto1.jpg
foto2.jpg  ->  trip_002_foto2.jpg
```

---

### Filtro por extensão

Renomeia apenas os arquivos com a extensão especificada; os demais não são tocados.

```bash
py renomeador.py ./fotos --prefixo "img_" --extensao jpg
```

```
foto1.jpg      ->  img_foto1.jpg
foto2.jpg      ->  img_foto2.jpg
  (sem alteração)  documento.pdf
```

---

### Modo simulação (`--dry-run`)

Exibe o que seria feito sem alterar nenhum arquivo. Útil para revisar antes de executar.

```bash
py renomeador.py ./fotos --numerar --extensao jpg --dry-run
```

```
[SIMULAÇÃO] foto1.jpg  ->  001_foto1.jpg
[SIMULAÇÃO] foto2.jpg  ->  002_foto2.jpg

2 arquivo(s) seriam renomeados.
```

---

## Testes

```bash
py -m pytest test_renomeador.py -v
```

A suíte cobre listagem de arquivos, geração de nomes (prefixo, sufixo, numeração, separadores, zero-padding) e a função principal com dry-run, filtro por extensão e retorno de tuplas.

## Estrutura

```
renomeador/
├── renomeador.py       # script principal + CLI
├── test_renomeador.py  # testes com pytest
└── README.md
```
