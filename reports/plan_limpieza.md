# Plan de limpieza

Basado en `reports/diagnostico_datos_crudos.md` (generado por `04_diagnostico.py`
sobre la union de los 23 CSV crudos, 94,533 registros x 17 variables).

Regla transversal (aplica a ESTABLECIMIENTO, DIRECCION, SUPERVISOR, DIRECTOR):
**no se modifica la ortografia, tildes, ñ ni mayusculas/minusculas originales
del texto**, tal como pidio el profesor, porque quien use el dataset despues
debe poder citar estos nombres en informes tal como estan escritos
oficialmente. Solo se corrigen problemas puramente de *formato* (espacios
dobles, valores que en realidad significan "sin dato" pero se capturaron como
texto).

---

## CODIGO

**Problemas encontrados:** ninguno. 0% faltantes, 100% cumple el patron
`NN-NN-NNNN-NN`, 94,533 valores unicos = 94,533 filas (es llave unica).

**Regla:** mantener tal cual, como texto (no convertir a numero: tiene ceros
a la izquierda y guiones). Usar como llave primaria del dataset limpio.

**Por que funcionara:** ya cumple el 100% del formato esperado, no hay nada
que corregir.

**Riesgos:** ninguno. Unico chequeo pendiente: reconfirmar unicidad de
CODIGO despues de la union final de los 23 archivos (ya verificado: se
mantiene unica).

---

## DISTRITO

**Problemas encontrados:** 11.31% faltante. Dos formatos de codigo distintos
conviven (`NN-NN-NNNN` en 54,911 filas y `NN-NNN` en 28,849 filas), y 79
filas con un formato incompleto (`NN-`, sin digitos despues).

**Regla:** no forzar un unico formato porque no hay certeza de que ambos
esquemas signifiquen lo mismo (posiblemente corresponden a una
reestructuracion administrativa de distritos en distintos anios). Se deja el
valor tal cual y se documentan ambos formatos como validos en el libro de
codigos. Los 79 casos con formato incompleto (`NN-` sin nada mas) se
convierten a NaN explicito porque no aportan informacion utilizable.

**Por que funcionara:** evita inventar una normalizacion sin base solida
(riesgo de introducir informacion falsa), y resuelve el unico caso
verdaderamente vacio de contenido (el `NN-` incompleto).

**Riesgos:** dejar dos formatos sin unificar puede complicar un join futuro
contra otra fuente que use un solo esquema de distrito; se documenta
explicitamente para que el proximo analista lo sepa de antemano.

---

## DEPARTAMENTO

**Problemas encontrados:** el dropdown de origen separa "CIUDAD CAPITAL"
(value=00) de "GUATEMALA" (value=01), pero administrativamente Ciudad
Capital *es* el municipio "Guatemala" del departamento Guatemala. Guatemala
tiene oficialmente 22 departamentos, no 23. Se verifico que no hay
solapamiento de CODIGO entre ambos grupos (0 interseccion), asi que no es un
duplicado de datos, es una particion administrativa del sitio web.

**Regla:** para el dataset limpio, unificar `CIUDAD CAPITAL` dentro de
`DEPARTAMENTO = GUATEMALA` (fijando tambien `MUNICIPIO = GUATEMALA` para
esas filas, ver seccion MUNICIPIO). Se documenta explicitamente esta
decision en el libro de codigos.

**Por que funcionara:** deja el dataset final alineado con la division
politico-administrativa oficial de Guatemala (22 departamentos), evitando
que alguien cuente "23 departamentos" por error al agrupar.

**Riesgos:** se pierde la distincion "capital vs resto del departamento
Guatemala" como variable de primer nivel, lo cual puede ser util
analiticamente (la capital tiene un perfil urbano muy distinto al resto del
departamento). Se mitiga dejando la zona capitalina visible en MUNICIPIO/
DIRECCION en vez de borrarla.

---

## MUNICIPIO

**Problemas encontrados:** 0% faltante, 357 valores. Bajo el grupo "CIUDAD
CAPITAL" del sitio, esta columna trae `ZONA 1` ... `ZONA 25` en vez de un
municipio real.

