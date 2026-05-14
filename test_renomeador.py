import pytest
from pathlib import Path

from renomeador import gerar_novos_nomes, listar_arquivos, renomear_arquivos, renomear_com_regex


@pytest.fixture
def pasta(tmp_path):
    """Pasta com arquivos variados para os testes."""
    for nome in ["foto1.jpg", "foto2.jpg", "documento.pdf", "nota.txt"]:
        (tmp_path / nome).touch()
    return tmp_path


# --- listar_arquivos ---


def test_listar_todos_os_arquivos(pasta):
    assert len(listar_arquivos(pasta)) == 4


def test_listar_filtra_por_extensao(pasta):
    jpgs = listar_arquivos(pasta, extensao="jpg")
    assert len(jpgs) == 2
    assert all(f.suffix == ".jpg" for f in jpgs)


def test_listar_extensao_case_insensitive(pasta):
    (pasta / "IMAGEM.JPG").touch()
    jpgs = listar_arquivos(pasta, extensao="jpg")
    assert len(jpgs) == 3


def test_listar_extensao_com_ponto(pasta):
    result = listar_arquivos(pasta, extensao=".jpg")
    assert len(result) == 2


def test_listar_pasta_inexistente(tmp_path):
    with pytest.raises(NotADirectoryError):
        listar_arquivos(tmp_path / "nao_existe")


def test_listar_pasta_vazia(tmp_path):
    assert listar_arquivos(tmp_path) == []


# --- gerar_novos_nomes ---


def test_prefixo():
    arquivos = [Path("/p/foto.jpg"), Path("/p/doc.pdf")]
    resultado = gerar_novos_nomes(arquivos, prefixo="viagem_")
    assert resultado[0][1].name == "viagem_foto.jpg"
    assert resultado[1][1].name == "viagem_doc.pdf"


def test_sufixo():
    arquivos = [Path("/p/foto.jpg")]
    resultado = gerar_novos_nomes(arquivos, sufixo="_editada")
    assert resultado[0][1].name == "foto_editada.jpg"


def test_prefixo_e_sufixo():
    arquivos = [Path("/p/img.png")]
    resultado = gerar_novos_nomes(arquivos, prefixo="novo_", sufixo="_v2")
    assert resultado[0][1].name == "novo_img_v2.png"


def test_numeracao_sequencial():
    arquivos = [Path(f"/p/{c}.jpg") for c in "abc"]
    resultado = gerar_novos_nomes(arquivos, numerar=True)
    assert resultado[0][1].name == "001_a.jpg"
    assert resultado[1][1].name == "002_b.jpg"
    assert resultado[2][1].name == "003_c.jpg"


def test_numeracao_inicio_customizado():
    arquivos = [Path("/p/a.jpg"), Path("/p/b.jpg")]
    resultado = gerar_novos_nomes(arquivos, numerar=True, inicio=10)
    assert resultado[0][1].name == "010_a.jpg"
    assert resultado[1][1].name == "011_b.jpg"


def test_numeracao_separador_customizado():
    arquivos = [Path("/p/foto.jpg")]
    resultado = gerar_novos_nomes(arquivos, numerar=True, separador="-")
    assert resultado[0][1].name == "001-foto.jpg"


def test_numeracao_com_prefixo():
    arquivos = [Path("/p/foto.jpg")]
    resultado = gerar_novos_nomes(arquivos, prefixo="trip_", numerar=True)
    assert resultado[0][1].name == "trip_001_foto.jpg"


def test_numeracao_zero_padding_adaptativo():
    # com 10+ arquivos, a largura mínima deve acompanhar
    arquivos = [Path(f"/p/f{i}.jpg") for i in range(12)]
    resultado = gerar_novos_nomes(arquivos, numerar=True)
    assert resultado[0][1].name == "001_f0.jpg"
    assert resultado[11][1].name == "012_f11.jpg"


def test_sem_transformacao_retorna_mesmo_nome():
    arquivos = [Path("/p/foto.jpg")]
    resultado = gerar_novos_nomes(arquivos)
    assert resultado[0][0] == resultado[0][1]


# --- renomear_arquivos ---


def test_renomear_aplica_prefixo(pasta):
    renomear_arquivos(pasta, prefixo="novo_")
    nomes = {f.name for f in pasta.iterdir() if f.is_file()}
    assert "novo_foto1.jpg" in nomes
    assert "novo_documento.pdf" in nomes


def test_renomear_aplica_sufixo(pasta):
    renomear_arquivos(pasta, sufixo="_bkp")
    nomes = {f.name for f in pasta.iterdir() if f.is_file()}
    assert "foto1_bkp.jpg" in nomes
    assert "nota_bkp.txt" in nomes


def test_renomear_numeracao(pasta):
    renomear_arquivos(pasta, numerar=True)
    nomes = {f.name for f in pasta.iterdir() if f.is_file()}
    assert any(n[:3].isdigit() for n in nomes)


def test_dry_run_nao_altera_arquivos(pasta):
    nomes_antes = {f.name for f in pasta.iterdir() if f.is_file()}
    renomear_arquivos(pasta, prefixo="x_", dry_run=True)
    nomes_depois = {f.name for f in pasta.iterdir() if f.is_file()}
    assert nomes_antes == nomes_depois


def test_dry_run_retorna_renomeacoes(pasta):
    resultado = renomear_arquivos(pasta, prefixo="x_", dry_run=True)
    assert len(resultado) == 4
    assert all(n.name.startswith("x_") for _, n in resultado)


def test_filtro_extensao_nao_altera_outros(pasta):
    renomear_arquivos(pasta, prefixo="img_", extensao="jpg")
    nomes = {f.name for f in pasta.iterdir() if f.is_file()}
    assert "img_foto1.jpg" in nomes
    assert "img_foto2.jpg" in nomes
    assert "documento.pdf" in nomes
    assert "nota.txt" in nomes


def test_pasta_vazia_retorna_lista_vazia(tmp_path):
    assert renomear_arquivos(tmp_path, prefixo="x_") == []


def test_retorno_e_lista_de_tuplas(pasta):
    resultado = renomear_arquivos(pasta, prefixo="p_")
    assert isinstance(resultado, list)
    assert all(isinstance(par, tuple) and len(par) == 2 for par in resultado)
    assert all(isinstance(par[0], Path) and isinstance(par[1], Path) for par in resultado)


# --- renomear_com_regex ---


def test_regex_match_simples(pasta):
    # "foto" → "imagem" no stem de foto1.jpg e foto2.jpg
    renomear_com_regex(pasta, padrao=r"foto", substituicao="imagem")
    nomes = {f.name for f in pasta.iterdir() if f.is_file()}
    assert "imagem1.jpg" in nomes
    assert "imagem2.jpg" in nomes
    assert "documento.pdf" in nomes  # sem match, inalterado


def test_regex_captura_grupos(pasta):
    # captura o número e reposiciona: "foto1" → "img_1"
    renomear_com_regex(pasta, padrao=r"foto(\d+)", substituicao=r"img_\1")
    nomes = {f.name for f in pasta.iterdir() if f.is_file()}
    assert "img_1.jpg" in nomes
    assert "img_2.jpg" in nomes


def test_regex_sem_match_nao_renomeia(pasta):
    nomes_antes = {f.name for f in pasta.iterdir() if f.is_file()}
    resultado = renomear_com_regex(pasta, padrao=r"xyz_nao_existe", substituicao="qualquer")
    nomes_depois = {f.name for f in pasta.iterdir() if f.is_file()}
    assert nomes_antes == nomes_depois
    assert all(original == novo for original, novo in resultado)
