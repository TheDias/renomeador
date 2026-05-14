# renomeador

[![Tests](https://github.com/TheDias/renomeador/actions/workflows/tests.yml/badge.svg)](https://github.com/TheDias/renomeador/actions/workflows/tests.yml)

Script Python para renomeação de arquivos em lote. Adiciona prefixo, sufixo ou numeração sequencial aos nomes dos arquivos, com suporte a filtro por extensão e modo de simulação.

## Instalação

Requer Python 3.10+. Nenhuma dependência externa além do `pytest` (opcional, apenas para testes).

**Windows**

```bash
git clone https://github.com/TheDias/renomeador.git
cd renomeador
py -m venv venv
.\venv\Scripts\activate
pip install pytest   # opcional, somente para testes
```

**Linux / Mac**

```bash
git clone https://github.com/TheDias/renomeador.git
cd renomeador
python3 -m venv venv
source venv/bin/activate
pip install pytest   # opcional, somente para testes
```

## Uso como biblioteca

Além da CLI, as funções podem ser importadas diretamente em outros scripts Python.

```python
from renomeador import renomear_arquivos

# Adiciona prefixo "backup_" a todos os .txt em ./documentos (sem alterar nada)
pares = renomear_arquivos(
    pasta="./documentos",
    prefixo="backup_",
    extensao="txt",
    dry_run=True,
)

for original, novo in pares:
    print(f"{original.name}  ->  {novo.name}")
```

`renomear_arquivos()` retorna uma lista de tuplas `(Path original, Path novo)` tanto em modo normal quanto em `dry_run`. Em modo normal os arquivos são renomeados no disco; em `dry_run` apenas a lista é retornada.

---

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

## Como rodar os testes

```bash
py -m pytest test_renomeador.py -v
```

Saída esperada (todos passando):

```
test_renomeador.py::test_listar_arquivos PASSED
test_renomeador.py::test_listar_com_filtro_extensao PASSED
test_renomeador.py::test_gerar_nomes_prefixo PASSED
test_renomeador.py::test_gerar_nomes_sufixo PASSED
test_renomeador.py::test_gerar_nomes_numeracao PASSED
test_renomeador.py::test_gerar_nomes_zero_padding PASSED
test_renomeador.py::test_gerar_nomes_separador_customizado PASSED
test_renomeador.py::test_renomear_dry_run PASSED
...
```

**Interpretando a saída:**

| Resultado | Significado |
|---|---|
| `PASSED` | Teste passou — comportamento correto |
| `FAILED` | Asserção falhou — saída real diverge do esperado |
| `ERROR` | Exceção inesperada antes da asserção — bug ou setup errado |

A suíte cobre listagem de arquivos, geração de nomes (prefixo, sufixo, numeração, separadores, zero-padding) e a função principal com dry-run, filtro por extensão e retorno de tuplas.

## Estrutura do projeto

```
renomeador/
├── renomeador.py       # lógica principal + entry point da CLI
├── test_renomeador.py  # suíte de testes com pytest
└── README.md           # documentação
```

- **`renomeador.py`** — contém três funções públicas (`listar_arquivos`, `gerar_novos_nomes`, `renomear_arquivos`) e o bloco `if __name__ == "__main__"` que expõe a CLI via `argparse`. Pode ser importado como módulo sem efeitos colaterais.
- **`test_renomeador.py`** — testes unitários e de integração usando `pytest` + `tmp_path`. Cada função pública tem cobertura isolada; `renomear_arquivos` é testado com arquivos reais em diretório temporário.
- **`README.md`** — documentação de uso, exemplos e referência das opções.

---

## Contribuindo

1. Faça um fork do repositório e clone localmente.
2. Crie uma branch descritiva a partir de `master`:

```bash
git checkout -b feat/minha-funcionalidade
# ou
git checkout -b fix/correcao-de-bug
# ou
git checkout -b docs/melhora-readme
```

3. Faça as alterações e rode os testes antes de commitar:

```bash
py -m pytest test_renomeador.py -v
```

4. Abra um Pull Request para `master` com uma descrição clara do que foi alterado e por quê.

**Convenção de branches:** use o prefixo `feat/` para novas funcionalidades, `fix/` para correções e `docs/` para documentação.
