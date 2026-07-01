# prompt-module

Librería mínima para leer y escribir archivos TOML de configuración de prompts. Copiá `prompt.py` + `prompt.toml` a tu proyecto, sin dependencias externas — solo stdlib.

## prompt.py

Dos funciones:

```python
import prompt

cfg = prompt.leer()           # prompt.toml → dict
cfg["nueva_clave"] = "valor"
prompt.escribir(cfg)          # dict → prompt.toml
```

Soporta strings, números, booleanos, listas, diccionarios anidados, tablas `[seccion]` y arrays de tablas `[[items]]`. Serializa fechas, datetime e inline tables.

## prompt.toml

Ejemplo de configuración para un analizador de IoC (Indicator of Compromise). Define:

- **system.prompt**: instrucción para un LLM que actúa como analista de inteligencia de amenazas
- **approach[]**: pasos de análisis (tipo de IoC, patrones de IP/dominio/hash/URL, correlación con campañas)
- **rules[]**: reglas de puntuación (0-100), niveles de confianza, y formato de respuesta
- **output**: esquema JSON de salida: `{malicioso, puntuacion, confidence, detalles}`

## Instalación

```bash
cp prompt.py prompt.toml tu-proyecto/
```

Nada que instalar. Solo usa `tomllib` (Python ≥ 3.11).

## Licencia

MIT
