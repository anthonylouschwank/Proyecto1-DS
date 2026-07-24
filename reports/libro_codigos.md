# Libro de codigos

## CODIGO

- **Descripcion:** Identificador unico del registro educativo.
- **Tipo de dato:** Texto
- **Dominio permitido:** Patron NN-NN-NNNN-NN
- **Valores posibles:** 90423 valores no nulos observados; consultar el CSV. Faltantes: 0.
- **Tratamiento aplicado:** Se conserva sin cambios y se valida como llave unica.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## DISTRITO

- **Descripcion:** Codigo administrativo de distrito.
- **Tipo de dato:** Texto
- **Dominio permitido:** NN-NNN o NN-NN-NNNN; admite NA
- **Valores posibles:** 2237 valores no nulos observados; consultar el CSV. Faltantes: 10102.
- **Tratamiento aplicado:** Los codigos incompletos NN- se convierten a NA.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## DEPARTAMENTO

- **Descripcion:** Departamento de Guatemala.
- **Tipo de dato:** Texto categorico
- **Dominio permitido:** 22 departamentos oficiales
- **Valores posibles:** ALTA VERAPAZ, BAJA VERAPAZ, CHIMALTENANGO, CHIQUIMULA, EL PROGRESO, ESCUINTLA, GUATEMALA, HUEHUETENANGO, IZABAL, JALAPA, JUTIAPA, PETEN, QUETZALTENANGO, QUICHE, RETALHULEU, SACATEPEQUEZ, SAN MARCOS, SANTA ROSA, SOLOLA, SUCHITEPEQUEZ, TOTONICAPAN, ZACAPA. Faltantes: 0.
- **Tratamiento aplicado:** CIUDAD CAPITAL se unifica en GUATEMALA.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## MUNICIPIO

