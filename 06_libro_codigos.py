"""Genera el libro de codigos en Markdown y PDF desde el dataset limpio."""

import argparse
import html
from datetime import date
from pathlib import Path

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer


FUENTE = "MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)"
COLUMNAS_ESPERADAS = (
    "CODIGO", "DISTRITO", "DEPARTAMENTO", "MUNICIPIO", "ZONA", "ESTABLECIMIENTO",
    "DIRECCION", "TELEFONO", "SUPERVISOR", "DIRECTOR", "NIVEL", "SECTOR", "AREA",
    "STATUS", "MODALIDAD", "JORNADA", "PLAN", "DEPARTAMENTAL",
)
COLUMNAS_CATEGORICAS = {
    "DEPARTAMENTO", "MUNICIPIO", "ZONA", "NIVEL", "SECTOR", "AREA", "STATUS",
    "MODALIDAD", "JORNADA", "PLAN", "DEPARTAMENTAL",
}
NIVELES_HASTA_DIVERSIFICADO = {
    "INICIAL", "PARVULOS", "PARVULOS Y PREP. BILINGUE", "PREPRIMARIA BILINGUE",
    "PRIMARIA", "PRIMARIA DE ADULTOS", "BASICO", "DIVERSIFICADO",
}

METADATOS = {
    "CODIGO": ("Identificador unico del registro educativo.", "Texto", "Patron NN-NN-NNNN-NN",
               "Se conserva sin cambios y se valida como llave unica.", "No"),
    "DISTRITO": ("Codigo administrativo de distrito.", "Texto", "NN-NNN o NN-NN-NNNN; admite NA",
                  "Los codigos incompletos NN- se convierten a NA.", "No"),
    "DEPARTAMENTO": ("Departamento de Guatemala.", "Texto categorico", "22 departamentos oficiales",
                      "CIUDAD CAPITAL se unifica en GUATEMALA.", "No"),
    "MUNICIPIO": ("Municipio del establecimiento.", "Texto categorico", "Catalogo oficial SEGEPLAN 2026",
                   "Las zonas de Ciudad Capital se asignan al municipio GUATEMALA.", "No"),
    "ZONA": ("Zona de Ciudad de Guatemala cuando aplica.", "Texto", "Numero de zona o NA",
             "Se extrae del MUNICIPIO original antes de unificar Ciudad Capital.", "Si: derivada"),
    "ESTABLECIMIENTO": ("Nombre del establecimiento educativo.", "Texto libre", "Texto o NA",
                        "Se recortan y colapsan espacios; se conserva la escritura original.", "No"),
    "DIRECCION": ("Direccion reportada del establecimiento.", "Texto libre", "Texto o NA",
                  "Se recortan y colapsan espacios.", "No"),
    "TELEFONO": ("Telefono principal reportado.", "Texto", "Ocho digitos o NA",
                 "Se conserva el primer numero completo de ocho digitos; lo ambiguo pasa a NA.", "No"),
    "SUPERVISOR": ("Persona o entidad supervisora.", "Texto libre", "Texto o NA",
                   "Se recortan y colapsan espacios.", "No"),
    "DIRECTOR": ("Nombre de la persona directora.", "Texto libre", "Texto o NA",
                 "Se normalizan espacios y placeholders de faltante a NA.", "No"),
    "NIVEL": ("Nivel escolar del establecimiento.", "Texto categorico",
              "Niveles educativos desde inicial hasta diversificado",
              "Se excluyen categorias fuera del recorrido educativo definido.", "No"),
    "SECTOR": ("Sector administrativo.", "Texto categorico", "OFICIAL, PRIVADO, MUNICIPAL o COOPERATIVA",
               "Se conserva y valida contra su dominio.", "No"),
    "AREA": ("Area geografica.", "Texto categorico", "URBANA, RURAL o NA",
             "SIN ESPECIFICAR se convierte a NA.", "No"),
    "STATUS": ("Estado administrativo del registro.", "Texto categorico", "Categorias observadas en la fuente",
               "Se conserva sin cambios.", "No"),
    "MODALIDAD": ("Modalidad linguistica.", "Texto categorico", "MONOLINGUE o BILINGUE",
                  "Se conserva y valida contra su dominio.", "No"),
    "JORNADA": ("Jornada educativa.", "Texto categorico", "Categorias observadas en la fuente",
                "Se conserva sin cambios.", "No"),
    "PLAN": ("Plan de estudios o asistencia.", "Texto categorico", "Categorias observadas en la fuente",
             "Se conserva sin cambios.", "No"),
    "DEPARTAMENTAL": ("Oficina departamental de educacion responsable.", "Texto categorico",
                      "Categorias observadas en la fuente", "Se conserva sin cambios.", "No"),
}


