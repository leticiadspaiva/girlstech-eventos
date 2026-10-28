#!/usr/bin/env python3
"""Fiscal do eventos.json: roda no GitHub Actions e também localmente (python3 scripts/validar.py)."""
import json
import sys

from eventos_lib import ARQUIVO, carregar, validar


def main():
    try:
        dados = carregar()
    except json.JSONDecodeError as e:
        msg = (f"eventos.json tem erro de formatação na linha {e.lineno}, coluna {e.colno}: {e.msg}. "
               "Costuma ser uma vírgula faltando/sobrando ou uma aspa sem fechar.")
        print(f"::error file={ARQUIVO.name},line={e.lineno}::{msg}")
        print(f"❌ {msg}")
        return 1

    erros, avisos = validar(dados)
    for a in avisos:
        print(f"::warning file={ARQUIVO.name}::{a}")
        print(f"⚠️  {a}")
    for e in erros:
        print(f"::error file={ARQUIVO.name}::{e}")
        print(f"❌ {e}")

    total = sum(len(v) for v in dados.values() if isinstance(v, list)) if isinstance(dados, dict) else 0
    if erros:
        print(f"\n❌ {len(erros)} erro(s) encontrado(s). Corrija para o site não quebrar.")
        return 1
    print(f"\n✅ Estrutura validada com sucesso! {total} eventos em conformidade.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