- **Descripcion:** Municipio del establecimiento.
- **Tipo de dato:** Texto categorico
- **Dominio permitido:** Catalogo oficial SEGEPLAN 2026
- **Valores posibles:** ACATENANGO, AGUA BLANCA, AGUACATAN, ALMOLONGA, ALOTENANGO, AMATITLAN, ANTIGUA GUATEMALA, ASUNCION MITA, ATESCATEMPA, AYUTLA, BARBERENA, CABAÑAS, CABRICAN, CAJOLA, CAMOTAN, CANILLA, CANTEL, CASILLAS, CATARINA, CHAHAL, CHAJUL, CHAMPERICO, CHIANTLA, CHICACAO, CHICAMAN, CHICHE, CHIMALTENANGO, CHINAUTLA, CHINIQUE, CHIQUIMULA, CHIQUIMULILLA, CHISEC, CHUARRANCHO, CIUDAD VIEJA, COATEPEQUE, COBAN, COLOMBA COSTA CUCA, COLOTENANGO, COMAPA, COMITANCILLO, CONCEPCION, CONCEPCION CHIQUIRICHAPA, CONCEPCION HUISTA, CONCEPCION LAS MINAS, CONCEPCION TUTUAPA, CONGUACO, CUBULCO, CUILAPA, CUILCO, CUNEN, CUYOTENANGO, DOLORES, EL ADELANTO, EL ASINTAL, EL CHAL, EL ESTOR, EL JICARO, EL PALMAR, EL PROGRESO, EL QUETZAL, EL TEJAR, EL TUMBADOR, ESCUINTLA, ESQUIPULAS, ESQUIPULAS PALO GORDO, ESTANZUELA, FLORES, FLORES COSTA CUCA, FRAIJANES, FRAY BARTOLOME DE LAS CASAS, GENOVA COSTA CUCA, GRANADOS, GUALAN, GUANAGAZAPA, GUASTATOYA, GUATEMALA, GUAZACAPAN, HUEHUETENANGO, HUITAN, HUITE, IPALA, IXCAN, IXCHIGUAN, IZTAPA, JACALTENANGO, JALAPA, JALPATAGUA, JEREZ, JOCOTAN, JOCOTENANGO, JOYABAJ, JUTIAPA, LA BLANCA, LA DEMOCRACIA, LA ESPERANZA, LA GOMERA, LA LIBERTAD, LA REFORMA, LA TINTA, LA UNION, LANQUIN, LAS CRUCES, LIVINGSTON, LOS AMATES, MAGDALENA MILPAS ALTAS, MALACATAN, MALACATANCITO, MASAGUA, MATAQUESCUINTLA, MAZATENANGO, MELCHOR DE MENCOS, MIXCO, MOMOSTENANGO, MONJAS, MORALES, MORAZAN, MOYUTA, NAHUALA, NEBAJ, NENTON, NUEVA CONCEPCION, NUEVA SANTA ROSA, NUEVO PROGRESO, NUEVO SAN CARLOS, OCOS, OLINTEPEQUE, OLOPA, ORATORIO, PACHALUN, PAJAPITA, PALENCIA, PALESTINA DE LOS ALTOS, PALIN, PANAJACHEL, PANZOS, PARRAMOS, PASACO, PASTORES, PATULUL, PATZICIA, PATZITE, PATZUN, PETATAN, PLAYA GRANDE, POPTUN, PUEBLO NUEVO, PUEBLO NUEVO VIÑAS, PUERTO BARRIOS, PURULHA, QUESADA, QUETZALTENANGO, QUEZALTEPEQUE, RABINAL, RAXRUHA, RETALHULEU, RIO BLANCO, RIO BRAVO, RIO HONDO, SACAPULAS, SALAMA, SALCAJA, SAMAYAC, SAN AGUSTIN ACASAGUASTLAN, SAN ANDRES, SAN ANDRES ITZAPA, SAN ANDRES SAJCABAJA, SAN ANDRES SEMETABAJ, SAN ANDRES VILLA SECA, SAN ANDRES XECUL, SAN ANTONIO AGUAS CALIENTES, SAN ANTONIO HUISTA, SAN ANTONIO ILOTENANGO, SAN ANTONIO LA PAZ, SAN ANTONIO PALOPO, SAN ANTONIO SACATEPEQUEZ, SAN ANTONIO SUCHITEPEQUEZ, SAN BARTOLO AGUAS CALIENTES, SAN BARTOLOME JOCOTENANGO, SAN BARTOLOME MILPAS ALTAS, SAN BENITO, SAN BERNARDINO, SAN CARLOS ALZATATE, SAN CARLOS SIJA, SAN CRISTOBAL ACASAGUASTLAN, SAN CRISTOBAL CUCHO, SAN CRISTOBAL TOTONICAPAN, SAN CRISTOBAL VERAPAZ, SAN DIEGO, SAN FELIPE, SAN FRANCISCO, SAN FRANCISCO EL ALTO, SAN FRANCISCO LA UNION, SAN FRANCISCO ZAPOTITLAN, SAN GABRIEL, SAN GASPAR IXCHIL, SAN ILDEFONSO IXTAHUACAN, SAN JACINTO, SAN JERONIMO, SAN JORGE, SAN JOSE, SAN JOSE ACATEMPA, SAN JOSE CHACAYA, SAN JOSE DEL GOLFO, SAN JOSE EL IDOLO, SAN JOSE EL RODEO, SAN JOSE LA ARADA, SAN JOSE LA MAQUINA, SAN JOSE OJETENAM, SAN JOSE PINULA, SAN JOSE POAQUIL, SAN JUAN ATITAN, SAN JUAN BAUTISTA, SAN JUAN CHAMELCO, SAN JUAN COMALAPA, SAN JUAN COTZAL, SAN JUAN ERMITA, SAN JUAN IXCOY, SAN JUAN LA LAGUNA, SAN JUAN OSTUNCALCO, SAN JUAN SACATEPEQUEZ, SAN JUAN TECUACO, SAN LORENZO, SAN LUCAS SACATEPEQUEZ, SAN LUCAS TOLIMAN, SAN LUIS, SAN LUIS JILOTEPEQUE, SAN MANUEL CHAPARRON, SAN MARCOS, SAN MARCOS LA LAGUNA, SAN MARTIN JILOTEPEQUE, SAN MARTIN SACATEPEQUEZ, SAN MARTIN ZAPOTITLAN, SAN MATEO, SAN MATEO IXTATAN, SAN MIGUEL ACATAN, SAN MIGUEL CHICAJ, SAN MIGUEL DUENAS, SAN MIGUEL IXTAHUACAN, SAN MIGUEL PANAM, SAN MIGUEL PETAPA, SAN MIGUEL POCHUTA, SAN MIGUEL SIGUILA, SAN MIGUEL TUCURU, SAN MIGUEL USPANTAN, SAN PABLO, SAN PABLO JOCOPILAS, SAN PABLO LA LAGUNA, SAN PEDRO AYAMPUC, SAN PEDRO CARCHA, SAN PEDRO JOCOPILAS, SAN PEDRO LA LAGUNA, SAN PEDRO NECTA, SAN PEDRO PINULA, SAN PEDRO SACATEPEQUEZ, SAN PEDRO SOLOMA, SAN PEDRO YEPOCAPA, SAN RAFAEL LA INDEPENDENCIA, SAN RAFAEL LAS FLORES, SAN RAFAEL PETZAL, SAN RAFAEL PIE DE LA CUESTA, SAN RAYMUNDO, SAN SEBASTIAN, SAN SEBASTIAN COATAN, SAN SEBASTIAN HUEHUETENANGO, SAN VICENTE PACAYA, SANARATE, SANSARE, SANTA ANA, SANTA ANA HUISTA, SANTA APOLONIA, SANTA BARBARA, SANTA CATARINA BARAHONA, SANTA CATARINA IXTAHUACAN, SANTA CATARINA MITA, SANTA CATARINA PALOPO, SANTA CATARINA PINULA, SANTA CLARA LA LAGUNA, SANTA CRUZ BALANYA, SANTA CRUZ BARILLAS, SANTA CRUZ DEL QUICHE, SANTA CRUZ EL CHOL, SANTA CRUZ LA LAGUNA, SANTA CRUZ MULUA, SANTA CRUZ NARANJO, SANTA CRUZ VERAPAZ, SANTA EULALIA, SANTA LUCIA COTZUMALGUAPA, SANTA LUCIA LA REFORMA, SANTA LUCIA MILPAS ALTAS, SANTA LUCIA UTATLAN, SANTA MARIA CAHABON, SANTA MARIA CHIQUIMULA, SANTA MARIA DE JESUS, SANTA MARIA IXHUATAN, SANTA MARIA VISITACION, SANTA ROSA DE LIMA, SANTIAGO ATITLAN, SANTIAGO CHIMALTENANGO, SANTIAGO SACATEPEQUEZ, SANTO DOMINGO SUCHITEPEQUEZ, SANTO DOMINGO XENACOJ, SANTO TOMAS CHICHICASTENANGO, SANTO TOMAS LA UNION, SAYAXCHE, SENAHU, SIBILIA, SIBINAL, SIPACAPA, SIPACATE, SIQUINALA, SOLOLA, SUMPANGO, TACANA, TACTIC, TAJUMULCO, TAMAHU, TAXISCO, TECPAN GUATEMALA, TECTITAN, TECULUTAN, TEJUTLA, TIQUISATE, TODOS SANTOS CUCHUMATAN, TOTONICAPAN, UNION CANTINIL, USUMATLAN, VILLA CANALES, VILLA NUEVA, YUPILTEPEQUE, ZACAPA, ZACUALPA, ZAPOTITLAN, ZARAGOZA, ZUNIL, ZUNILITO. Faltantes: 0.
- **Tratamiento aplicado:** Las zonas de Ciudad Capital se asignan al municipio GUATEMALA.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## ZONA

