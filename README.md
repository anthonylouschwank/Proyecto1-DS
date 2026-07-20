# Proyecto 1 — Obtención y Limpieza de Datos (CC3066)

Scraping y limpieza de establecimientos educativos de Guatemala desde
[BUSCAESTABLECIMIENTO_GE (MINEDUC)](http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/).

## Instalación

Requiere Python 3.10+. Todo el trabajo se hace dentro de un entorno virtual
(`.venv`) para no ensuciar el Python global.

```bash
python -m venv .venv

# activar el entorno
.venv\Scripts\activate        # Windows (cmd / PowerShell)
source .venv/bin/activate     # Git Bash / Linux / Mac

pip install --upgrade pip
pip install playwright beautifulsoup4 requests pandas tabulate notebook ipykernel reportlab
python -m playwright install chromium

# registrar el entorno como kernel de Jupyter
python -m ipykernel install --user --name proyecto1-ds --display-name "Python (Proyecto1-DS)"
```

- `playwright` (+ `chromium`) es obligatorio para el scraping real: el sitio
  esta detras de Incapsula y bloquea peticiones `requests` crudas, solo
  funciona con un navegador real.
- `tabulate` es necesario para que `pandas.to_markdown()` funcione en el
  script de diagnóstico.
- `notebook` + `ipykernel` son necesarios para abrir/correr `05_limpieza.ipynb`.
- `reportlab` es necesario para generar el libro de códigos en PDF
  (`06_libro_codigos.py`).
- Sin activar el venv, se puede invocar todo con la ruta directa al
  ejecutable: `.venv\Scripts\python.exe archivo.py` (Windows) o
  `.venv/bin/python archivo.py` (Linux/Mac).

## Orden de ejecución

Los scripts/notebooks están numerados y se corren en orden desde la raíz del repo:

| Archivo | Qué hace |
|---|---|
| `00_discover_form.py` | Reconocimiento del formulario (GET simple, sin scraping real). Solo para inspección manual. |
| `01_test_search.py` | Prueba de postback con `requests` (queda documentado que falla por Incapsula). |
| `02_explore_playwright.py` | Prueba de un departamento con Playwright, para confirmar que el cascade Departamento→Municipio funciona en navegador real. |
| `03_scrape_all.py` | **Scraper real.** Recorre los 23 valores del dropdown de departamento (22 departamentos + Ciudad Capital) y guarda un CSV crudo por cada uno en `data/crudo/`. Tarda varios minutos. |
| `04_diagnostico.py` | Une los 23 CSV crudos, calcula el diagnóstico del estado de los datos (registros, tipos, faltantes, únicos, duplicados, fuera de dominio, formatos, problemas de calidad) e imprime el resultado en `reports/diagnostico_datos_crudos.md`. No modifica los datos. |
| `05_limpieza.ipynb` | **Notebook de limpieza.** Aplica cada regla de `reports/plan_limpieza.md` (con su justificación y riesgos documentados en celdas markdown), une los 23 departamentos y exporta el dataset final a `data/limpio/establecimientos_educativos_limpio.csv`. |
| `06_libro_codigos.py` | Lee el CSV limpio y genera `reports/libro_codigos.pdf`: descripción general del dataset + descripción, tipo, % de faltantes, valores únicos y tabla de frecuencias por cada variable. |

Para correr todo desde cero (con el venv activado):

```bash
python 03_scrape_all.py
python 04_diagnostico.py
jupyter notebook 05_limpieza.ipynb   # abrir y correr todas las celdas
python 06_libro_codigos.py
```

También se puede ejecutar el notebook completo sin abrir la interfaz:

```bash
jupyter nbconvert --to notebook --execute --inplace 05_limpieza.ipynb
```

(`00`–`02` son scripts de exploración ya validados, no hace falta
volver a correrlos salvo que el sitio cambie de estructura.)

## Estructura de carpetas

```
data/crudo/        23 CSV crudos, uno por departamento (generados por 03, no versionados en git)
data/limpio/        CSV final limpio y unido (generado por 05, no versionado en git)
reports/            Diagnóstico y plan de limpieza (markdown, versionados en git)
```

`data/` y `.venv/` están en `.gitignore`: los CSV se regeneran corriendo los
scripts/notebook, y el entorno virtual se recrea con los comandos de
instalación de arriba.

## Documentos de análisis

- [`reports/diagnostico_datos_crudos.md`](reports/diagnostico_datos_crudos.md) — diagnóstico del estado inicial de los datos crudos.
- [`reports/plan_limpieza.md`](reports/plan_limpieza.md) — plan de limpieza variable por variable (problemas, reglas, justificación, riesgos).
- [`reports/libro_codigos.pdf`](reports/libro_codigos.pdf) — libro de códigos del dataset limpio (generado por `06_libro_codigos.py`, versionado en git).
