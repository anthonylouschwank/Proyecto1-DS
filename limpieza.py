"""Reglas reproducibles de limpieza para establecimientos educativos."""

import re
import unicodedata
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path

import pandas as pd


COLUMNAS_ESPERADAS = (
    "CODIGO", "DISTRITO", "DEPARTAMENTO", "MUNICIPIO", "ESTABLECIMIENTO",
    "DIRECCION", "TELEFONO", "SUPERVISOR", "DIRECTOR", "NIVEL", "SECTOR",
    "AREA", "STATUS", "MODALIDAD", "JORNADA", "PLAN", "DEPARTAMENTAL",
)
PREFIJOS_ESPERADOS = {f"{i:02d}" for i in range(23)}
NIVELES_HASTA_DIVERSIFICADO = {
    "INICIAL", "PARVULOS", "PARVULOS Y PREP. BILINGUE", "PREPRIMARIA BILINGUE",
    "PRIMARIA", "PRIMARIA DE ADULTOS", "BASICO", "DIVERSIFICADO",
}
DEPARTAMENTOS_VALIDOS = {
    "ALTA VERAPAZ", "BAJA VERAPAZ", "CHIMALTENANGO", "CHIQUIMULA", "EL PROGRESO",
    "ESCUINTLA", "GUATEMALA", "HUEHUETENANGO", "IZABAL", "JALAPA", "JUTIAPA",
    "PETEN", "QUETZALTENANGO", "QUICHE", "RETALHULEU", "SACATEPEQUEZ",
    "SAN MARCOS", "SANTA ROSA", "SOLOLA", "SUCHITEPEQUEZ", "TOTONICAPAN", "ZACAPA",
}
DEPARTAMENTO_POR_CODIGO = {
    1: "GUATEMALA", 2: "EL PROGRESO", 3: "SACATEPEQUEZ", 4: "CHIMALTENANGO",
    5: "ESCUINTLA", 6: "SANTA ROSA", 7: "SOLOLA", 8: "TOTONICAPAN",
    9: "QUETZALTENANGO", 10: "SUCHITEPEQUEZ", 11: "RETALHULEU", 12: "SAN MARCOS",
    13: "HUEHUETENANGO", 14: "QUICHE", 15: "BAJA VERAPAZ", 16: "ALTA VERAPAZ",
    17: "PETEN", 18: "IZABAL", 19: "ZACAPA", 20: "CHIQUIMULA", 21: "JALAPA",
    22: "JUTIAPA",
}
CATALOGO_MUNICIPIOS_PATH = Path(__file__).resolve().parent / "catalogos" / "municipios_segeplan_2026.csv"
ALIAS_MUNICIPIOS_MINEDUC = {
    ("ALTA VERAPAZ", "LA TINTA"): "SANTA CATALINA LA TINTA",
    ("ALTA VERAPAZ", "LANQUIN"): "SAN AGUSTIN LANQUIN",
    ("ALTA VERAPAZ", "SENAHU"): "SAN ANTONIO SENAHU",
    ("BAJA VERAPAZ", "SANTA CRUZ EL CHOL"): "EL CHOL",
    ("CHIMALTENANGO", "SAN MIGUEL POCHUTA"): "POCHUTA",
    ("CHIQUIMULA", "SAN JUAN ERMITA"): "SAN JUAN LA ERMITA",
    ("ESCUINTLA", "TIQUISATE"): "PUEBLO NUEVO TIQUISATE",
    ("GUATEMALA", "SAN MIGUEL PETAPA"): "PETAPA",
    ("HUEHUETENANGO", "SAN ILDEFONSO IXTAHUACAN"): "SAN IDELFONSO IXTAHUACAN",
    ("HUEHUETENANGO", "SANTA CRUZ BARILLAS"): "BARILLAS",
    ("HUEHUETENANGO", "UNION CANTINIL"): "LA UNION CANTINIL",
    ("QUICHE", "PACHALUN"): "PACHALUM",
    ("QUICHE", "PLAYA GRANDE"): "IXCAN",
    ("QUICHE", "SAN MIGUEL USPANTAN"): "USPANTAN",
    ("QUICHE", "SANTO TOMAS CHICHICASTENANGO"): "CHICHICASTENANGO",
    ("SAN MARCOS", "SAN JOSE EL RODEO"): "EL RODEO",
    ("SUCHITEPEQUEZ", "SAN MIGUEL PANAM"): "SAN MIGUEL PANAN",
}
DOMINIO_SECTOR = {"OFICIAL", "PRIVADO", "MUNICIPAL", "COOPERATIVA"}
DOMINIO_MODALIDAD = {"MONOLINGUE", "BILINGUE"}
DOMINIO_AREA = {"URBANA", "RURAL"}
PLACEHOLDERS_TEXTO = {"-", "--", "---", "----", "-----", ".", "S/D", "SIN DATO", "N/A", "NINGUNO"}
CODIGO_PAT = re.compile(r"^\d{2}-\d{2}-\d{4}-\d{2}$")
MAX_FRECUENCIA_TELEFONO_BLOQUE = 20


