"""
prompt — lee y escribe prompt.toml. Copiá prompt.py + prompt.toml a tu proyecto.

Uso:
    import prompt

    cfg = prompt.leer()
    cfg["clave"] = "valor"
    prompt.escribir(cfg)
"""

import tomllib
from datetime import date, datetime, time
from pathlib import Path

ARCHIVO = Path("prompt.toml")


def leer(ruta: str | Path = ARCHIVO) -> dict:
    """prompt.toml → dict."""
    with open(ruta, "rb") as f:
        return tomllib.load(f)


def escribir(datos: dict, ruta: str | Path = ARCHIVO) -> None:
    """Dict → prompt.toml."""
    Path(ruta).write_text(_serializar(datos), encoding="utf-8")


def _serializar(v: object, prefijo: str = "") -> str:
    if isinstance(v, dict):
        return _dict(v, prefijo)
    if isinstance(v, list):
        return f"[{', '.join(_valor(e) for e in v)}]"
    return _valor(v)


def _dict(d: dict, prefijo: str = "") -> str:
    partes: list[str] = []
    tablas: list[tuple[str, dict]] = []
    tablas_array: list[tuple[str, list[dict]]] = []

    for k, v in d.items():
        clave = f"{prefijo}.{k}" if prefijo else k
        if isinstance(v, list) and v and all(isinstance(e, dict) for e in v):
            tablas_array.append((clave, v))
        elif isinstance(v, dict) and (not prefijo or not _es_inline(v)):
            tablas.append((clave, v))
        else:
            partes.append(f"{k} = {_valor(v)}")

    texto = "\n".join(partes)

    for nombre, contenido in tablas:
        texto += f"\n\n[{nombre}]\n{_dict(contenido, nombre)}"

    for nombre, elementos in tablas_array:
        for elem in elementos:
            texto += f"\n\n[[{nombre}]]\n{_dict(elem, nombre)}"

    return texto.strip()


def _es_inline(d: dict) -> bool:
    return len(d) <= 3 and not any(isinstance(v, dict) for v in d.values())


def _valor(v: object) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return _cadena(v)
    if isinstance(v, (datetime, date, time)):
        return v.isoformat()
    if isinstance(v, list):
        return f"[{', '.join(_valor(e) for e in v)}]"
    if isinstance(v, dict):
        pares = [f"{k} = {_valor(v)}" for k, v in v.items()]
        return f"{{ {', '.join(pares)} }}"
    if v is None:
        return '""'
    raise TypeError(f"prompt: tipo no soportado {type(v).__name__}")


def _cadena(s: str) -> str:
    if "\n" in s:
        escapada = s.replace(chr(92), chr(92) + chr(92))
        return f'"""{escapada}"""'
    if "'" not in s:
        return f"'{s}'"
    escapada = s.replace(chr(92), chr(92) + chr(92)).replace(chr(34), chr(92) + chr(34))
    return f'"{escapada}"'