**Regla:** al aplicar la unificacion de CIUDAD CAPITAL -> GUATEMALA (ver
DEPARTAMENTO), reemplazar esas 7,594 filas con `MUNICIPIO = GUATEMALA`. La
zona (1-25) no se descarta: se verifico que solo el 16% de esas filas
menciona "ZONA" dentro de DIRECCION, asi que no es seguro depender de ese
texto libre. En su lugar se agrega una columna nueva `ZONA` (numero de zona,
solo poblada para las filas que antes eran Ciudad Capital, NaN para el
resto) extraida directamente del valor original de MUNICIPIO antes de
sobreescribirlo.

**Por que funcionara:** el dataset queda con municipios reales y
consistentes con el resto del pais, sin perder la informacion de zona
capitalina (se verifico que la extraccion captura el 100% de los casos,
0 zonas sin capturar).

**Riesgos:** minimo. `ZONA` es una columna nueva que no existia en el
formulario original del sitio, hay que documentarla claramente en el libro
de codigos para que no se confunda con una variable oficial de MINEDUC.

---

## ESTABLECIMIENTO

**Problemas encontrados:** 0.02% faltante (15 filas). 4,675 filas con
espacios dobles internos. Sin problemas de ortografia/encoding reales (se
verifico que los caracteres que se ven raros en consola son solo limitacion
de la fuente de la terminal, no del dato).

**Regla:** **no tocar ortografia, tildes, mayusculas ni signos**. Unica
transformacion: colapsar espacios internos multiples a uno solo
(`re.sub(r'\s+', ' ', texto)`), que es un problema de formato, no de
contenido. Los 15 registros sin nombre quedan como NaN (no se inventa un
nombre).

**Por que funcionara:** corrige el unico problema real de formato sin tocar
el contenido textual que debe permanecer intacto para reportes.

**Riesgos:** minimo. Teoricamente un nombre podria usar doble espacio a
proposito (extremadamente improbable en nombres de establecimientos
educativos), asi que el riesgo de alterar contenido legitimo es muy bajo.

---

## DIRECCION

**Problemas encontrados:** 0.91% faltante. 2,163 filas con espacios dobles
internos. 77 filas con minusculas (legitimas, ej. abreviaturas como "km",
no error de captura).

**Regla:** igual que ESTABLECIMIENTO: solo colapsar espacios multiples,
mantener el resto intacto.

**Por que funcionara:** mismo razonamiento que ESTABLECIMIENTO.

**Riesgos:** minimo, mismo caso que ESTABLECIMIENTO.

---

## TELEFONO

**Problemas encontrados:** 29.10% faltante (ya NaN). Ademas: 792 filas con
mas de un numero separados por "/" o "-" (o texto como "CEL. ..."); 138
filas solo con digitos pero longitud distinta de 8 (Guatemala usa 8 digitos);
133 filas con el valor literal `S/D`; un puñado de valores de 1-3 digitos que
son placeholders de captura, no telefonos.

**Regla:**
1. `S/D` y variantes equivalentes de "sin dato" -> NaN.
2. Para valores con multiples numeros: extraer el primer numero de 8 digitos
   valido como `TELEFONO` principal (se documenta que solo se conserva el
   primero).
3. Para valores solo-digitos con longitud != 8 -> NaN (no se completa ni se
   trunca, porque no hay forma confiable de saber que digito falta o sobra).
4. El resto (numeros ya de 8 digitos limpios) se deja igual.

**Por que funcionara:** deja la columna en un formato uniforme (8 digitos o
NaN), utilizable directamente para validacion o contacto, sin adivinar
digitos que no estan.

**Riesgos:** se pierde el segundo numero en los casos con multiples
telefonos, y se pierde por completo cualquier numero con longitud incorrecta
que en realidad tuviera un solo digito mal capturado (podria haberse
recuperado con mas contexto, pero se prefiere ser conservador y no adivinar).

---

## SUPERVISOR