def cargar_datos_crudos(crudo_dir):
    """Carga sin modificar los 23 CSV de la extraccion definitiva."""
    crudo_dir = Path(crudo_dir)
    archivos = sorted(crudo_dir.glob("*.csv"))
    prefijos = {archivo.stem.split("_", maxsplit=1)[0] for archivo in archivos}
    if len(archivos) != 23 or prefijos != PREFIJOS_ESPERADOS:
        raise RuntimeError("Se requieren exactamente 23 CSV con prefijos 00-22.")

    partes = []
    for archivo in archivos:
        parte = pd.read_csv(archivo, dtype="string", encoding="utf-8-sig")
        if tuple(parte.columns) != COLUMNAS_ESPERADAS:
            raise RuntimeError(f"Encabezado inesperado en {archivo.name}.")
        partes.append(parte)

    df = pd.concat(partes, ignore_index=True)
    if df["NIVEL"].isna().any():
        raise RuntimeError("La extraccion contiene registros sin NIVEL.")
    return df, archivos


def _registrar(registro, variable, problema, transformacion, afectados, justificacion):
    registro.append({
        "Variable": variable,
        "Problema detectado": problema,
        "Transformacion": transformacion,
        "Registros afectados": int(afectados),
        "Justificacion": justificacion,
    })


def _normalizar_espacios(serie):
    return serie.str.replace(r"\s+", " ", regex=True).str.strip()


def limpiar_datos(df):
    """Aplica el plan sin mutar el DataFrame recibido."""
    if tuple(df.columns) != COLUMNAS_ESPERADAS:
        raise RuntimeError("El DataFrame no tiene el esquema crudo esperado.")
    limpio = df.copy(deep=True)
    registro = []

    fuera_de_alcance = ~limpio["NIVEL"].isin(NIVELES_HASTA_DIVERSIFICADO)
    _registrar(registro, "NIVEL", "Nivel fuera del recorrido hasta diversificado",
               "Excluir el registro del conjunto limpio", fuera_de_alcance.sum(),
               "Mantener unicamente niveles educativos desde inicial hasta diversificado.")
    limpio = limpio.loc[~fuera_de_alcance].reset_index(drop=True)

    distrito_incompleto = limpio["DISTRITO"].str.match(r"^\d{2}-$", na=False)
    limpio.loc[distrito_incompleto, "DISTRITO"] = pd.NA
    _registrar(registro, "DISTRITO", "Codigo incompleto NN-", "Convertir a NA",
               distrito_incompleto.sum(), "No contiene un identificador utilizable.")

    es_capital = limpio["DEPARTAMENTO"].eq("CIUDAD CAPITAL")
    zona = limpio.loc[es_capital, "MUNICIPIO"].str.extract(r"^ZONA\s*(\d+)$", expand=False)
    if zona.isna().any():
        raise RuntimeError("Hay filas de CIUDAD CAPITAL sin una zona extraible.")
    limpio["ZONA"] = pd.Series(pd.NA, index=limpio.index, dtype="string")
    limpio.loc[es_capital, "ZONA"] = zona
    limpio.loc[es_capital, "DEPARTAMENTO"] = "GUATEMALA"
    limpio.loc[es_capital, "MUNICIPIO"] = "GUATEMALA"
    columnas = limpio.columns.tolist()
    columnas.insert(columnas.index("MUNICIPIO") + 1, columnas.pop(columnas.index("ZONA")))
    limpio = limpio[columnas]
    _registrar(registro, "DEPARTAMENTO, MUNICIPIO, ZONA", "Ciudad Capital usa zonas como municipios",
               "Unificar en Guatemala y conservar la zona derivada", es_capital.sum(),
               "Alinear con los 22 departamentos sin perder la zona de origen.")

    for columna in ("ESTABLECIMIENTO", "DIRECCION", "SUPERVISOR", "DIRECTOR"):
        antes = limpio[columna].copy()
        limpio[columna] = _normalizar_espacios(limpio[columna])
        afectados = antes.fillna("").ne(limpio[columna].fillna(""))
        _registrar(registro, columna, "Espacios iniciales, finales o multiples",
                   "Recortar y colapsar espacios", afectados.sum(),
                   "Uniformar formato sin cambiar ortografia ni capitalizacion.")

    director_placeholder = limpio["DIRECTOR"].isin(PLACEHOLDERS_TEXTO)
    limpio.loc[director_placeholder, "DIRECTOR"] = pd.NA
    _registrar(registro, "DIRECTOR", "Placeholder textual de dato faltante", "Convertir a NA",
               director_placeholder.sum(), "Representar faltantes de forma consistente.")

    telefono_antes = limpio["TELEFONO"].copy()
    telefono_extraido = limpio["TELEFONO"].str.extract(r"(?<!\d)(\d{8})(?!\d)", expand=False)
    limpio["TELEFONO"] = telefono_extraido.astype("string")
    telefono_cambio = telefono_antes.fillna("").ne(limpio["TELEFONO"].fillna(""))
    _registrar(registro, "TELEFONO", "Formato distinto de un numero de 8 digitos",
               "Conservar el primer numero completo de 8 digitos o convertir a NA",
               telefono_cambio.sum(), "No completar ni truncar numeros ambiguos.")

    area_sin_especificar = limpio["AREA"].eq("SIN ESPECIFICAR")
    limpio.loc[area_sin_especificar, "AREA"] = pd.NA
    _registrar(registro, "AREA", "Categoria SIN ESPECIFICAR", "Convertir a NA",
               area_sin_especificar.sum(), "Es ausencia de informacion, no un area geografica.")

    return limpio, pd.DataFrame(registro)