- **Descripcion:** Zona de Ciudad de Guatemala cuando aplica.
- **Tipo de dato:** Texto
- **Dominio permitido:** Numero de zona o NA
- **Valores posibles:** 1, 2, 3, 4, 5, 6, 7. Faltantes: 86515.
- **Tratamiento aplicado:** Se extrae del MUNICIPIO original antes de unificar Ciudad Capital.
- **Variable derivada:** Si: derivada
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## ESTABLECIMIENTO

- **Descripcion:** Nombre del establecimiento educativo.
- **Tipo de dato:** Texto libre
- **Dominio permitido:** Texto o NA
- **Valores posibles:** 19636 valores no nulos observados; consultar el CSV. Faltantes: 13.
- **Tratamiento aplicado:** Se recortan y colapsan espacios; se conserva la escritura original.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## DIRECCION

- **Descripcion:** Direccion reportada del establecimiento.
- **Tipo de dato:** Texto libre
- **Dominio permitido:** Texto o NA
- **Valores posibles:** 41593 valores no nulos observados; consultar el CSV. Faltantes: 829.
- **Tratamiento aplicado:** Se recortan y colapsan espacios.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## TELEFONO

- **Descripcion:** Telefono principal reportado.
- **Tipo de dato:** Texto
- **Dominio permitido:** Ocho digitos o NA
- **Valores posibles:** 34919 valores no nulos observados; consultar el CSV. Faltantes: 27201.
- **Tratamiento aplicado:** Se conserva el primer numero completo de ocho digitos; lo ambiguo pasa a NA.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## SUPERVISOR

- **Descripcion:** Persona o entidad supervisora.
- **Tipo de dato:** Texto libre
- **Dominio permitido:** Texto o NA
- **Valores posibles:** 1622 valores no nulos observados; consultar el CSV. Faltantes: 10039.
- **Tratamiento aplicado:** Se recortan y colapsan espacios.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## DIRECTOR

- **Descripcion:** Nombre de la persona directora.
- **Tipo de dato:** Texto libre
- **Dominio permitido:** Texto o NA
- **Valores posibles:** 34610 valores no nulos observados; consultar el CSV. Faltantes: 28427.
- **Tratamiento aplicado:** Se normalizan espacios y placeholders de faltante a NA.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## NIVEL

