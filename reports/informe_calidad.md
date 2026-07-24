# Informe de calidad de los datos

## Comparacion antes y despues

| Metrica                             | Antes         | Despues         |
|:------------------------------------|:--------------|:----------------|
| Registros                           | 90425         | 90423           |
| Variables                           | 17            | 18              |
| Valores faltantes                   | 73988 (4.81%) | 163131 (10.02%) |
| Variables con NA                    | 6             | 8               |
| Duplicados exactos                  | 0             | 0               |
| Posibles duplicados                 | 14366         | 14359           |
| Variables con formato inconsistente | 7             | 0               |
| Variables con tipo incorrecto       | 0             | 0               |
| Categorias inconsistentes           | 0             | 0               |
| Errores corregidos                  | 0             | 37211           |

## Explicaciones

- Registros: cambio de 90425 a 90423; se excluyeron 2 registros con NIVEL fuera del recorrido hasta diversificado.
- Variables: cambio de 17 a 18 por la variable derivada ZONA.
- Posibles duplicados: 14359 grupos candidatos; conservados=14359, fusionados=0, corregidos=0. Patrones: RED_MISMO_NOMBRE_DISTINTA_DIRECCION=3298, REREGISTRO_ADMINISTRATIVO=11061.
- Errores corregidos: suma de registros afectados por regla; una fila puede contarse en mas de una regla.

## Pruebas automaticas

| Prueba                                           | Resultado   | Detalle                                                                                                                                    |
|:-------------------------------------------------|:------------|:-------------------------------------------------------------------------------------------------------------------------------------------|
| Sin duplicados exactos                           | OK          | 0                                                                                                                                          |
| Sin espacios iniciales o finales                 | OK          | 0                                                                                                                                          |
| Telefonos con formato uniforme                   | OK          | 0                                                                                                                                          |
| Departamentos dentro del catalogo                | OK          | []                                                                                                                                         |
| Municipios consistentes con la fuente            | OK          | []                                                                                                                                         |
| Variables con tipo esperado                      | OK          | []                                                                                                                                         |
| Sin categorias duplicadas por escritura          | OK          | {}                                                                                                                                         |
| Sin valores invalidos diagnosticados             | OK          | {'CODIGO': 0, 'DISTRITO': 0, 'DIRECTOR': 0, 'AREA': 0}                                                                                     |
| Zona consistente con Guatemala                   | OK          | 0                                                                                                                                          |
| Niveles dentro del recorrido hasta diversificado | OK          | ['BASICO', 'DIVERSIFICADO', 'INICIAL', 'PARVULOS', 'PARVULOS Y PREP. BILINGUE', 'PREPRIMARIA BILINGUE', 'PRIMARIA', 'PRIMARIA DE ADULTOS'] |

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