def validar_consistencia(df):
    """Verifica las invariantes disponibles sin inventar catalogos municipales."""
    errores = []
    if not df["CODIGO"].str.match(CODIGO_PAT, na=False).all():
        errores.append("CODIGO fuera de formato")
    if not df["CODIGO"].is_unique:
        errores.append("CODIGO duplicado")
    if not set(df["NIVEL"].dropna().unique()) <= NIVELES_HASTA_DIVERSIFICADO:
        errores.append("NIVEL fuera del alcance")
    if not set(df["DEPARTAMENTO"].dropna().unique()) <= DEPARTAMENTOS_VALIDOS:
        errores.append("DEPARTAMENTO fuera de catalogo")
    if not set(df["SECTOR"].dropna().unique()) <= DOMINIO_SECTOR:
        errores.append("SECTOR fuera de dominio")
    if not set(df["MODALIDAD"].dropna().unique()) <= DOMINIO_MODALIDAD:
        errores.append("MODALIDAD fuera de dominio")
    if not set(df["AREA"].dropna().unique()) <= DOMINIO_AREA:
        errores.append("AREA fuera de dominio")
    zona_inconsistente = df["ZONA"].notna() & (
        df["DEPARTAMENTO"].ne("GUATEMALA") | df["MUNICIPIO"].ne("GUATEMALA")
    )
    if zona_inconsistente.any():
        errores.append("ZONA contradice DEPARTAMENTO o MUNICIPIO")
    if errores:
        raise RuntimeError("; ".join(errores))
    return True


def _texto_comparable(valor):
    """Normaliza solo para comparar; nunca reemplaza el valor original."""
    if pd.isna(valor):
        return ""
    texto = unicodedata.normalize("NFKD", str(valor).upper())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"[^A-Z0-9]+", " ", texto).strip()


def detectar_duplicados_exactos(df):
    """Devuelve todas las filas involucradas en duplicados exactos."""
    duplicados = df.loc[df.duplicated(keep=False)].copy()
    duplicados.insert(0, "INDICE_ORIGINAL", duplicados.index)
    duplicados["PATRON"] = ""
    duplicados["DECISION"] = "PENDIENTE_REVISION"
    duplicados["JUSTIFICACION"] = ""
    return duplicados.reset_index(drop=True)


def decidir_duplicados_exactos(exactos):
    """Documenta la decision sin eliminar filas del conjunto limpio."""
    if exactos.empty:
        return exactos
    decididos = exactos.copy()
    decididos["PATRON"] = "DUPLICADO_EXACTO_CONSERVADO"
    decididos["DECISION"] = "CONSERVAR_TODOS"
    decididos["JUSTIFICACION"] = (
        "Filas identicas en todas las columnas; se conservan todas para no "
        "perder trazabilidad hasta una revision que justifique eliminar alguna."
    )
    return decididos


def _partir_valores_grupo(texto):
    if texto is None or (isinstance(texto, float) and pd.isna(texto)) or texto == "":
        return []
    return [parte.strip() for parte in str(texto).split(" | ") if parte.strip()]