- **Descripcion:** Nivel escolar del establecimiento.
- **Tipo de dato:** Texto categorico
- **Dominio permitido:** Niveles educativos desde inicial hasta diversificado
- **Valores posibles:** BASICO, DIVERSIFICADO, INICIAL, PARVULOS, PARVULOS Y PREP. BILINGUE, PREPRIMARIA BILINGUE, PRIMARIA, PRIMARIA DE ADULTOS. Faltantes: 0.
- **Tratamiento aplicado:** Se excluyen categorias fuera del recorrido educativo definido.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## SECTOR

- **Descripcion:** Sector administrativo.
- **Tipo de dato:** Texto categorico
- **Dominio permitido:** OFICIAL, PRIVADO, MUNICIPAL o COOPERATIVA
- **Valores posibles:** COOPERATIVA, MUNICIPAL, OFICIAL, PRIVADO. Faltantes: 0.
- **Tratamiento aplicado:** Se conserva y valida contra su dominio.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## AREA

- **Descripcion:** Area geografica.
- **Tipo de dato:** Texto categorico
- **Dominio permitido:** URBANA, RURAL o NA
- **Valores posibles:** RURAL, URBANA. Faltantes: 5.
- **Tratamiento aplicado:** SIN ESPECIFICAR se convierte a NA.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## STATUS

- **Descripcion:** Estado administrativo del registro.
- **Tipo de dato:** Texto categorico
- **Dominio permitido:** Categorias observadas en la fuente
- **Valores posibles:** ABIERTA, CERRADA DEFINITIVAMENTE, CERRADA TEMPORALMENTE, TEMPORAL CONTRATO 021, TEMPORAL NOMBRAMIENTO, TEMPORAL TITULOS. Faltantes: 0.
- **Tratamiento aplicado:** Se conserva sin cambios.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## MODALIDAD

- **Descripcion:** Modalidad linguistica.
- **Tipo de dato:** Texto categorico
- **Dominio permitido:** MONOLINGUE o BILINGUE
- **Valores posibles:** BILINGUE, MONOLINGUE. Faltantes: 0.
- **Tratamiento aplicado:** Se conserva y valida contra su dominio.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## JORNADA

- **Descripcion:** Jornada educativa.
- **Tipo de dato:** Texto categorico
- **Dominio permitido:** Categorias observadas en la fuente
- **Valores posibles:** DOBLE, INTERMEDIA, MATUTINA, NOCTURNA, SIN JORNADA, VESPERTINA. Faltantes: 0.
- **Tratamiento aplicado:** Se conserva sin cambios.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## PLAN

- **Descripcion:** Plan de estudios o asistencia.
- **Tipo de dato:** Texto categorico
- **Dominio permitido:** Categorias observadas en la fuente
- **Valores posibles:** A DISTANCIA, DIARIO(REGULAR), DOMINICAL, FIN DE SEMANA, INTERCALADO, IRREGULAR, MIXTO, SABATINO, SEMIPRESENCIAL, SEMIPRESENCIAL (DOS DÍAS A LA SEMANA), SEMIPRESENCIAL (FIN DE SEMANA), SEMIPRESENCIAL (UN DÍA A LA SEMANA), VIRTUAL A DISTANCIA. Faltantes: 0.
- **Tratamiento aplicado:** Se conserva sin cambios.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1

## DEPARTAMENTAL

- **Descripcion:** Oficina departamental de educacion responsable.
- **Tipo de dato:** Texto categorico
- **Dominio permitido:** Categorias observadas en la fuente
- **Valores posibles:** ALTA VERAPAZ, BAJA VERAPAZ, CHIMALTENANGO, CHIQUIMULA, EL PROGRESO, ESCUINTLA, GUATEMALA NORTE, GUATEMALA OCCIDENTE, GUATEMALA ORIENTE, GUATEMALA SUR, HUEHUETENANGO, IZABAL, JALAPA, JUTIAPA, PETÉN, QUETZALTENANGO, QUICHÉ, QUICHÉ NORTE, RETALHULEU, SACATEPÉQUEZ, SAN MARCOS, SANTA ROSA, SOLOLÁ, SUCHITEPÉQUEZ, TOTONICAPÁN, ZACAPA. Faltantes: 0.
- **Tratamiento aplicado:** Se conserva sin cambios.
- **Variable derivada:** No
- **Fecha de extraccion:** 2026-07-23
- **Fuente:** MINEDUC - BUSCAESTABLECIMIENTO_GE (http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/)
- **Version del conjunto limpio:** 1.0.1