**Problemas encontrados:** 11.32% faltante. 318 filas con espacios dobles.
Valores como "PROYECTO HUN BARAHONA", "PROYECTO FUNDAZUCAR" son legitimos
(programas/entidades que ejercen supervision institucional, no un error de
captura de nombre de persona).

**Regla:** igual que ESTABLECIMIENTO/DIRECCION: solo colapsar espacios
dobles, sin tocar el contenido ni intentar "corregir" los valores tipo
"PROYECTO ...".

**Por que funcionara:** respeta que esta columna mezcla personas y entidades
de forma legitima segun como opera MINEDUC.

**Riesgos:** minimo.

---

## DIRECTOR

**Problemas encontrados:** 29.34% faltante (NaN). Ademas, 2,180 filas
adicionales usan placeholders de texto distintos para decir "sin dato"
(`-`, `--`, `---`, `----`, `-----`, `.`, `S/D`, `SIN DATO`), lo que infla el
conteo de valores unicos y esconde el verdadero porcentaje de informacion
faltante. 9,502 filas con espacios dobles internos.

**Regla:** homologar todos los placeholders de la lista anterior a NaN
explicito. Para los nombres reales, solo colapsar espacios dobles, sin tocar
ortografia/tildes.

**Por que funcionara:** revela el porcentaje real de faltantes
(29.34% + 2180/94533 ≈ 31.7%) en vez de contar placeholders como si fueran
nombres validos, y mejora la calidad del conteo de valores unicos.

**Riesgos:** si algun placeholder corto (ej. ".") fuera parte legitima de un
nombre truncado, se perderia como faltante; se recomienda revisar una
muestra antes de aplicar esta regla en el dataset final.

---

## NIVEL

**Problemas encontrados:** 0% faltante, 10 valores observados (el dropdown
del sitio solo ofrecia 6 como filtro). Hay 3 filas fuera del alcance del
proyecto: 1 `UNIVERSIDAD` y 2 `ADMINISTRATIVOS`, que no son niveles
educativos hasta diversificado.

**Regla:** excluir (eliminar) las 3 filas con `NIVEL` en
`{UNIVERSIDAD, ADMINISTRATIVOS}`, porque el alcance definido por el proyecto
es explicitamente "hasta el nivel de diversificado". Mantener `INICIAL` y
`PARVULOS Y PREP. BILINGUE` como categorias validas (son niveles
pre-primarios reales, no errores) y documentarlas en el libro de codigos.

**Por que funcionara:** ajusta el dataset al alcance pedido sin tocar
categorias legitimas que simplemente no aparecian en el dropdown de filtro.

**Riesgos:** perdida de 3 registros (impacto insignificante sobre 94,533),
pero debe quedar documentado por que se excluyen para que el proceso sea
auditable.

---

## SECTOR

**Problemas encontrados:** ninguno. 0% faltante, 4 valores, los 4 dentro del
dominio esperado (OFICIAL, PRIVADO, MUNICIPAL, COOPERATIVA).

**Regla:** sin cambios. Documentar en el libro de codigos.

**Riesgos:** ninguno.

---

## AREA

**Problemas encontrados:** 0% faltante, pero 8 filas tienen `SIN ESPECIFICAR`,
fuera del dominio esperado (URBANA/RURAL).

**Regla:** convertir `SIN ESPECIFICAR` a NaN explicito: semanticamente es un
dato faltante, no una tercera categoria geografica real.

**Por que funcionara:** el dominio queda limpio en 2 categorias reales mas
NaN, en vez de una pseudo-categoria de "no se sabe".

**Riesgos:** minimo, solo 8 filas afectadas.

---

## STATUS

**Problemas encontrados:** 0% faltante, 6 valores, todos parecen estados
administrativos legitimos (ABIERTA, CERRADA DEFINITIVAMENTE, CERRADA
TEMPORALMENTE, TEMPORAL NOMBRAMIENTO, TEMPORAL TITULOS, TEMPORAL CONTRATO
021).