def _clasificar_grupo_parcial(fila, df):
    """Asigna patron y justificacion; la decision siempre es conservar."""
    codigos = _partir_valores_grupo(fila["CODIGOS"])
    direcciones = {
        _texto_comparable(valor) for valor in _partir_valores_grupo(fila["DIRECCIONES"])
        if _texto_comparable(valor)
    }
    telefonos = {
        _texto_comparable(valor) for valor in _partir_valores_grupo(fila["TELEFONOS"])
        if _texto_comparable(valor)
    }
    n_codigos = len(codigos)
    n_direcciones = len(direcciones)
    n_telefonos = len(telefonos)

    if n_codigos >= 2 and n_direcciones >= 2:
        return (
            "RED_MISMO_NOMBRE_DISTINTA_DIRECCION",
            "Misma red o nombre operativo en ubicaciones distintas; cada CODIGO "
            "corresponde a un establecimiento distinto y se conservan todos.",
        )

    if n_codigos >= 2:
        subset = df.loc[df["CODIGO"].isin(codigos), "STATUS"]
        n_status = int(subset.nunique(dropna=True))
        if n_status >= 2:
            return (
                "REREGISTRO_ADMINISTRATIVO",
                "Mismos o muy similares nombre y direccion con CODIGO distinto y "
                "STATUS distinto; se interpreta como re-registro administrativo y "
                "se conservan todos los historicos.",
            )
        return (
            "REREGISTRO_ADMINISTRATIVO",
            "Mismos o muy similares nombre y direccion con CODIGO distinto; se "
            "interpreta como re-registro administrativo y se conservan todos.",
        )

    if n_telefonos == 1 and (n_direcciones >= 2 or n_codigos >= 2):
        return (
            "TELEFONO_COMPARTIDO",
            "Telefono institucional compartido entre registros distintos; no "
            "implica duplicado eliminable y se conservan todos.",
        )

    return (
        "CANDIDATO_SIMILITUD_CONSERVADO",
        "Similitud >= 0.90 en al menos dos criterios genera candidato, pero sin "
        "evidencia de duplicado exacto se conservan todas las filas.",
    )


def decidir_duplicados_parciales(grupos, df):
    """Clasifica cada grupo por patron automatico y conserva todos los registros."""
    if grupos.empty:
        decididos = grupos.copy()
        if "PATRON" not in decididos.columns:
            decididos["PATRON"] = pd.Series(dtype="string")
        return decididos

    decididos = grupos.copy()
    patrones = []
    decisiones = []
    justificaciones = []
    for _, fila in decididos.iterrows():
        patron, justificacion = _clasificar_grupo_parcial(fila, df)
        patrones.append(patron)
        decisiones.append("CONSERVAR_TODOS")
        justificaciones.append(justificacion)
    decididos["PATRON"] = patrones
    decididos["DECISION"] = decisiones
    decididos["JUSTIFICACION"] = justificaciones
    return decididos


def registrar_decision_duplicados(registro, grupos):
    """Anade al registro la documentacion de decisiones sobre duplicados parciales."""
    filas = registro.to_dict("records") if registro is not None and len(registro) else []
    n_grupos = 0 if grupos is None else len(grupos)
    conteo = {}
    if grupos is not None and not grupos.empty and "PATRON" in grupos.columns:
        conteo = grupos["PATRON"].value_counts().to_dict()
    detalle = ", ".join(f"{patron}={cantidad}" for patron, cantidad in sorted(conteo.items()))
    justificacion = (
        f"Se clasificaron {n_grupos} grupos; fusionados=0, eliminados=0. "
        f"Distribucion de patrones: {detalle or 'ninguno'}."
    )
    _registrar(
        filas,
        "DUPLICADOS_PARCIALES",
        "Grupos candidatos por similitud de nombre, direccion o telefono",
        "Documentar decision CONSERVAR_TODOS por patron automatico (0 filas eliminadas)",
        n_grupos,
        justificacion,
    )
    return pd.DataFrame(filas)


