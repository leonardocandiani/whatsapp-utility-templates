#!/usr/bin/env python3
"""Fail-closed: só deixa passar template vivo, aprovado, categoria UTILITY.

Uso:
    export META_TOKEN="..."
    export META_WABA="<id numérico da sua WABA>"
    python3 preflight.py <nome_do_template> [--lang pt_BR] [--fresh]
    python3 preflight.py --all [--fresh]

Contrato descrito em `references/send-preflight.md`: consulta a
categoria VIVA na Meta antes de qualquer envio, nunca confia em "aprovou
uma vez". Cache de 1 hora em `~/.cache/whatsapp-utility-templates/<waba>/`,
`--fresh` força consulta nova. Erro de rede ou HTTP nunca deixa passar por
precaução: bloqueia, sempre. Exit 0 só com APPROVED + UTILITY vindo da
consulta (cache ou live); qualquer outra coisa é exit 1. `--all` varre a
WABA inteira e mostra quem foi reclassificado desde a última varredura,
comparando com o cache anterior de cada nome.

O token nunca é impresso, em nenhuma saída, log ou erro.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

GRAPH_VERSAO = "v21.0"
CAMPOS = "name,language,status,category,previous_category,quality_score"
TTL_SEGUNDOS = 3600
USO = "uso: python3 preflight.py <nome> [--lang pt_BR] [--fresh] | --all [--fresh] | --help"
ERROS_DE_REDE = (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError)


def pasta_cache(waba: str) -> str:
    base = os.path.expanduser(os.path.join("~", ".cache", "whatsapp-utility-templates", waba))
    os.makedirs(base, exist_ok=True)
    return base


def caminho_cache(waba: str, nome: str) -> str:
    seguro = "".join(c if c.isalnum() or c in "_-." else "_" for c in nome)
    return os.path.join(pasta_cache(waba), f"{seguro}.json")


def ler_cache(waba: str, nome: str) -> dict | None:
    caminho = caminho_cache(waba, nome)
    if not os.path.exists(caminho):
        return None
    with open(caminho, encoding="utf-8") as f:
        registro = json.load(f)
    registro["_idade_segundos"] = time.time() - registro.get("consultado_em_epoch", 0)
    return registro


def gravar_cache(waba: str, nome: str, item: dict) -> None:
    registro = dict(item)
    registro["consultado_em_epoch"] = time.time()
    with open(caminho_cache(waba, nome), "w", encoding="utf-8") as f:
        json.dump(registro, f, ensure_ascii=False, indent=2)


def _requisitar(url: str, token: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def consultar_template(waba: str, token: str, nome: str, idioma: str) -> dict | None:
    """Devolve o item vivo, ou None se não existe template com esse nome e
    idioma. Lança em qualquer falha de rede/HTTP; o chamador decide bloquear."""
    query = urllib.parse.urlencode({"name": nome, "fields": CAMPOS, "limit": "100"})
    url = f"https://graph.facebook.com/{GRAPH_VERSAO}/{waba}/message_templates?{query}"
    corpo = _requisitar(url, token)
    itens = [i for i in corpo.get("data", []) if i.get("name") == nome and i.get("language") == idioma]
    return itens[0] if len(itens) == 1 else None


def consultar_waba_inteira(waba: str, token: str) -> list[dict]:
    query = urllib.parse.urlencode({"fields": CAMPOS, "limit": "500"})
    url = f"https://graph.facebook.com/{GRAPH_VERSAO}/{waba}/message_templates?{query}"
    return _requisitar(url, token).get("data", [])


def decisao(item: dict) -> tuple[bool, str]:
    status, categoria, anterior = item.get("status"), item.get("category"), item.get("previous_category")
    if status == "APPROVED" and categoria == "UTILITY":
        return True, ""
    motivo = f"status={status} category={categoria}"
    if anterior and anterior != categoria:
        motivo += f" (reclassificado de {anterior} para {categoria})"
    return False, motivo


def rodar_um(waba: str, token: str, nome: str, idioma: str, fresh: bool) -> int:
    cache = None if fresh else ler_cache(waba, nome)
    if cache is not None and cache["_idade_segundos"] < TTL_SEGUNDOS:
        item, origem = cache, "cache"
    else:
        try:
            item = consultar_template(waba, token, nome, idioma)
        except ERROS_DE_REDE:
            print(f"blocked: {nome} network-error - network error, refusing to send")
            return 1
        if item is None:
            print(f"blocked: {nome} not-found - nenhum template com esse nome e idioma nesta WABA")
            return 1
        gravar_cache(waba, nome, item)
        origem = "live"

    ok, motivo = decisao(item)
    if ok:
        print(f"ok: {nome} APPROVED UTILITY ({origem})")
        return 0
    print(f"blocked: {nome} {motivo}")
    return 1


def _linha_da_varredura(waba: str, item: dict, fresh: bool) -> tuple[tuple[str, str, str, str], bool, bool]:
    nome = item.get("name", "?")
    antes = None if fresh else ler_cache(waba, nome)
    categoria_antes = antes.get("category") if antes else None
    gravar_cache(waba, nome, item)
    ok, _ = decisao(item)
    mudou = categoria_antes is not None and categoria_antes != item.get("category")
    marca = f"{categoria_antes}->{item.get('category')}" if mudou else "não"
    linha = (nome, str(item.get("status")), str(item.get("category")), marca)
    return linha, not ok, mudou


def rodar_todos(waba: str, token: str, fresh: bool) -> int:
    try:
        itens = consultar_waba_inteira(waba, token)
    except ERROS_DE_REDE:
        print("blocked: --all network-error - network error, refusing to scan")
        return 1

    resultados = [_linha_da_varredura(waba, item, fresh) for item in itens]
    linhas = [r[0] for r in resultados]
    bloqueados = sum(1 for r in resultados if r[1])
    reclassificados = sum(1 for r in resultados if r[2])

    largura = max((len(l[0]) for l in linhas), default=4)
    for nome, status, categoria, marca in linhas:
        print(f"{nome.ljust(largura)}  {status.ljust(10)}  {categoria.ljust(10)}  reclassificado={marca}")
    print(f"\n{len(linhas)} templates | {len(linhas) - bloqueados} ok | {bloqueados} bloqueados | {reclassificados} reclassificados desde a ultima varredura")
    return 0


def _ler_credenciais() -> tuple[str, str]:
    token = os.environ.get("META_TOKEN")
    waba = os.environ.get("META_WABA")
    if not token:
        print("erro: variável de ambiente META_TOKEN não definida", file=sys.stderr)
        print(USO, file=sys.stderr)
        sys.exit(2)
    if not waba or not waba.isdigit():
        print("erro: variável de ambiente META_WABA ausente ou não numérica", file=sys.stderr)
        print(USO, file=sys.stderr)
        sys.exit(2)
    return token, waba


def _parsear_alvo(args: list[str]) -> tuple[str, str]:
    """Devolve (nome_ou_ALL, idioma). Sai com uso em stderr se o formato é inválido."""
    if args == ["--all"]:
        return "--all", ""
    idioma = "pt_BR"
    resto = list(args)
    if len(resto) >= 3 and resto[1] == "--lang":
        idioma = resto[2]
        resto = resto[:1]
    if len(resto) != 1 or resto[0].startswith("-"):
        print(USO, file=sys.stderr)
        sys.exit(2)
    return resto[0], idioma


def main() -> None:
    args = sys.argv[1:]
    if args in (["--help"], ["-h"]):
        print(USO)
        sys.exit(0)

    fresh = "--fresh" in args
    args = [a for a in args if a != "--fresh"]

    alvo, idioma = _parsear_alvo(args)
    token, waba = _ler_credenciais()

    if alvo == "--all":
        sys.exit(rodar_todos(waba, token, fresh))
    sys.exit(rodar_um(waba, token, alvo, idioma, fresh))


if __name__ == "__main__":
    main()