def cargar_dataset(path):
    df = pd.read_csv(path, dtype="string", encoding="utf-8-sig")
    if tuple(df.columns) != COLUMNAS_ESPERADAS:
        raise RuntimeError(f"Esquema limpio inesperado: {tuple(df.columns)}")
    if not set(df["NIVEL"].dropna().unique()) <= NIVELES_HASTA_DIVERSIFICADO:
        raise RuntimeError("El dataset contiene niveles fuera del recorrido hasta diversificado.")
    if not df["CODIGO"].is_unique:
        raise RuntimeError("CODIGO no es unico; no se puede publicar el libro de codigos.")
    return df


def valores_posibles(df, variable):
    serie = df[variable]
    faltantes = int(serie.isna().sum())
    if variable in COLUMNAS_CATEGORICAS:
        valores = sorted(str(valor) for valor in serie.dropna().unique())
        texto = ", ".join(valores) if valores else "Sin valores no nulos observados"
    else:
        texto = f"{serie.nunique(dropna=True)} valores no nulos observados; consultar el CSV"
    return f"{texto}. Faltantes: {faltantes}."


def construir_entradas(df, fecha_extraccion, version):
    entradas = []
    for variable in COLUMNAS_ESPERADAS:
        descripcion, tipo, dominio, tratamiento, derivada = METADATOS[variable]
        entradas.append({
            "Variable": variable,
            "Descripcion": descripcion,
            "Tipo de dato": tipo,
            "Dominio permitido": dominio,
            "Valores posibles": valores_posibles(df, variable),
            "Tratamiento aplicado": tratamiento,
            "Variable derivada": derivada,
            "Fecha de extraccion": fecha_extraccion,
            "Fuente": FUENTE,
            "Version del conjunto limpio": version,
        })
    return entradas


def exportar_markdown(entradas, path):
    lineas = ["# Libro de codigos", ""]
    for entrada in entradas:
        lineas.extend([f"## {entrada['Variable']}", ""])
        for campo, valor in entrada.items():
            if campo != "Variable":
                valor_md = str(valor).replace("|", "\\|")
                lineas.append(f"- **{campo}:** {valor_md}")
        lineas.append("")
    Path(path).write_text("\n".join(lineas), encoding="utf-8")


def exportar_pdf(entradas, path):
    estilos = getSampleStyleSheet()
    elementos = [Paragraph("Libro de codigos", estilos["Title"]), Spacer(1, 0.2 * inch)]
    for entrada in entradas:
        encabezado = Paragraph(html.escape(entrada["Variable"]), estilos["Heading2"])
        primer_campo = None
        campos_restantes = []
        for campo, valor in entrada.items():
            if campo != "Variable":
                parrafo = Paragraph(
                    f"<b>{html.escape(campo)}:</b> {html.escape(str(valor))}",
                    estilos["BodyText"],
                )
                if primer_campo is None:
                    primer_campo = parrafo
                else:
                    campos_restantes.extend([parrafo, Spacer(1, 0.05 * inch)])
        elementos.append(KeepTogether([encabezado, primer_campo]))
        elementos.extend(campos_restantes)
        elementos.append(Spacer(1, 0.18 * inch))
    SimpleDocTemplate(str(path), pagesize=letter, rightMargin=36, leftMargin=36,
                      topMargin=36, bottomMargin=36).build(elementos)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default="data/limpio/establecimientos_educativos_limpio.csv")
    parser.add_argument("--fecha-extraccion", required=True, help="Fecha ISO YYYY-MM-DD")
    parser.add_argument("--version", required=True, help="Version del conjunto limpio")
    parser.add_argument("--markdown", default="reports/libro_codigos.md")
    parser.add_argument("--pdf", default="reports/libro_codigos.pdf")
    return parser.parse_args()


def main():
    args = parse_args()
    date.fromisoformat(args.fecha_extraccion)
    df = cargar_dataset(args.csv)
    entradas = construir_entradas(df, args.fecha_extraccion, args.version)
    markdown_path = Path(args.markdown)
    pdf_path = Path(args.pdf)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    exportar_markdown(entradas, markdown_path)
    exportar_pdf(entradas, pdf_path)
    print(f"Libro Markdown: {markdown_path.resolve()}")
    print(f"Libro PDF: {pdf_path.resolve()}")


if __name__ == "__main__":
    main()