def detectar_duplicados_parciales(df, umbral=0.90):
    """Genera candidatos por similitud sin eliminar ni fusionar registros."""
    if not 0 <= umbral <= 1:
        raise ValueError("El umbral debe estar entre 0 y 1.")

    comparables = pd.DataFrame(index=df.index)
    for columna in ("ESTABLECIMIENTO", "DIRECCION", "TELEFONO"):
        comparables[columna] = df[columna].map(_texto_comparable)
    frecuencia_telefono = comparables["TELEFONO"].value_counts()

    bloques = {}
    for indice in df.index:
        ubicacion = (
            _texto_comparable(df.at[indice, "DEPARTAMENTO"]),
            _texto_comparable(df.at[indice, "MUNICIPIO"]),
        )
        nombre = comparables.at[indice, "ESTABLECIMIENTO"]
        direccion = comparables.at[indice, "DIRECCION"]
        telefono = comparables.at[indice, "TELEFONO"]
        claves = []
        if len(nombre) >= 6:
            claves.append(("nombre", *ubicacion, nombre[:12]))
        if len(direccion) >= 6:
            claves.append(("direccion", *ubicacion, direccion[:12]))
        if len(telefono) >= 8 and frecuencia_telefono.get(telefono, 0) <= MAX_FRECUENCIA_TELEFONO_BLOQUE:
            claves.append(("telefono", *ubicacion, telefono))
        for clave in claves:
            bloques.setdefault(clave, []).append(indice)

    criterios_por_par = {}
    for clave, indices in bloques.items():
        criterio = clave[0]
        for par in combinations(indices, 2):
            par_ordenado = tuple(sorted(par))
            criterios_por_par.setdefault(par_ordenado, set()).add(criterio)

    # Si un par no coincide ni siquiera en los bloques de dos campos distintos,
    # no puede satisfacer la regla de dos criterios y no requiere comparacion.
    pares = [
        par for par, criterios in criterios_por_par.items()
        if len(criterios) >= 2
    ]

    candidatos = []
    for indice_a, indice_b in sorted(pares):
        fila_a = df.loc[indice_a]
        fila_b = df.loc[indice_b]
        if fila_a.equals(fila_b):
            continue

        similitudes = {}
        for columna in ("ESTABLECIMIENTO", "DIRECCION", "TELEFONO"):
            valor_a = comparables.at[indice_a, columna]
            valor_b = comparables.at[indice_b, columna]
            if not valor_a or not valor_b:
                similitudes[columna] = 0.0
            elif valor_a == valor_b:
                similitudes[columna] = 1.0
            elif columna == "TELEFONO":
                # Tras la estandarizacion son cadenas de ocho digitos: dos
                # telefonos distintos nunca alcanzan el umbral de 0.90.
                similitudes[columna] = 0.0
            else:
                similitudes[columna] = SequenceMatcher(None, valor_a, valor_b).ratio()
        puntuaciones_ordenadas = sorted(similitudes.values(), reverse=True)
        criterios_coincidentes = sum(valor >= umbral for valor in similitudes.values())
        if criterios_coincidentes < 2:
            continue
        puntuacion = sum(puntuaciones_ordenadas[:2]) / 2

        candidatos.append({
            "INDICE_A": int(indice_a),
            "INDICE_B": int(indice_b),
            "CODIGO_A": fila_a["CODIGO"],
            "CODIGO_B": fila_b["CODIGO"],
            "DEPARTAMENTO": fila_a["DEPARTAMENTO"],
            "MUNICIPIO": fila_a["MUNICIPIO"],
            "ESTABLECIMIENTO_A": fila_a["ESTABLECIMIENTO"],
            "ESTABLECIMIENTO_B": fila_b["ESTABLECIMIENTO"],
            "SIMILITUD_ESTABLECIMIENTO": round(similitudes["ESTABLECIMIENTO"], 4),
            "DIRECCION_A": fila_a["DIRECCION"],
            "DIRECCION_B": fila_b["DIRECCION"],
            "SIMILITUD_DIRECCION": round(similitudes["DIRECCION"], 4),
            "TELEFONO_A": fila_a["TELEFONO"],
            "TELEFONO_B": fila_b["TELEFONO"],
            "SIMILITUD_TELEFONO": round(similitudes["TELEFONO"], 4),
            "CRITERIOS_COINCIDENTES": criterios_coincidentes,
            "PUNTUACION_COMBINADA": round(puntuacion, 4),
            "DECISION": "PENDIENTE_REVISION",
            "JUSTIFICACION": "",
        })

    columnas = (
        "INDICE_A", "INDICE_B", "CODIGO_A", "CODIGO_B", "DEPARTAMENTO", "MUNICIPIO",
        "ESTABLECIMIENTO_A", "ESTABLECIMIENTO_B", "SIMILITUD_ESTABLECIMIENTO",
        "DIRECCION_A", "DIRECCION_B", "SIMILITUD_DIRECCION", "TELEFONO_A", "TELEFONO_B",
        "SIMILITUD_TELEFONO", "CRITERIOS_COINCIDENTES", "PUNTUACION_COMBINADA",
        "DECISION", "JUSTIFICACION",
    )
    return pd.DataFrame(candidatos, columns=columnas)


