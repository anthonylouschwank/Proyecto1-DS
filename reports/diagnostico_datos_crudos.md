# Diagnostico del estado inicial de los datos crudos

Fuente: 23 archivos CSV crudos en `data/crudo/` (uno por departamento, sin ninguna limpieza aplicada).

## 1. Numero de registros y variables

Numero de registros: **94533**

Numero de variables: **17**

## 2. Tipo de dato de cada variable

|    | variable        | tipo_pandas   | tipo_logico                  |
|---:|:----------------|:--------------|:-----------------------------|
|  0 | CODIGO          | str           | identificador/codigo         |
|  1 | DISTRITO        | str           | identificador/codigo         |
|  2 | DEPARTAMENTO    | str           | categorica                   |
|  3 | MUNICIPIO       | str           | categorica                   |
|  4 | ESTABLECIMIENTO | str           | texto libre                  |
|  5 | DIRECCION       | str           | texto libre                  |
|  6 | TELEFONO        | str           | telefono (texto con formato) |
|  7 | SUPERVISOR      | str           | texto libre                  |
|  8 | DIRECTOR        | str           | texto libre                  |
|  9 | NIVEL           | str           | categorica                   |
| 10 | SECTOR          | str           | categorica                   |
| 11 | AREA            | str           | categorica                   |
| 12 | STATUS          | str           | categorica                   |
| 13 | MODALIDAD       | str           | categorica                   |
| 14 | JORNADA         | str           | categorica                   |
| 15 | PLAN            | str           | categorica                   |
| 16 | DEPARTAMENTAL   | str           | categorica                   |

Nota: pandas carga todas las columnas como texto (`str`) porque el scraper las guarda como texto (CODIGO, TELEFONO y DISTRITO parecen numericos pero tienen ceros a la izquierda / separadores, asi que deben quedarse como texto). No hay ninguna variable numerica continua en el dataset.

## 3. Valores faltantes por variable

|                 |   faltantes_NaN |   pct_NaN |   cadenas_vacias_incl_NaN |
|:----------------|----------------:|----------:|--------------------------:|
| CODIGO          |               0 |      0    |                         0 |
| DISTRITO        |           10694 |     11.31 |                     10694 |
| DEPARTAMENTO    |               0 |      0    |                         0 |
| MUNICIPIO       |               0 |      0    |                         0 |
| ESTABLECIMIENTO |              15 |      0.02 |                        15 |
| DIRECCION       |             863 |      0.91 |                       863 |
| TELEFONO        |           27513 |     29.1  |                     27513 |
| SUPERVISOR      |           10702 |     11.32 |                     10702 |
| DIRECTOR        |           27738 |     29.34 |                     27738 |
| NIVEL           |               0 |      0    |                         0 |
| SECTOR          |               0 |      0    |                         0 |
| AREA            |               0 |      0    |                         0 |
| STATUS          |               0 |      0    |                         0 |
| MODALIDAD       |               0 |      0    |                         0 |
| JORNADA         |               0 |      0    |                         0 |
| PLAN            |               0 |      0    |                         0 |
| DEPARTAMENTAL   |               0 |      0    |                         0 |

Nota: 'cadenas_vacias_incl_NaN' cuenta NaN + strings vacios/solo espacios; en este dataset coincide exactamente con los NaN, es decir, no hay strings vacios escondidos que pandas no haya detectado como faltantes al leer el CSV.

## 4. Cantidad de valores unicos por variable

|                 |   valores_unicos |
|:----------------|-----------------:|
| CODIGO          |            94533 |
| DISTRITO        |             2275 |
| DEPARTAMENTO    |               23 |
| MUNICIPIO       |              357 |
| ESTABLECIMIENTO |            22784 |
| DIRECCION       |            44489 |
| TELEFONO        |            36709 |
| SUPERVISOR      |             1639 |
| DIRECTOR        |            35951 |
| NIVEL           |               10 |
| SECTOR          |                4 |
| AREA            |                3 |
| STATUS          |                6 |
| MODALIDAD       |                2 |
| JORNADA         |                6 |
| PLAN            |               13 |
| DEPARTAMENTAL   |               26 |

