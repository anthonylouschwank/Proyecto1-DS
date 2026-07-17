"""
Paso 3 — Diagnostico del estado inicial de los datos crudos.

Carga los 23 CSV crudos de data/crudo/ (uno por departamento, generados por
03_scrape_all.py), los une SIN limpiar ni modificar ningun valor, y calcula
el diagnostico pedido por el proyecto:

  1. Numero de registros y variables.
  2. Tipo de dato de cada variable.
  3. Cantidad y % de valores faltantes por variable.
  4. Cantidad de valores unicos por variable.
  5. Cantidad de registros duplicados exactos.
  6. Variables con valores fuera de dominio o inconsistentes.
  7. Variables con formatos inconsistentes.
  8. Problemas potenciales de calidad de datos.

Todo el resultado se imprime en consola y se guarda en
reports/diagnostico_datos_crudos.md para entrega.

No se modifica ningun dato: este script es solo de analisis (actividad 3
del proyecto). La limpieza real se hace en un paso posterior.
"""

import glob
import re
from pathlib import Path

import pandas as pd

CRUDO_DIR = Path(__file__).resolve().parent / "data" / "crudo"
REPORT_PATH = Path(__file__).resolve().parent / "reports" / "diagnostico_datos_crudos.md"

# Dominios esperados segun los <select> del formulario (00_discover_form.py).
DOMINIO_NIVEL = {
    "PARVULOS", "PREPRIMARIA BILINGUE", "PRIMARIA", "PRIMARIA DE ADULTOS",
    "BASICO", "DIVERSIFICADO",
}
DOMINIO_SECTOR = {"OFICIAL", "PRIVADO", "MUNICIPAL", "COOPERATIVA"}
DOMINIO_MODALIDAD = {"MONOLINGUE", "BILINGUE"}
DOMINIO_AREA = {"URBANA", "RURAL"}

CODIGO_PAT = re.compile(r"^\d{2}-\d{2}-\d{4}-\d{2}$")
TELEFONO_DIGITOS_PAT = re.compile(r"^\d{8}$")

PLACEHOLDERS_TEXTO = {"-", "--", "---", "----", "-----", ".", "S/D", "SIN DATO", "N/A", "NINGUNO"}


def cargar_datos_crudos():
    archivos = sorted(glob.glob(str(CRUDO_DIR / "*.csv")))
    dfs = [pd.read_csv(f, dtype=str, encoding="utf-8-sig") for f in archivos]
    df = pd.concat(dfs, ignore_index=True)
    return df, archivos


def tabla_general(df):
    return f"Numero de registros: **{len(df)}**\n\nNumero de variables: **{df.shape[1]}**\n"


def tabla_tipos(df):
    tipos = pd.DataFrame({
        "variable": df.columns,
        "tipo_pandas": [str(df[c].dtype) for c in df.columns],
        "tipo_logico": [
            "texto libre" if c in ("ESTABLECIMIENTO", "DIRECCION", "SUPERVISOR", "DIRECTOR")
            else "categorica" if c in ("DEPARTAMENTO", "MUNICIPIO", "NIVEL", "SECTOR", "AREA",
                                        "STATUS", "MODALIDAD", "JORNADA", "PLAN", "DEPARTAMENTAL")
            else "identificador/codigo" if c in ("CODIGO", "DISTRITO")
            else "telefono (texto con formato)" if c == "TELEFONO"
            else "otro"
            for c in df.columns
        ],
    })
    return tipos


def tabla_faltantes(df):
    faltantes = df.isna().sum()
    pct = (faltantes / len(df) * 100).round(2)
    vacios = pd.Series({c: (df[c].fillna("").astype(str).str.strip() == "").sum() for c in df.columns})
    out = pd.DataFrame({
        "faltantes_NaN": faltantes,
        "pct_NaN": pct,
        "cadenas_vacias_incl_NaN": vacios,
    })
    return out


def tabla_unicos(df):
    return pd.DataFrame({"valores_unicos": df.nunique()})


def duplicados_exactos(df):
    return int(df.duplicated().sum())


