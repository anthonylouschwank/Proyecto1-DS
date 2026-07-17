# Proyecto 1 — Obtención y Limpieza de Datos (CC3066)

Scraping y limpieza de establecimientos educativos de Guatemala desde
[BUSCAESTABLECIMIENTO_GE (MINEDUC)](http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/).

## Instalación

Requiere Python 3.10+.

```bash
pip install playwright beautifulsoup4 requests pandas tabulate
python -m playwright install chromium
```

- `playwright` (+ `chromium`) es obligatorio para el scraping real: el sitio
  esta detras de Incapsula y bloquea peticiones `requests` crudas, solo
  funciona con un navegador real.
- `tabulate` es necesario para que `pandas.to_markdown()` funcione en el
  script de diagnóstico.

## Orden de ejecución

Los scripts están numerados y se corren en orden desde la raíz del repo:

| Script | Qué hace |
|---|---|
| `00_discover_form.py` | Reconocimiento del formulario (GET simple, sin scraping real). Solo para inspección manual. |
| `01_test_search.py` | Prueba de postback con `requests` (queda documentado que falla por Incapsula). |
| `02_explore_playwright.py` | Prueba de un departamento con Playwright, para confirmar que el cascade Departamento→Municipio funciona en navegador real. |
| `03_scrape_all.py` | **Scraper real.** Recorre los 23 valores del dropdown de departamento (22 departamentos + Ciudad Capital) y guarda un CSV crudo por cada uno en `data/crudo/`. Tarda varios minutos. |
| `04_diagnostico.py` | Une los 23 CSV crudos, calcula el diagnóstico del estado de los datos (registros, tipos, faltantes, únicos, duplicados, fuera de dominio, formatos, problemas de calidad) e imprime el resultado en `reports/diagnostico_datos_crudos.md`. No modifica los datos. |

Para correr todo desde cero:

```bash
python 03_scrape_all.py
python 04_diagnostico.py
```

(`00`–`02` son scripts de exploración ya validados, no hace falta
volver a correrlos salvo que el sitio cambie de estructura.)

## Estructura de carpetas

```
data/crudo/        23 CSV crudos, uno por departamento (generados por 03, no versionados en git)
reports/            Diagnóstico y plan de limpieza (markdown, versionados en git)
```

`data/` está en `.gitignore` porque los CSV crudos se regeneran corriendo
`03_scrape_all.py`; no se versionan.

## Documentos de análisis

- [`reports/diagnostico_datos_crudos.md`](reports/diagnostico_datos_crudos.md) — diagnóstico del estado inicial de los datos crudos.
- [`reports/plan_limpieza.md`](reports/plan_limpieza.md) — plan de limpieza variable por variable (problemas, reglas, justificación, riesgos).