## 5. Registros duplicados exactos

Duplicados exactos (todas las columnas iguales): **0**

Duplicados por CODIGO (deberia ser llave unica): **0**


## 6. Variables con valores fuera de dominio


**NIVEL** (dominio esperado segun el formulario del sitio):

| NIVEL                     |   valor |
|:--------------------------|--------:|
| INICIAL                   |    2167 |
| PARVULOS Y PREP. BILINGUE |       4 |
| ADMINISTRATIVOS           |       2 |
| UNIVERSIDAD               |       1 |

**SECTOR** (dominio esperado segun el formulario del sitio):

Sin valores fuera de dominio.


**MODALIDAD** (dominio esperado segun el formulario del sitio):

Sin valores fuera de dominio.


**AREA** (dominio esperado segun el formulario del sitio):

| AREA            |   valor |
|:----------------|--------:|
| SIN ESPECIFICAR |       8 |

## 7. Variables con formatos inconsistentes


**CODIGO fuera de patron NN-NN-NNNN-NN**

0

**TELEFONO con separadores (multiples numeros / texto)**

792

**TELEFONO solo digitos con longitud != 8**

138

**TELEFONO == 'S/D'**

133

**Espacios dobles internos (por columna)**

- ESTABLECIMIENTO: 4675
- DIRECCION: 2163
- SUPERVISOR: 318
- DIRECTOR: 9502

**DISTRITO: patrones de formato mas comunes (digitos -> #)**

| DISTRITO   |   valor |
|:-----------|--------:|
| ##-##-#### |   54911 |
| ##-###     |   28849 |
| ##-        |      79 |

**DIRECTOR con placeholder textual (-, S/D, SIN DATO, etc.)**

2180

## 8. Problemas potenciales de calidad de datos

1. GUATEMALA vs CIUDAD CAPITAL: son dos entradas separadas del dropdown de departamento (value='01' y value='00'); administrativamente Ciudad Capital es el municipio 'Guatemala' del departamento Guatemala. No hay solapamiento de CODIGO entre ambos (verificado), pero hay que decidir si se unifican o se mantienen separados antes de reportar totales por departamento.

2. 4380 filas comparten ESTABLECIMIENTO+DIRECCION+MUNICIPIO+NIVEL+JORNADA+SECTOR con un CODIGO distinto y, en la mayoria de los casos, un STATUS distinto (una fila ABIERTA y otra CERRADA/HISTORICA). Esto sugiere re-registro administrativo del mismo establecimiento con un CODIGO nuevo, no un duplicado exacto. Distribucion de STATUS en esas filas:
STATUS
ABIERTA                    2090
CERRADA DEFINITIVAMENTE    1239
CERRADA TEMPORALMENTE      1006
TEMPORAL NOMBRAMIENTO        41
TEMPORAL TITULOS              3
TEMPORAL CONTRATO 021         1

3. NIVEL contiene 3 registros fuera del alcance del proyecto (que pide datos hasta diversificado): 1 'UNIVERSIDAD' y 2 'ADMINISTRATIVOS'.

4. TELEFONO mezcla telefonos reales (8 digitos), valores con mas de un numero separados por '/' o '-', texto libre ('S/D', 'CEL. ...') y codigos muy cortos (1-3 digitos) que parecen placeholders de captura, no telefonos.

5. DIRECTOR usa distintos placeholders de texto para 'sin dato' en vez de dejar la celda vacia ('-', '--', '---', '.', 'S/D', 'SIN DATO'), lo que infla el conteo de 'valores unicos' y esconde el verdadero porcentaje de faltantes si no se homologan a NaN.

6. DISTRITO mezcla al menos dos formatos de codigo (NN-NNN y NN-NN-NNNN), posiblemente porque codifica cosas distintas segun el departamento/epoca.