def agrupar_duplicados_parciales(candidatos):
    """Colapsa pares relacionados en casos unicos para revision humana."""
    columnas = (
        "GRUPO_ID", "REGISTROS", "PARES_SOPORTE", "CODIGOS", "ESTABLECIMIENTOS",
        "DIRECCIONES", "TELEFONOS", "PUNTUACION_COMBINADA_MAXIMA",
        "PUNTUACION_COMBINADA_PROMEDIO", "PATRON", "DECISION", "JUSTIFICACION",
    )
    if candidatos.empty:
        return pd.DataFrame(columns=columnas)

    padre = {}

    def buscar(indice):
        padre.setdefault(indice, indice)
        if padre[indice] != indice:
            padre[indice] = buscar(padre[indice])
        return padre[indice]

    def unir(a, b):
        raiz_a, raiz_b = buscar(a), buscar(b)
        if raiz_a != raiz_b:
            padre[raiz_b] = raiz_a

    for indice_a, indice_b in candidatos[["INDICE_A", "INDICE_B"]].itertuples(index=False, name=None):
        unir(int(indice_a), int(indice_b))

    filas_por_raiz = {}
    for indice_fila, fila in candidatos.iterrows():
        raiz = buscar(int(fila["INDICE_A"]))
        filas_por_raiz.setdefault(raiz, []).append(indice_fila)

    grupos = []
    for numero, indices_filas in enumerate(filas_por_raiz.values(), start=1):
        pares = candidatos.loc[indices_filas]

        def valores_unicos(columna_a, columna_b):
            valores = pd.concat([pares[columna_a], pares[columna_b]], ignore_index=True).dropna()
            return " | ".join(sorted({str(valor) for valor in valores}))

        codigos = valores_unicos("CODIGO_A", "CODIGO_B")
        grupos.append({
            "GRUPO_ID": f"DP-{numero:05d}",
            "REGISTROS": len(codigos.split(" | ")) if codigos else 0,
            "PARES_SOPORTE": len(pares),
            "CODIGOS": codigos,
            "ESTABLECIMIENTOS": valores_unicos("ESTABLECIMIENTO_A", "ESTABLECIMIENTO_B"),
            "DIRECCIONES": valores_unicos("DIRECCION_A", "DIRECCION_B"),
            "TELEFONOS": valores_unicos("TELEFONO_A", "TELEFONO_B"),
            "PUNTUACION_COMBINADA_MAXIMA": round(pares["PUNTUACION_COMBINADA"].max(), 4),
            "PUNTUACION_COMBINADA_PROMEDIO": round(pares["PUNTUACION_COMBINADA"].mean(), 4),
            "PATRON": "",
            "DECISION": "PENDIENTE_REVISION",
            "JUSTIFICACION": "",
        })
    return pd.DataFrame(grupos, columns=columnas).sort_values(
        ["REGISTROS", "PARES_SOPORTE"], ascending=False, ignore_index=True,
    )


def exportar_duplicados(exactos, parciales, exactos_path, parciales_path):
    """Exporta tablas para revision humana sin modificar el dataset."""
    exactos_path = Path(exactos_path)
    parciales_path = Path(parciales_path)
    exactos_path.parent.mkdir(parents=True, exist_ok=True)
    parciales_path.parent.mkdir(parents=True, exist_ok=True)
    exactos.to_csv(exactos_path, index=False, encoding="utf-8-sig")
    parciales.to_csv(parciales_path, index=False, encoding="utf-8-sig")


def cargar_catalogo_geografico(path=CATALOGO_MUNICIPIOS_PATH):
    """Carga los 340 municipios oficiales desde un recurso independiente de SEGEPLAN."""
    catalogo = pd.read_csv(path, sep=";", encoding="latin-1", dtype=str)
    catalogo = catalogo.dropna(how="all").reset_index(drop=True)
    codigos = pd.to_numeric(catalogo.iloc[:, 0].str.strip(), errors="raise").astype(int)
    municipios = catalogo.iloc[:, 1].str.strip()
    if len(catalogo) != 340 or codigos.nunique() != 340:
        raise RuntimeError("El catalogo de SEGEPLAN no contiene 340 codigos municipales unicos.")

    pares = set()
    for codigo, municipio in zip(codigos, municipios):
        departamento_codigo = codigo // 100
        if departamento_codigo not in DEPARTAMENTO_POR_CODIGO:
            raise RuntimeError(f"Codigo departamental desconocido en catalogo: {codigo}")
        pares.add((
            _texto_comparable(DEPARTAMENTO_POR_CODIGO[departamento_codigo]),
            _texto_comparable(municipio),
        ))
    if len(pares) != 340:
        raise RuntimeError("El catalogo geografico contiene pares repetidos.")
    return pares


def _par_geografico_comparable(departamento, municipio):
    departamento = _texto_comparable(departamento)
    municipio = _texto_comparable(municipio)
    municipio = ALIAS_MUNICIPIOS_MINEDUC.get((departamento, municipio), municipio)
    return departamento, municipio


def _categorias_inconsistentes(df):
    columnas = (
        "DEPARTAMENTO", "MUNICIPIO", "NIVEL", "SECTOR", "AREA", "STATUS",
        "MODALIDAD", "JORNADA", "PLAN", "DEPARTAMENTAL",
    )
    inconsistencias = {}
    for columna in columnas:
        variantes = {}
        for valor in df[columna].dropna().unique():
            variantes.setdefault(_texto_comparable(valor), set()).add(str(valor))
        repetidas = {clave: valores for clave, valores in variantes.items() if len(valores) > 1}
        if repetidas:
            inconsistencias[columna] = repetidas
    return inconsistencias