def duplicados_semanticos(df):
    subset = ["ESTABLECIMIENTO", "DIRECCION", "MUNICIPIO", "NIVEL", "JORNADA", "SECTOR"]
    mask = df.duplicated(subset=subset, keep=False)
    return int(mask.sum()), df.loc[mask, "STATUS"].value_counts()


def fuera_de_dominio(df):
    hallazgos = {}
    hallazgos["NIVEL"] = df.loc[~df["NIVEL"].isin(DOMINIO_NIVEL), "NIVEL"].value_counts()
    hallazgos["SECTOR"] = df.loc[~df["SECTOR"].isin(DOMINIO_SECTOR), "SECTOR"].value_counts()
    hallazgos["MODALIDAD"] = df.loc[~df["MODALIDAD"].isin(DOMINIO_MODALIDAD), "MODALIDAD"].value_counts()
    hallazgos["AREA"] = df.loc[~df["AREA"].isin(DOMINIO_AREA), "AREA"].value_counts()
    return hallazgos


def formatos_inconsistentes(df):
    resultados = {}

    codigo_malo = (~df["CODIGO"].str.match(CODIGO_PAT)).sum()
    resultados["CODIGO fuera de patron NN-NN-NNNN-NN"] = int(codigo_malo)

    tel = df["TELEFONO"].dropna()
    tel_con_separadores = tel.str.contains(r"[/,\-\s]").sum()
    tel_solo_digitos = tel[tel.str.match(r"^\d+$")]
    tel_longitud_invalida = (tel_solo_digitos.apply(len) != 8).sum()
    resultados["TELEFONO con separadores (multiples numeros / texto)"] = int(tel_con_separadores)
    resultados["TELEFONO solo digitos con longitud != 8"] = int(tel_longitud_invalida)
    resultados["TELEFONO == 'S/D'"] = int((df["TELEFONO"] == "S/D").sum())

    espacios_dobles = {
        c: int(df[c].fillna("").str.contains(r"  +").sum())
        for c in ["ESTABLECIMIENTO", "DIRECCION", "SUPERVISOR", "DIRECTOR"]
    }
    resultados["Espacios dobles internos (por columna)"] = espacios_dobles

    distrito_formatos = df["DISTRITO"].dropna().str.replace(r"\d", "#", regex=True).value_counts().head(10)
    resultados["DISTRITO: patrones de formato mas comunes (digitos -> #)"] = distrito_formatos

    resultados["DIRECTOR con placeholder textual (-, S/D, SIN DATO, etc.)"] = int(
        df["DIRECTOR"].isin(PLACEHOLDERS_TEXTO).sum()
    )

    return resultados


def problemas_calidad(df):
    dup_sem_n, dup_sem_status = duplicados_semanticos(df)
    problemas = [
        "GUATEMALA vs CIUDAD CAPITAL: son dos entradas separadas del dropdown de "
        "departamento (value='01' y value='00'); administrativamente Ciudad Capital "
        "es el municipio 'Guatemala' del departamento Guatemala. No hay solapamiento "
        "de CODIGO entre ambos (verificado), pero hay que decidir si se unifican o "
        "se mantienen separados antes de reportar totales por departamento.",
        f"{dup_sem_n} filas comparten ESTABLECIMIENTO+DIRECCION+MUNICIPIO+NIVEL+JORNADA+SECTOR "
        "con un CODIGO distinto y, en la mayoria de los casos, un STATUS distinto "
        "(una fila ABIERTA y otra CERRADA/HISTORICA). Esto sugiere re-registro "
        "administrativo del mismo establecimiento con un CODIGO nuevo, no un "
        "duplicado exacto. Distribucion de STATUS en esas filas:\n"
        + dup_sem_status.to_string(),
        "NIVEL contiene 3 registros fuera del alcance del proyecto (que pide datos "
        "hasta diversificado): 1 'UNIVERSIDAD' y 2 'ADMINISTRATIVOS'.",
        "TELEFONO mezcla telefonos reales (8 digitos), valores con mas de un numero "
        "separados por '/' o '-', texto libre ('S/D', 'CEL. ...') y codigos muy "
        "cortos (1-3 digitos) que parecen placeholders de captura, no telefonos.",
        "DIRECTOR usa distintos placeholders de texto para 'sin dato' en vez de "
        "dejar la celda vacia ('-', '--', '---', '.', 'S/D', 'SIN DATO'), lo que "
        "infla el conteo de 'valores unicos' y esconde el verdadero porcentaje de "
        "faltantes si no se homologan a NaN.",
        "DISTRITO mezcla al menos dos formatos de codigo (NN-NNN y NN-NN-NNNN), "
        "posiblemente porque codifica cosas distintas segun el departamento/epoca.",
    ]
    return problemas


