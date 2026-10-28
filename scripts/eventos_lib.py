"""Funções compartilhadas pelo validador (CI) e pelo script de IA.

Usa APENAS a biblioteca padrão do Python, para o validador rodar sem instalar nada.
"""
import difflib
import json
import re
import unicodedata
from datetime import date, datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ARQUIVO = Path(__file__).resolve().parent.parent / "eventos.json"

ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA",
           "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
SECOES = ["ONLINE"] + ESTADOS
CATEGORIAS = ["UNIVERSIDADE", "MULTINACIONAL", "COMUNIDADE", "GRANDE EVENTO", "BIG TECH", "LINKEDIN EVENT"]
CUSTOS = ["Gratuito", "Pago"]
CAMPOS = ["title", "category", "cost", "date", "displayDate", "link"]

MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
ABREV = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


# ---------------------------------------------------------------- leitura / escrita
def carregar(caminho=ARQUIVO):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def formatar(dados):
    """Serializa no mesmo estilo do arquivo atual (um evento por linha) para o diff do PR ficar mínimo."""
    linhas = ["{"]
    secoes = list(dados.keys())
    for i, secao in enumerate(secoes):
        linhas.append(f"  {json.dumps(secao, ensure_ascii=False)}: [")
        eventos = dados[secao]
        for j, ev in enumerate(eventos):
            chaves = [k for k in CAMPOS if k in ev] + [k for k in ev if k not in CAMPOS]
            corpo = ", ".join(
                f"{json.dumps(k, ensure_ascii=False)}: {json.dumps(ev[k], ensure_ascii=False)}" for k in chaves
            )
            virgula = "," if j < len(eventos) - 1 else ""
            linhas.append(f"    {{ {corpo} }}{virgula}")
        linhas.append("  ]" + ("," if i < len(secoes) - 1 else ""))
    linhas.append("}")
    return "\n".join(linhas) + "\n"


def salvar(dados, caminho=ARQUIVO):
    Path(caminho).write_text(formatar(dados), encoding="utf-8")


# ---------------------------------------------------------------- normalização
def normalizar_texto(txt):
    txt = unicodedata.normalize("NFKD", txt or "")
    txt = "".join(c for c in txt if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", " ", txt).strip()


_RASTREIO = ("utm_", "fbclid", "gclid", "mc_", "ref", "trk", "trackingid", "originalsubdomain")


def limpar_link(url):
    """Remove parâmetros de rastreamento (utm_*, fbclid...) e fragmentos."""
    p = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(p.query) if not k.lower().startswith(_RASTREIO)]
    return urlunsplit((p.scheme, p.netloc, p.path, urlencode(query), ""))


def normalizar_link(url):
    p = urlsplit(limpar_link(url))
    host = p.netloc.lower().removeprefix("www.")
    return f"{host}{p.path.rstrip('/')}?{p.query}".rstrip("?")


def montar_display_date(ini, fim=None, precisao="dia"):
    """Gera o displayDate no padrão já usado no calendário."""
    if precisao == "mes":
        return f"{MESES[ini.month - 1]} de {ini.year}"
    if not fim or fim <= ini:
        return f"{ini.day:02d} de {MESES[ini.month - 1]}, {ini.year}"
    if (ini.year, ini.month) == (fim.year, fim.month):
        conector = " e " if fim.day - ini.day == 1 else " a "
        return f"{ini.day:02d}{conector}{fim.day:02d} de {MESES[ini.month - 1]}, {ini.year}"
    if ini.year == fim.year:
        return f"{ini.day:02d} de {ABREV[ini.month - 1]} a {fim.day:02d} de {ABREV[fim.month - 1]}, {ini.year}"
    return (f"{ini.day:02d} de {ABREV[ini.month - 1]}, {ini.year} a "
            f"{fim.day:02d} de {ABREV[fim.month - 1]}, {fim.year}")


# ---------------------------------------------------------------- duplicatas
def achar_duplicata(dados, evento, limiar=0.85):
    """Retorna (secao, evento_existente) se o evento já parece estar cadastrado."""
    titulo = normalizar_texto(evento["title"])
    link = normalizar_link(evento["link"])
    for secao, lista in dados.items():
        for ex in lista:
            if ex.get("date") != evento["date"]:
                # mesmo evento com data corrigida: título praticamente idêntico no mesmo ano
                mesmo_ano = str(ex.get("date", ""))[:4] == evento["date"][:4]
                if not (mesmo_ano and normalizar_texto(ex.get("title")) == titulo):
                    continue
            semelhanca = difflib.SequenceMatcher(None, titulo, normalizar_texto(ex.get("title"))).ratio()
            mesmo_link = normalizar_link(ex.get("link", "")) == link and ex.get("date") == evento["date"]
            if semelhanca >= limiar or mesmo_link:
                return secao, ex
    return None


# ---------------------------------------------------------------- validação
def _data_valida(txt):
    try:
        return datetime.strptime(txt, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def validar(dados):
    """Retorna (erros, avisos). Erros quebram o site; avisos são só qualidade."""
    erros, avisos = [], []
    if not isinstance(dados, dict):
        return ["O arquivo deve começar com { } contendo uma lista de eventos por estado."], avisos

    vistos = {}
    for secao, lista in dados.items():
        if secao not in SECOES:
            avisos.append(f'Seção "{secao}" não é "ONLINE" nem uma sigla de estado (UF) válida.')
        if not isinstance(lista, list):
            erros.append(f'Seção "{secao}": deve ser uma lista [ ... ] de eventos.')
            continue
        for i, ev in enumerate(lista, start=1):
            onde = f'{secao} #{i}' + (f' ("{ev.get("title")}")' if isinstance(ev, dict) and ev.get("title") else "")
            if not isinstance(ev, dict):
                erros.append(f"{onde}: cada evento deve ser um bloco {{ ... }}.")
                continue
            for campo in CAMPOS:
                valor = ev.get(campo)
                if not isinstance(valor, str) or not valor.strip():
                    erros.append(f'{onde}: campo "{campo}" ausente ou vazio.')
            if ev.get("cost") and ev["cost"] not in CUSTOS:
                erros.append(f'{onde}: "cost" deve ser exatamente "Gratuito" ou "Pago" (veio "{ev.get("cost")}").')
            if ev.get("date") and _data_valida(ev["date"]) is None:
                erros.append(f'{onde}: "date" deve ser uma data real no formato AAAA-MM-DD (veio "{ev["date"]}").')
            link = ev.get("link")
            if isinstance(link, str) and link:
                p = urlsplit(link)
                if p.scheme not in ("http", "https") or not p.netloc:
                    erros.append(f'{onde}: "link" deve ser uma URL completa começando com https:// (veio "{link}").')
            if ev.get("category") and ev["category"] not in CATEGORIAS:
                avisos.append(f'{onde}: categoria "{ev["category"]}" fora da lista usual ({", ".join(CATEGORIAS)}).')
            chave = (normalizar_texto(ev.get("title")), ev.get("date"))
            if chave in vistos:
                avisos.append(f"{onde}: possível duplicata de {vistos[chave]}.")
            else:
                vistos[chave] = onde
    return erros, avisos