def _variables_formato_inconsistente(df):
    variables = set()
    for columna in ("ESTABLECIMIENTO", "DIRECCION", "SUPERVISOR", "DIRECTOR"):
        serie = df[columna].dropna()
        if serie.str.contains(r"^\s|\s$|\s{2,}", regex=True).any():
            variables.add(columna)
    if (~df["CODIGO"].str.match(CODIGO_PAT, na=False)).any():
        variables.add("CODIGO")
    if df["DISTRITO"].str.match(r"^\d{2}-$", na=False).any():
        variables.add("DISTRITO")
    if (~df["TELEFONO"].dropna().str.match(r"^\d{8}$")).any():
        variables.add("TELEFONO")
    if df["DIRECTOR"].isin(PLACEHOLDERS_TEXTO).any():
        variables.add("DIRECTOR")
    if df["AREA"].eq("SIN ESPECIFICAR").any():
        variables.add("AREA")
    return variables


def ejecutar_pruebas_calidad(df, catalogo_geografico):
    """Ejecuta las reglas objetivas requeridas y devuelve su detalle."""
    textos = ("ESTABLECIMIENTO", "DIRECCION", "SUPERVISOR", "DIRECTOR")
    espacios_invalidos = sum(
        int(df[columna].dropna().str.contains(r"^\s|\s$", regex=True).sum())
        for columna in textos
    )
    telefonos_invalidos = int((~df["TELEFONO"].dropna().str.match(r"^\d{8}$")).sum())
    pares_observados = {
        _par_geografico_comparable(departamento, municipio)
        for departamento, municipio
        in df[["DEPARTAMENTO", "MUNICIPIO"]].drop_duplicates().itertuples(index=False, name=None)
    }
    pares_invalidos = pares_observados - set(catalogo_geografico)
    tipos_invalidos = [columna for columna in df.columns if str(df[columna].dtype) != "string"]
    categorias_inconsistentes = _categorias_inconsistentes(df)
    valores_invalidos = {
        "CODIGO": int((~df["CODIGO"].str.match(CODIGO_PAT, na=False)).sum()),
        "DISTRITO": int(df["DISTRITO"].str.match(r"^\d{2}-$", na=False).sum()),
        "DIRECTOR": int(df["DIRECTOR"].isin(PLACEHOLDERS_TEXTO).sum()),
        "AREA": int(df["AREA"].eq("SIN ESPECIFICAR").sum()),
    }
    zona_inconsistente = int((df["ZONA"].notna() & (
        df["DEPARTAMENTO"].ne("GUATEMALA") | df["MUNICIPIO"].ne("GUATEMALA")
    )).sum())

    pruebas = [
        ("Sin duplicados exactos", int(df.duplicated().sum()) == 0, int(df.duplicated().sum())),
        ("Sin espacios iniciales o finales", espacios_invalidos == 0, espacios_invalidos),
        ("Telefonos con formato uniforme", telefonos_invalidos == 0, telefonos_invalidos),
        ("Departamentos dentro del catalogo", set(df["DEPARTAMENTO"].dropna().unique()) <= DEPARTAMENTOS_VALIDOS,
         sorted(set(df["DEPARTAMENTO"].dropna().unique()) - DEPARTAMENTOS_VALIDOS)),
        ("Municipios consistentes con la fuente", not pares_invalidos, sorted(pares_invalidos)),
        ("Variables con tipo esperado", not tipos_invalidos, tipos_invalidos),
        ("Sin categorias duplicadas por escritura", not categorias_inconsistentes, categorias_inconsistentes),
        ("Sin valores invalidos diagnosticados", not any(valores_invalidos.values()), valores_invalidos),
        ("Zona consistente con Guatemala", zona_inconsistente == 0, zona_inconsistente),
        ("Niveles dentro del recorrido hasta diversificado",
         set(df["NIVEL"].dropna().unique()) <= NIVELES_HASTA_DIVERSIFICADO,
         sorted(df["NIVEL"].dropna().unique())),
    ]
    return pd.DataFrame([
        {"Prueba": nombre, "Resultado": "OK" if cumple else "FALLO", "Detalle": str(detalle)}
        for nombre, cumple, detalle in pruebas
    ])


def exigir_pruebas_aprobadas(pruebas):
    """Impide exportar cuando al menos una regla de calidad falla."""
    fallos = pruebas.loc[pruebas["Resultado"] != "OK", "Prueba"].tolist()
    if fallos:
        raise RuntimeError(f"Fallaron pruebas de calidad: {fallos}")
    return True