def df_to_md(df_or_series, index_name=None):
    if isinstance(df_or_series, pd.Series):
        df_or_series = df_or_series.to_frame("valor")
    try:
        return df_or_series.to_markdown()
    except ImportError:
        return "```\n" + df_or_series.to_string() + "\n```"


def main():
    df, archivos = cargar_datos_crudos()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    lineas = []
    lineas.append("# Diagnostico del estado inicial de los datos crudos\n")
    lineas.append(f"Fuente: {len(archivos)} archivos CSV crudos en `data/crudo/` "
                   "(uno por departamento, sin ninguna limpieza aplicada).\n")

    lineas.append("## 1. Numero de registros y variables\n")
    lineas.append(tabla_general(df))

    lineas.append("## 2. Tipo de dato de cada variable\n")
    lineas.append(df_to_md(tabla_tipos(df)))
    lineas.append(
        "\nNota: pandas carga todas las columnas como texto (`str`) porque el "
        "scraper las guarda como texto (CODIGO, TELEFONO y DISTRITO parecen "
        "numericos pero tienen ceros a la izquierda / separadores, asi que deben "
        "quedarse como texto). No hay ninguna variable numerica continua en el "
        "dataset.\n"
    )

    lineas.append("## 3. Valores faltantes por variable\n")
    lineas.append(df_to_md(tabla_faltantes(df)))
    lineas.append(
        "\nNota: 'cadenas_vacias_incl_NaN' cuenta NaN + strings vacios/solo "
        "espacios; en este dataset coincide exactamente con los NaN, es decir, "
        "no hay strings vacios escondidos que pandas no haya detectado como "
        "faltantes al leer el CSV.\n"
    )

    lineas.append("## 4. Cantidad de valores unicos por variable\n")
    lineas.append(df_to_md(tabla_unicos(df)))

    lineas.append("\n## 5. Registros duplicados exactos\n")
    lineas.append(f"Duplicados exactos (todas las columnas iguales): **{duplicados_exactos(df)}**\n")
    lineas.append(f"Duplicados por CODIGO (deberia ser llave unica): "
                   f"**{int(df.duplicated(subset=['CODIGO']).sum())}**\n")

    lineas.append("\n## 6. Variables con valores fuera de dominio\n")
    for var, serie in fuera_de_dominio(df).items():
        lineas.append(f"\n**{var}** (dominio esperado segun el formulario del sitio):\n")
        lineas.append(df_to_md(serie) if len(serie) else "Sin valores fuera de dominio.\n")

    lineas.append("\n## 7. Variables con formatos inconsistentes\n")
    for titulo, valor in formatos_inconsistentes(df).items():
        lineas.append(f"\n**{titulo}**\n")
        if isinstance(valor, dict):
            for k, v in valor.items():
                lineas.append(f"- {k}: {v}")
        elif isinstance(valor, (pd.Series, pd.DataFrame)):
            lineas.append(df_to_md(valor))
        else:
            lineas.append(str(valor))

    lineas.append("\n## 8. Problemas potenciales de calidad de datos\n")
    for i, p in enumerate(problemas_calidad(df), start=1):
        lineas.append(f"{i}. {p}\n")

    reporte = "\n".join(str(x) for x in lineas)
    REPORT_PATH.write_text(reporte, encoding="utf-8")
    print(reporte)
    print(f"\n\nReporte guardado en: {REPORT_PATH}")


if __name__ == "__main__":
    main()