**Regla:** sin cambios de valores. Documentar el significado de cada estado
en el libro de codigos, con una nota de advertencia: cualquier conteo de
"numero de establecimientos activos" debe filtrar por `STATUS = ABIERTA`.

**Riesgos:** el riesgo no esta en la variable sino en su mal uso posterior
(sobreconteo de escuelas activas si no se filtra); se mitiga con
documentacion explicita, no con una transformacion de los datos.

---

## MODALIDAD

**Problemas encontrados:** ninguno. 0% faltante, 2 valores, ambos dentro de
dominio (MONOLINGUE, BILINGUE).

**Regla:** sin cambios. Documentar en el libro de codigos.

**Riesgos:** ninguno.

---

## JORNADA

**Problemas encontrados:** 0% faltante, 6 valores (MATUTINA, VESPERTINA,
DOBLE, SIN JORNADA, NOCTURNA, INTERMEDIA). `SIN JORNADA` podria confundirse
con un faltante.

**Regla:** mantener `SIN JORNADA` como categoria valida (no convertir a NaN),
porque es coherente con establecimientos de PLAN `A DISTANCIA` o `VIRTUAL A
DISTANCIA`, donde no aplica una jornada fija. Documentar explicitamente en
el libro de codigos.

**Por que funcionara:** evita perder informacion real disfrazandola de dato
faltante.

**Riesgos:** si en la practica algunos de esos casos si fueran un dato no
capturado (y no una ausencia real de jornada), se estaria tratando como
categoria valida algo que deberia ser NaN; se documenta la ambiguedad.

---

## PLAN

**Problemas encontrados:** 0% faltante, 13 valores. Se verifico que no hay
problema real de encoding (las tildes estan correctamente codificadas en
UTF-8; lo que parecia un caracter roto en la consola era solo una limitacion
de fuente del terminal). Existen 4 variantes de "SEMIPRESENCIAL" (general,
fin de semana, un dia, dos dias a la semana).

**Regla:** sin cambios de contenido. Documentar las 13 categorias en el
libro de codigos, dejando explicito que las variantes de SEMIPRESENCIAL se
mantienen separadas (no se agrupan) para no perder detalle.

**Riesgos:** ninguno al dejarlas intactas.

---

## DEPARTAMENTAL

**Problemas encontrados:** 0% faltante, 26 valores (oficinas departamentales
de educacion; no necesariamente coincide 1 a 1 con DEPARTAMENTO por
reorganizaciones administrativas del ministerio).

**Regla:** sin cambios. Documentar como variable administrativa categorica
en el libro de codigos.

**Riesgos:** ninguno.

---

## Transversal: duplicados y union final

**Problemas encontrados:** 0 duplicados exactos. Sin embargo, 4,380 filas
comparten ESTABLECIMIENTO + DIRECCION + MUNICIPIO + NIVEL + JORNADA + SECTOR
con un CODIGO distinto, y casi siempre un STATUS distinto (una fila ABIERTA,
otra CERRADA/historica). Esto sugiere re-registro administrativo del mismo
establecimiento fisico bajo un CODIGO nuevo con el paso del tiempo, no un
error de captura.

**Regla:** no eliminar estas filas (cada CODIGO es un registro
administrativo legitimo con su propio historial de STATUS). Se documentan en
el libro de codigos con una advertencia explicita: un mismo establecimiento
fisico puede aparecer con mas de un CODIGO a lo largo de los anios, por lo
que cualquier conteo de "numero de escuelas" debe filtrar primero por
`STATUS = ABIERTA`.

**Por que funcionara:** preserva la trazabilidad historica completa del
dataset (que es justamente lo que MINEDUC registra), en vez de borrar
informacion basandose en una suposicion no verificada de que son errores.

**Riesgos:** si un analista no lee la documentacion y suma filas sin filtrar
STATUS, sobreestimara el numero real de establecimientos activos. Mitigado
con la advertencia explicita en el libro de codigos.

Al unir los 23 CSV de `data/crudo/` en un solo dataset, se revalida que
CODIGO siga siendo unico (ya verificado: 94,533 codigos unicos = 94,533
filas, ninguna colision entre departamentos).
