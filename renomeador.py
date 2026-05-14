#!/usr/bin/env python3
"""Renomeador de arquivos em lote — prefixo, sufixo ou numeração sequencial."""

import argparse
import re
import sys
from pathlib import Path


def listar_arquivos(pasta: Path, extensao: str | None = None) -> list[Path]:
    """Lista arquivos na pasta, opcionalmente filtrando por extensão."""
    if not pasta.is_dir():
        raise NotADirectoryError(f"Pasta não encontrada: {pasta}")

    arquivos = sorted(f for f in pasta.iterdir() if f.is_file())

    if extensao:
        ext = extensao.lower().lstrip(".")
        arquivos = [f for f in arquivos if f.suffix.lower().lstrip(".") == ext]

    return arquivos


def gerar_novos_nomes(
    arquivos: list[Path],
    prefixo: str = "",
    sufixo: str = "",
    numerar: bool = False,
    inicio: int = 1,
    separador: str = "_",
) -> list[tuple[Path, Path]]:
    """Gera pares (arquivo_original, novo_caminho) aplicando as transformações."""
    renomeacoes = []

    for i, arq in enumerate(arquivos):
        stem = arq.stem
        ext = arq.suffix

        if numerar:
            total = len(arquivos) + inicio - 1
            largura = max(len(str(total)), 3)
            numero = str(i + inicio).zfill(largura)
            novo_nome = f"{prefixo}{numero}{separador}{stem}{sufixo}{ext}"
        else:
            novo_nome = f"{prefixo}{stem}{sufixo}{ext}"

        renomeacoes.append((arq, arq.parent / novo_nome))

    return renomeacoes


def renomear_arquivos(
    pasta: Path,
    prefixo: str = "",
    sufixo: str = "",
    numerar: bool = False,
    inicio: int = 1,
    separador: str = "_",
    extensao: str | None = None,
    dry_run: bool = False,
) -> list[tuple[Path, Path]]:
    """
    Renomeia arquivos em lote numa pasta.

    Returns:
        Lista de tuplas (caminho_original, caminho_novo).
    """
    arquivos = listar_arquivos(pasta, extensao)

    if not arquivos:
        return []

    renomeacoes = gerar_novos_nomes(arquivos, prefixo, sufixo, numerar, inicio, separador)

    if not dry_run:
        for original, novo in renomeacoes:
            if original != novo:
                original.rename(novo)

    return renomeacoes


def renomear_com_regex(
    pasta: Path,
    padrao: str,
    substituicao: str,
    extensao: str | None = None,
    dry_run: bool = False,
) -> list[tuple[Path, Path]]:
    """
    Renomeia arquivos aplicando uma expressão regular ao stem (nome sem extensão).

    Returns:
        Lista de tuplas (caminho_original, caminho_novo).
    """
    arquivos = listar_arquivos(pasta, extensao)
    renomeacoes = []

    for arq in arquivos:
        novo_stem = re.sub(padrao, substituicao, arq.stem)
        novo_caminho = arq.parent / (novo_stem + arq.suffix)
        renomeacoes.append((arq, novo_caminho))

    if not dry_run:
        for original, novo in renomeacoes:
            if original != novo:
                original.rename(novo)

    return renomeacoes


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Renomeia arquivos em lote numa pasta.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
exemplos:
  prefixo:                py renomeador.py ./fotos --prefixo "viagem_"
  sufixo:                 py renomeador.py ./fotos --sufixo "_editado"
  numeração sequencial:   py renomeador.py ./fotos --numerar
  prefixo + numeração:    py renomeador.py ./fotos --prefixo "foto_" --numerar --inicio 10
  filtrar por extensão:   py renomeador.py ./fotos --numerar --extensao jpg --dry-run
        """,
    )

    parser.add_argument("pasta", type=Path, help="Pasta com os arquivos a renomear")
    parser.add_argument("--prefixo", default="", metavar="TEXTO", help="Texto a adicionar antes do nome")
    parser.add_argument("--sufixo", default="", metavar="TEXTO", help="Texto a adicionar após o nome (antes da extensão)")
    parser.add_argument("--numerar", action="store_true", help="Adiciona numeração sequencial como prefixo (ex: 001_)")
    parser.add_argument("--inicio", type=int, default=1, metavar="N", help="Número inicial da sequência (padrão: 1)")
    parser.add_argument("--separador", default="_", metavar="SEP", help="Separador entre número e nome (padrão: _)")
    parser.add_argument("--extensao", default=None, metavar="EXT", help="Filtra arquivos por extensão (ex: jpg, pdf)")
    parser.add_argument("--dry-run", action="store_true", help="Simula a renomeação sem alterar arquivos")

    args = parser.parse_args()

    if not args.prefixo and not args.sufixo and not args.numerar:
        parser.error("Informe ao menos uma opção: --prefixo, --sufixo ou --numerar")

    try:
        renomeacoes = renomear_arquivos(
            pasta=args.pasta,
            prefixo=args.prefixo,
            sufixo=args.sufixo,
            numerar=args.numerar,
            inicio=args.inicio,
            separador=args.separador,
            extensao=args.extensao,
            dry_run=args.dry_run,
        )
    except NotADirectoryError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)

    if not renomeacoes:
        print("Nenhum arquivo encontrado.")
        return

    tag = "[SIMULAÇÃO] " if args.dry_run else ""
    alterados = [(o, n) for o, n in renomeacoes if o != n]

    for original, novo in renomeacoes:
        if original == novo:
            print(f"  (sem alteração)  {original.name}")
        else:
            print(f"{tag}{original.name}  ->  {novo.name}")

    print(f"\n{len(alterados)} arquivo(s) {'seriam renomeados' if args.dry_run else 'renomeados'}.")


if __name__ == "__main__":
    main()