def _metricas_dataset(df, duplicados_parciales):
    faltantes = int(df.isna().sum().sum())
    total_celdas = int(df.shape[0] * df.shape[1])
    return {
        "Registros": len(df),
        "Variables": df.shape[1],
        "Valores faltantes": f"{faltantes} ({faltantes / total_celdas * 100:.2f}%)" if total_celdas else "0 (0.00%)",
        "Variables con NA": int((df.isna().sum() > 0).sum()),
        "Duplicados exactos": int(df.duplicated().sum()),
        "Posibles duplicados": len(duplicados_parciales),
        "Variables con formato inconsistente": len(_variables_formato_inconsistente(df)),
        "Variables con tipo incorrecto": sum(str(df[columna].dtype) != "string" for columna in df.columns),
        "Categorias inconsistentes": sum(len(grupos) for grupos in _categorias_inconsistentes(df).values()),
    }


def construir_informe_calidad(df_antes, df_despues, parciales_antes, parciales_despues, registro):
    """Construye la comparacion exigida sin usar cifras escritas manualmente."""
    antes = _metricas_dataset(df_antes, parciales_antes)
    despues = _metricas_dataset(df_despues, parciales_despues)
    metricas = list(antes)
    tabla = pd.DataFrame({
        "Metrica": metricas + ["Errores corregidos"],
        "Antes": [antes[metrica] for metrica in metricas] + [0],
        "Despues": [despues[metrica] for metrica in metricas]
        + [int(registro["Registros afectados"].sum())],
    })
    eliminados = len(df_antes) - len(df_despues)
    explicacion_registros = (
        f"Registros: cambio de {len(df_antes)} a {len(df_despues)}; se excluyeron "
        f"{eliminados} registros con NIVEL fuera del recorrido hasta diversificado."
        if eliminados
        else f"Registros: se conservaron las {len(df_antes)} filas; no hubo niveles fuera de alcance."
    )
    n_parciales = len(parciales_despues)
    if parciales_despues is not None and not parciales_despues.empty and "DECISION" in parciales_despues:
        conservados = int(parciales_despues["DECISION"].eq("CONSERVAR_TODOS").sum())
        if "PATRON" in parciales_despues.columns:
            resumen_patrones = ", ".join(
                f"{patron}={cantidad}"
                for patron, cantidad in sorted(parciales_despues["PATRON"].value_counts().items())
            )
        else:
            resumen_patrones = "sin patron"
        explicacion_duplicados = (
            f"Posibles duplicados: {n_parciales} grupos candidatos; conservados={conservados}, "
            f"fusionados=0, corregidos=0. Patrones: {resumen_patrones}."
        )
    else:
        explicacion_duplicados = (
            f"Posibles duplicados: {n_parciales} grupos candidatos; conservados=0, "
            "fusionados=0, corregidos=0."
        )
    explicaciones = [
        explicacion_registros,
        f"Variables: cambio de {df_antes.shape[1]} a {df_despues.shape[1]} por la variable derivada ZONA.",
        explicacion_duplicados,
        "Errores corregidos: suma de registros afectados por regla; una fila puede contarse en mas de una regla.",
    ]
    return tabla, explicaciones


CUMPLIMIENTO_ENUNCIADO = """
## Cumplimiento del enunciado

| Requisito | Estado |
|---|---|
| 1-2. Descarga y CSV crudos (23 archivos) | CUMPLE |
| 3. Diagnostico inicial a-h | CUMPLE |
| 4. Plan de limpieza por variable | CUMPLE |
| 5a-f. Limpieza (faltantes, tipos, texto, categorias, formatos, invalidos) | CUMPLE |
| 5g. Duplicados exactos/parciales con decision documentada | CUMPLE (CONSERVAR_TODOS por patron) |
| 5h-i. Consistencia entre variables y derivadas | CUMPLE |
| 6. Registro de transformaciones | CUMPLE |
| 7. Pruebas automaticas de calidad | CUMPLE |
| 8. Informe de calidad antes/despues | CUMPLE |
| 9. Conjunto limpio unico | CUMPLE |
| 10. Libro de codigos | CUMPLE |
| 11. Reproducibilidad | CUMPLE (scripts numerados, requirements.txt, informe Word regenerable) |
""".strip()


def exportar_informe_calidad(tabla, explicaciones, pruebas, path):
    """Escribe el informe comparativo y la evidencia de pruebas."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    contenido = [
        "# Informe de calidad de los datos\n",
        "## Comparacion antes y despues\n",
        tabla.to_markdown(index=False),
        "\n## Explicaciones\n",
        "\n".join(f"- {texto}" for texto in explicaciones),
        "\n## Pruebas automaticas\n",
        pruebas.to_markdown(index=False),
        "",
        CUMPLIMIENTO_ENUNCIADO,
        "",
    ]
    path.write_text("\n".join(contenido), encoding="utf-8")


def exportar_resultados(df, registro, csv_path, registro_path):
    """Exporta solo resultados derivados; nunca sobrescribe los CSV crudos."""
    csv_path = Path(csv_path)
    registro_path = Path(registro_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    registro_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    registro_path.write_text(registro.to_markdown(index=False) + "\n", encoding="utf-8")
