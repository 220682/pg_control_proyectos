# 02 - Prueba funcional del RDT con el servicio real PS-0001 (TECNET)

> Fecha de preparacion: 2026-10-19. Estado: PLAN de prueba, NO ejecutado. Preparado en solo lectura (sin tocar la app, la base de datos ni ningun repositorio de codigo).
> Servicio: PS-0001 OBRAS CIVILES PARA SISTEMA DETECCION CONTRAINCENDIOS (cliente TECNET; en el repo de planeamiento es PS-167-2026). Moneda: USD, solo costo directo (CD). Formato de numeros de este documento: 1,234.56.
> Etiquetas de procedencia: **[DOC]** = escrito en un flujo de `docs/04-flujos-de-negocio/`; **[APP]** = leido en el codigo de `py_control_proyectos_web` (solo lectura); **[CALC]** = calculado aqui a partir del presupuesto y del cronograma del servicio; **[NO DERIVABLE]** = no se pudo obtener sin consultar la base de datos o a Victor.
> Limite de la preparacion: la base de datos no estuvo disponible (los servidores MCP de PostgreSQL y planeamiento no conectaron), asi que todo lo que vive solo en la base (personal, `dp_moi`, tarifas congeladas, lineas reales del Plan Maestro, catalogo vigente) esta marcado como por confirmar.

## A. Mapa de funciones del RDT

### A.1 Pantallas y rutas

| Pantalla | Ruta | Que hace | Fuente |
|---|---|---|---|
| Crear RDT | `/rdts/crear` | Formulario PROM-GP-002 (matriz actividades x personas). Guarda un RDT en estado REGISTRADO o un borrador. | [DOC] 06 / [APP] `FormularioCrearRdt.tsx` |
| Status de RDT | `/rdts/status` | Seguimiento por estado; aqui se valida, rechaza, reasigna y corrige. | [DOC] 06 / [APP] `TablaStatusRdts.tsx` |
| Archivo de subidos | `/rdts/listado` | Archivo de RDT subidos como archivo; el borrado solo se hace aqui (administrador y jefe de proyectos). | [DOC] 06 |
| Consolidado | `/rdts/consolidado` | Consolidado de RDT por servicio. | [DOC] 06 / [APP] `TablaConsolidadoRdts.tsx` |
| Subir RDT (archivo) | Mi entorno `?accion=subir-rdt` | Alta de un RDT ya hecho en Excel. No se usa en esta prueba. | [DOC] 06 |
| Plan Maestro | `/proyectos/{id}/plan-maestro` (nombre exacto por confirmar) | Real vs Prog por clave `paquete|DIRECTA : partida`, semanas sabado a viernes. | [DOC] 20 |
| PR | `/proyectos/{id}/pr` | Reporte de proyecto: avance, EV, AC, HH, recursos, `recursos_sin_tarifa`. | [DOC] 10 / [APP] ruta existe |
| Dashboard | `/proyectos/{id}/dashboard` | KPIs, Pareto de CNC, PPC; version Parcial o Completa. | [DOC] 11 / [APP] ruta existe |
| Curva S | `/api/curva-s` (la ve el servicio en su panel) | Serie diaria, se muestra por semana sabado a viernes. | [DOC] 21 / [APP] `src/app/api/curva-s/route.ts` |
| Restricciones | dentro de Informes `/proyectos/{id}/informes` | Lista y estados Pendiente, Recepcionado, Atendido. | [DOC] 22 |
| Inasistencias | pestana de Informes | Consulta informativa por rango de fechas. | [DOC] 22 / [APP] `PestanaInasistencias.tsx` |
| Foto de campo | `/proyectos/{id}/informes/foto` | Banco de fotos JPEG hasta 3 MB, uso "Para partidas" o "Para restricciones". | [DOC] 22 / [APP] la pagina y `api/proyectos/[id]/fotos-campo` existen |
| Causas CNC | Recursos > Causas CNC | Catalogo mantenible `catalogo_cnc` (activo/inactivo). | [DOC] 06, 14 / [APP] `TablaCatalogoCnc.tsx` |

### A.2 Campos del formulario y de donde sale cada dato

| Seccion | Campo | Obligatorio | Fuente del dato |
|---|---|---|---|
| 1.0 Identificacion | N° OT (codigo del servicio) y cliente | si | Proyecto abierto; cliente viene del proyecto |
| 1.0 | Fecha | si | Selector `type=date` **sin maximo** [APP]; zona Lima |
| 1.0 | Turno (Dia / Noche) | si | Lista fija [APP] `TURNOS` |
| 1.0 | Especialidad (8 disciplinas) | si | Lista del flujo 06 (nombre exacto de la disciplina civil por confirmar en pantalla) |
| 1.0 | Ubicacion / area | si | Texto libre |
| 1.0 | Semana N° | si | Numero ingresado a mano |
| 1.0 | Partidas del DP (contador) y jornada laboral (h) | informativo / parametro | DP importado; la jornada fija cuanto es normal y cuanto es HH extra |
| 2.0 Reporte de avance | Actividad (selector del Plan Maestro aprobado) | si, minimo 1 | Lineas del Plan Maestro sin transversales [APP] `api/rdts/catalogos` |
| 2.0 | Descripcion, TA (D / C / NC), unidad | si | Texto; TA lista fija |
| 2.0 | Metrado programado | no (lo trae del Plan Maestro) | Plan Maestro aprobado, por dia |
| 2.0 | Metrado ejecutado | si en D | Lo escribe el supervisor; en paquete se declara solo la guia (2.3, ML) y el servidor reparte el mismo % |
| 2.0 | Restricciones (texto + fotos) | no | Texto crea siempre una restriccion `{N° OT}-RE-{n}`; fotos del banco "Para restricciones" (hasta 10) |
| 2.0 | CNC (causa) | si en D con ejecutado < programado | Catalogo `catalogo_cnc`, texto exacto |
| Tareo | Persona (DNI, nombre, cargo, especialidad) | minimo 1 con horas | Catalogo `recursos_personal` / cargos `recursos_cargos` |
| Tareo | Horas por actividad y horas extra | si | Escritas; las extra se valoran x 1.25 |
| Inasistencias (informativo) | Persona, DNI, motivo (Falta, Descanso medico, Permiso, Vacaciones, Otro), nota (max 500) | no | Texto; no suma horas ni costo |
| Equipos | Equipo, WBS (partida), HM, HM stand-by, estado (OPERATIVO, STAND_BY, AVERIADO, EN_MANTENIMIENTO) | HM > 0 y partida | `recursos_equipos` (solo unidad HM) |
| Materiales (informativo) | Descripcion, WBS, unidad, cantidad | no | Texto; **no se suma a ningun costo** [APP] |
| Observaciones | Texto | no | Texto libre |
| Acciones | Guardar borrador, plantillas, PDF borrador, Registrar | - | `rdt_borradores`; registrar borra el borrador coincidente |

Notas [APP] sobre el guardado: no existe un paso "enviar": registrar deja el RDT en REGISTRADO. Un solo RDT por N° OT + fecha + turno (si existe, el servidor responde 409 `PARTE_DUPLICADO`; reemplazar exige `motivoCorreccion` y no se puede reemplazar un VALIDADO). Crear exige Plan Maestro APROBADO y servicio en estado EJECUCION (400 `SERVICIO_NO_EN_EJECUCION`).

### A.3 Que existe y que no existe en el RDT

| Elemento | Existe | Detalle |
|---|---|---|
| Fotos | Parcial | No hay campo de foto en el formulario del RDT. Las fotos viven en el banco "Foto de campo" del modulo Informes y solo se vinculan al RDT a traves de una restriccion (selector de fotos de la fila de actividad). Los RDT de esta prueba no tienen fotos propias. |
| Materiales | Solo informativo | Se registran pero no suman a costo ni a avance. El costo de materiales del PR viene del DP x avance. |
| CNC | Si | Causa del catalogo por actividad D no cumplida. Es un catalogo con activo/inactivo; **no tiene estados de flujo** (responde la duda "CNC y sus estados"). |
| Restricciones | Si | Texto por actividad crea una restriccion con codigo `{N° OT}-RE-{n}`; estados Pendiente, Recepcionado, Atendido; atienden administrador, jefe de proyectos y jefe de oficina tecnica. |
| Inasistencias | Si, informativas | Sin horas ni costo; se excluyen si el RDT es RECHAZADO. |
| Clima | No | No hay campo de clima. |
| "Avance fisico del dia" escrito a mano | No | El avance fisico se calcula (EV / BAC); el supervisor solo escribe el metrado. |
| Horas extra y stand-by | Si | HH extra x 1.25; HM stand-by suman al costo del equipo; estado del equipo. |
| Borrador y plantillas | Si | `rdt_borradores`, plantillas. |

### A.4 Restricciones, CNC e inasistencias: en que flujo viven

No tienen un flujo propio. [DOC] Viven dentro de **06 (RDT)**: restricciones por actividad y CNC; dentro de **22 (Informes de supervision)**: la lista de restricciones y la pestana Inasistencias; y los permisos de todas estan en **14 (accesos)** como filas de tabla: causa CNC (crear, activar, editar: solo administrador y jefe de proyectos), la nota 17 sobre restricciones y la pestana Inasistencias (los 13 roles).

## B. Reglas de calculo que la app debe cumplir

**B.1 Estados y quien valida** [DOC 06, 14; APP `partes/[id]/route.ts`]

- Estados: REGISTRADO, (REVISADO), VALIDADO, RECHAZADO. Solo VALIDADO alimenta el PR (`recalcular_pr_desde_rdt`, recalculo completo, ultima version db/112).
- Validar o rechazar: administrador, jefe de proyectos, jefe de oficina tecnica. Rechazar un RDT ya VALIDADO: solo administrador y jefe de proyectos. Rechazar exige motivo. Validar un RECHAZADO exige justificacion.
- Crear / subir: administrador, jefe de proyectos, jefe de oficina tecnica, supervisor operativo. Corregir un RDT rechazado: administrador, jefe de proyectos, supervisor operativo (el jefe de oficina tecnica crea pero no corrige). Borrar: administrador y jefe de proyectos.
- Avisos: registrar avisa a los validadores; validar avisa al autor (no si el autor es quien valida); rechazar avisa al autor con el motivo.
- Plan Maestro: crear un RDT exige Plan Maestro APROBADO y servicio en EJECUCION; las demas acciones solo exigen Plan Maestro aprobado.

**B.2 Avance fisico y EV** [DOC 18, 10]

- EV por partida = metrado ejecutado acumulado (solo actividades D de RDT VALIDADOS) x PU. % fisico = suma de EV / BAC. PV = metrado programado del Plan Maestro aprobado x PU.
- Declarar por paquete: el supervisor escribe el metrado de la guia (2.3, ML); el servidor reparte el **mismo %** a las demas partidas del paquete (filas derivadas, solo lectura, `es_derivada`). La cantidad declarada no puede superar el metrado de la guia del paquete ([APP] `declaracion-paquete.ts`, error "La cantidad declarada supera el metrado de la partida guia del paquete"). Las filas derivadas cuentan como actividades en el PPC.
- Una partida repartida entre varios paquetes es la regla general; suma de porciones = metrado contractual [DOC 19, INDICE del servicio].
- Una partida directa (3.1, 3.2) se declara por su propia clave `DIRECTA : partida`.

**B.3 HH** [DOC 10, 18; APP db/112]

- Las horas (y su costo) se atribuyen a las partidas vinculadas en `rdt_actividad_partidas`. En modo paquete eso es **solo la guia 2.3**: las filas derivadas no llevan horas propias. El metrado y el EV si se reparten en 2.1 a 2.7.
- HH ganadas = % avance de la partida x HH contractual. IP = HH ganadas / HH reales. Las horas de cargos MOI (`es_moi`) se acumulan solo como horas y no se valorizan.
- HH extra: entra en horas totales y el costo es tarifa x horas x (1 + 0.25 x extra / total de la persona). Las HH reales y el IP no cambian por el recargo.

**B.4 Costo real (AC)** [DOC 10 "todo suma"; APP db/112, `tarifas.ts`]

- AC = personal (HH x tarifa congelada al validar) + equipos ((HM operativas + HM stand-by) x tarifa_hm, a la partida elegida en la fila) + materiales + subcontratos. Todo es costo directo, en USD. C y NC tambien suman (no son "indirectas").
- Materiales = costo contractual de materiales x v_avance, con v_avance = EV / BAC sin tope de 100 %. Subcontratos: por avance fisico o manual; este DP no tiene.
- Resolucion de tarifa al validar: cargo en `dp_moi` => MOI (sin costo, horas); si no, fila `dp_recursos` de mano de obra con el nombre normalizado (mayusculas, sin punto final); si no, equivalencias; si no, SIN_RESOLVER. Un recurso sin tarifa **no bloquea** la validacion (regla A5): cuesta 0, suma horas, avisa a administrador y jefe de proyectos y queda en `proyecto_pr.recursos_sin_tarifa`.
- La tarifa se congela al validar; las tarifas de los equipos se resuelven por nombre exacto en `dp_recursos`.

**B.5 Partidas transversales** (1.1, 1.2, 4.1) [DOC 10; APP db/111, db/112]

- Se excluyen del catalogo del RDT y se ignora cualquier dato de RDT que traigan. p = EV_resto / BAC_resto, con resto = partidas no transversales. EV total = EV_resto x BAC / BAC_resto. PV transversal = BAC x PV% del resto a la fecha de corte. HH = APU x p. Costo real = (MO + equipo del APU) x p. Sus materiales y subcontratos no se suman aparte. Requiere `dp_partida_costos` (DP reimportado).

**B.6 Acumulacion al validar y corregir** [APP]

- Validar: recalculo completo del PR desde todos los VALIDADOS (no incremental). Rechazar un VALIDADO: sale del PR y se recalcula. Un RDT REGISTRADO o RECHAZADO nunca entra. Corregir un rechazado crea el RDT en REGISTRADO con `motivoCorreccion`; hay que volver a validarlo.

**B.7 Otras formulas** [DOC 18, 11, 21]

- SV = EV - PV; CV = EV - AC; SPI = EV/PV; CPI = EV/AC; PPC = (actividades acumuladas - actividades con CNC) / actividades acumuladas.
- Curva S: serie diaria, se muestra por semana sabado a viernes; la serie real no pasa de la fecha de corte; el modo fisico no muestra USD; el modo economico solo para los 5 roles economicos (administrador, jefe de proyectos, jefe de oficina tecnica, supervisor de costos, jefe de costos). Los totales son resto x k (k = BAC / BAC_resto).
- CNC obligatorio si la actividad D tiene programado y ejecutado y ejecutado < programado ([APP] `parte.ts`).

## C. Linea base independiente del servicio (presupuesto y cronograma)

Fuente: `01_pg_planeamiento/vpc_trabajo/servicios/PS-167-2026_OBRAS-CIVILES-DETECCION-CONTRAINCENDIOS-TECNET/` (presupuesto-fusion.xlsx, que es el subido a la app; programar-plan-maestro.sql; INDICE.md). [CALC]

### C.1 Partidas

| Codigo | Descripcion | Und | Metrado | PU | Costo directo | HH contractual |
|---|---|---|---|---|---|---|
| 1.1 | Movilizacion y desmovilizacion (transversal) | VJE | 4 | 585.79 | 2,343.16 | 42.00 |
| 1.2 | Seguridad y senalizacion (transversal) | GLB | 1 | 2,010.18 | 2,010.18 | 0.00 |
| 2.1 | Andamios | DIA | 25 | 363.24 | 9,081.00 | 275.00 |
| 2.2 | Excavacion con retroexcavadora | M3 | 112.14 | 28.93 | 3,244.21 | 74.76 |
| 2.3 | Perfilado y nivelacion | ML | 267 | 5.49 | 1,465.83 | 70.09 |
| 2.4 | Cama de arena | ML | 267 | 24.93 | 6,656.31 | 93.45 |
| 2.5 | Suministro tuberia PVC | GLB | 1 | 0.00 | 0.00 | 0.00 |
| 2.6 | Instalacion tuberia PVC | ML | 267 | 6.86 | 1,831.62 | 93.45 |
| 2.7 | Relleno y compactacion | M3 | 80.1 | 57.10 | 4,573.71 | 273.70 |
| 3.1 | Suministro de buzon | UND | 4 | 311.43 | 1,245.72 | 48.80 |
| 3.2 | Instalacion de buzon | UND | 4 | 85.66 | 342.64 | 21.00 |
| 4.1 | Supervision servicios menores (transversal) | MES | 1.09 | 6,546.95 | 7,136.18 | 0.00 |
| | **Total costo directo (BAC)** | | | | **39,930.56** | **992.25** (el presupuesto fusion dice 992.26; dif. por redondeo del HH/und) |

- Grupos: 1 = 4,353.34; 2 (zanja) = 26,852.68; 3 (buzones) = 1,588.36; 4 = 7,136.18. Gastos generales (6,997.66) y utilidad (3,993.06) no entran al sistema (solo CD).
- BAC_resto (no transversales) = 26,852.68 + 1,588.36 = **28,441.04**. Transversales = 2,343.16 + 2,010.18 + 7,136.18 = 11,489.52. **k = 39,930.56 / 28,441.04 = 1.403977**.
- Valor por metro lineal de guia (zanja completa = 267 ml): 26,852.68 / 267 = **100.5718 USD/ml**; HH por ml = 880.45 / 267 = **3.2976 HH/ml**. Buzon 3.1: 311.43 USD y 12.19885 HH por und; buzon 3.2: 85.66 USD y 5.25 HH por und.
- Partida 2.5 (suministro de tuberia PVC) tiene PU 0: no aporta EV ni costo.

### C.2 Paquetes de zanja (PT-01 a PT-08) y orden de ejecucion

Guia = 2.3 en ML; cada paquete tiene las 7 partidas 2.1 a 2.7 con el mismo % [INDICE, SQL del Plan Maestro].

| Paquete | Ambiente | ml guia | BAC del paquete | 2.1 DIA | 2.2 M3 | 2.4/2.6 ML | 2.5 GLB | 2.7 M3 | Fechas |
|---|---|---|---|---|---|---|---|---|---|
| PT-01 | Lingo 1 y vestuarios | 30 | 3,017.16 | 2.8090 | 12.600 | 30.0 | 0.1124 | 9.000 | 19.10 a 22.10 |
| PT-02 | Vestidores y lingo oxidos | 101 | 10,157.76 | 9.4569 | 42.420 | 101.0 | 0.3783 | 30.300 | 22.10 a 04.11 |
| PT-03 | Torre de comunicaciones | 10.8 | 1,086.18 | 1.0112 | 4.536 | 10.8 | 0.0404 | 3.240 | 04.11 a 05.11 |
| PT-04 | Area cero | 17.5 | 1,760.01 | 1.6386 | 7.350 | 17.5 | 0.0655 | 5.250 | 05.11 a 07.11 |
| PT-05 | Lingo 2 y banos | 32 | 3,218.30 | 2.9963 | 13.440 | 32.0 | 0.1199 | 9.600 | 07.11 a 12.11 |
| PT-06 | Oficinas (chancado primario) | 41 | 4,123.45 | 3.8390 | 17.220 | 41.0 | 0.1536 | 12.300 | 12.11 a 18.11 |
| PT-07 | Estacion (chancado primario) | 3 | 301.72 | 0.2809 | 1.260 | 3.0 | 0.0112 | 0.900 | 18.11 |
| PT-08 | Sobreexcavaciones | 31.7 | 3,188.13 | 2.9682 | 13.314 | 31.7 | 0.1187 | 9.510 | 18.11 a 21.11 |

Partidas sueltas (sin paquete): 3.1 (4 und) programada 1 und por dia del 19 al 22.10; 3.2 (4 und) programada 4 und el 23.10 (ambas ESTIMADO, por confirmar). Los metrados de linea son proporcionales a ml/267 [CALC]; el redondeo que la app guarda en `metrado_linea` [NO DERIVABLE] puede cambiar el cuarto decimal.

### C.3 Programado (PV) por dia, 19 a 23.10

PV_resto del dia = ml guia programados x 100.5718 + und de buzon x PU. PV total = PV_resto x k (las transversales siguen el % del resto, no su fecha del cronograma).

| Dia | Programado (guia ml / und) | PV_resto del dia | PV total del dia | PV_resto acum. | PV total acum. | % programado acum. |
|---|---|---|---|---|---|---|
| 19.10 | PT-01 8.9 ml; 3.1 1 und | 1,206.52 | 1,693.93 | 1,206.52 | 1,693.93 | 4.24 % |
| 20.10 | PT-01 8.9; 3.1 1 | 1,206.52 | 1,693.93 | 2,413.04 | 3,387.85 | 8.48 % |
| 21.10 | PT-01 8.9; 3.1 1 | 1,206.52 | 1,693.93 | 3,619.56 | 5,081.78 | 12.73 % |
| 22.10 | PT-01 3.3; PT-02 5.6; 3.1 1 | 1,206.52 | 1,693.93 | 4,826.08 | 6,775.70 | 16.97 % |
| 23.10 | PT-02 8.9; 3.2 4 | 1,237.73 | 1,737.74 | 6,063.81 | 8,513.44 | 21.32 % |

Programado acumulado por clave al cierre de cada dia (guia ml): PT-01 = 8.9 / 17.8 / 26.7 / 30.0 / 30.0; PT-02 = 0 / 0 / 0 / 5.6 / 14.5; 3.1 = 1 / 2 / 3 / 4 / 4; 3.2 = 0 / 0 / 0 / 0 / 4.

### C.4 Costo directo contractual por recurso (referencia)

Mano de obra 20,731.96; equipos 13,891.60; materiales 5,307.00 (listado de insumos). HH MOD 992.26. Tarifas por HH en el APU: CAPATAZ 15.38; OPERARIO CIVIL 13.94; OFICIAL CIVIL 13.37; PEON 11.86 (aparece tambien un PEON a 20.20, ver E); OPERARIO MECANICO 13.94; OFICIAL MECANICO 13.37; VIGIA 11.86; OPERADOR EQUIPO LIVIANO 13.46; OPERADOR LINEA AMARILLA 15.20. Tarifas por HM: CAMION BARANDA 75.00; RETROEXCAVADORA JOHN DEERE 310G 38.23; MARTILLO NEUMATICO 12.50; ROTOMARTILLO 3.50; GRUPO ELECTROGENO 11KW 9.20; CAMION VOLQUETE 15 m3 75.00; VIBRO APISONADOR 12.20. [CALC]

### C.5 Lo que NO se puede derivar sin la base de datos

- Personas reales del catalogo `recursos_personal` (DNI, nombre, cargo) y si existen para TECNET. **No se inventaron nombres ni DNI.**
- Que cargos estan en `dp_moi` (se asume por la hoja GG: Jefe de Proyectos, Ingeniero de Calidad, Ingeniero de Oficina Tecnica, Ingeniero Operativo, Ingeniero SSOMA, Conductor, Almacen; sin verificar).
- Tarifas congeladas reales y la resolucion de los nombres de cargo y equipo tras la conciliacion del DP (los nombres del APU difieren a veces del catalogo, p. ej. "OPERADOR LINEA AMARILLA" contra "OPERADOR DE LINEA AMARILLA").
- Si el DP se reimporto con `dp_partida_costos` (sin eso, las transversales no se calculan).
- El monto real de materiales en `pr_recursos`: el listado dice 5,307.00, pero la suma de materiales por APU da 3,570.22 (no transversales) + 1,819.10 (transversales) = 5,389.32. Por eso el AC se da con dos hipotesis (M = 5,307.00 y M = 3,570.22). Usar la que coincida con el valor de materiales del PR antes de empezar.
- Lineas reales y redondeo del Plan Maestro aprobado; el estado actual del servicio (EJECUCION o no) y el tipo de dashboard.
- Equipo "MARTILLO NEUMATICO" y "CAMION VOLQUETE 15 m3": el catalogo los llama "MARTILLO NEUMATICO P/ RETROEXCAVADORA" y "CAMION VOLQUETE DE 15 M3"; por eso esta prueba usa solo equipos cuyo nombre coincide exacto (RETROEXCAVADORA JOHN DEERE 310G, CAMION BARANDA, ROTOMARTILLO, GRUPO ELECTROGENO 11KW).

## D. Cinco RDT de prueba (dia 1 a dia 5)

### D.0 Supuestos y datos fijos

- Dias: D1 = lun 19.10, D2 = mar 20.10, D3 = mie 21.10, D4 = jue 22.10, D5 = vie 23.10. **Hoy es 19.10: D2 a D5 son fechas futuras.** El servidor no tiene validacion de fecha futura (busqueda en el codigo, no exhaustiva) y el selector no tiene maximo; si Victor no las permite, ver pregunta E1.
- Cabecera comun: N° OT PS-0001, turno DIA, especialidad civil (nombre exacto de la lista), ubicacion = ambiente del paquete (PT-01 "Lingo 1 y vestuarios", PT-02 "Vestidores y lingo oxidos"), semana N° 1 (a confirmar), jornada 8 h.
- Toda observacion y toda nota de la prueba empieza con **PRUEBA FUNCIONAL** para poder filtrarlas y borrarlas despues (el borrado lo hace Victor o el admin, nunca este plan).
- Modo de declaracion: PT-01 y PT-02 **por paquete** (se escribe solo la guia 2.3 en ML); 3.1 y 3.2 **directas**. C y NC no llevan metrado.
- Cargos reales del catalogo (db/097, 2026-10-15; puede haber cambiado): CAPATAZ, OPERARIO CIVIL, OFICIAL CIVIL, PEON, OPERADOR DE LINEA AMARILLA, INGENIERO SSOMA (supuesto MOI), TOPOGRAFO (sin tarifa en el DP: prueba de la regla A5). Personas: tomar del catalogo, una por fila; si no hay, ver E3.
- Tarifas usadas en el calculo: las de C.4. Horas extra: factor 1.25.

### D.1 Orden de las acciones (por rol)

| Paso | Accion | Rol que la hace | Resultado esperado |
|---|---|---|---|
| 0 | Precondiciones: Plan Maestro APROBADO, servicio en EJECUCION, DP con costos, catalogos | administrador / jefe de proyectos | Si no, crear RDT responde 400 |
| 1 | Crear RDT D1 | supervisor operativo | REGISTRADO; validadores avisados |
| 2 | Validar D1 | jefe de proyectos | VALIDADO; autor avisado; PR = fila D1 de D.7 |
| 3 | Crear RDT D2 version 1 (con error de metrado 9.5 ml) | supervisor operativo | REGISTRADO |
| 4 | Rechazar D2 con motivo | jefe de oficina tecnica | RECHAZADO; autor avisado con el motivo; **PR sin cambio** (= fila D1) |
| 5 | Corregir D2 (metrado 8.9 ml) con `motivoCorreccion` | supervisor operativo | REGISTRADO (reemplaza al rechazado) |
| 6 | Validar D2 | jefe de proyectos | VALIDADO; PR = fila D2 |
| 7 | Crear y validar D3; la restriccion de D3 se recepciona y atiende | supervisor operativo / jefe de proyectos | PR = fila D3; restriccion PS-0001-RE-1 (codigo por confirmar) |
| 8 | Crear y validar D4 (incluye TOPOGRAFO sin tarifa) | supervisor operativo / jefe de proyectos | PR = fila D4; aviso por recurso sin tarifa |
| 9 | Crear y validar D5 | supervisor operativo / jefe de proyectos | PR = fila D5 |
| 10 | Pruebas negativas y de permisos (D.8) | segun caso | Mensajes de la app |

Nota de lectura: en cada dia "act. 1", "act. 2" y "act. 3" son las columnas T1, T2, T3 de la matriz del RDT; el contenido de cada columna esta en la lista de actividades del dia. Las horas de MOI y de TOPOGRAFO se escriben igual que las demas.

### D.2 RDT D1 - lun 19.10 - caso PARCIAL (con CNC)

Actividades:

- T1 D, paquete PT-01, guia 2.3 ML: programado 8.9, **ejecutado 6.0** (parcial, 67.4 % de lo programado). Falta ejecutado => **CNC obligatoria**: elegir una causa activa del catalogo (texto exacto). El servidor deriva 2.1 = 0.5618 DIA, 2.2 = 2.520 M3, 2.4 = 6.0 ML, 2.5 = 0.0225 GLB, 2.6 = 6.0 ML, 2.7 = 1.800 M3 (20 % de cada linea del paquete: 6.0 / 30).
- T2 D, partida directa 3.1 UND: programado 1, ejecutado 1.
- T3 C "PRUEBA FUNCIONAL charla de seguridad y reunion de inicio" (sin metrado), vinculada a 2.3 de PT-01.
- Restriccion: ninguna. Inasistencia: ninguna. Observaciones: "PRUEBA FUNCIONAL D1: avance parcial por inicio de frente."

| Cargo | Personas | Horas act. 1 | Horas act. 2 | Horas act. 3 | Total h por persona | de ellas extra | Tarifa | Costo (formula) |
|---|---|---|---|---|---|---|---|---|
| CAPATAZ | 1 | 7 | 0 | 1 | 8 | 0 | 15.38 | 1 x 8 h x 15.38 = 123.04 |
| OPERARIO CIVIL | 2 | 7 | 0 | 1 | 8 | 0 | 13.94 | 2 x 8 h x 13.94 = 223.04 |
| OFICIAL CIVIL | 2 | 3 | 4 | 1 | 8 | 0 | 13.37 | 2 x 8 h x 13.37 = 213.92 |
| OPERADOR DE LINEA AMARILLA | 1 | 7 | 0 | 1 | 8 | 0 | 15.20 | 1 x 8 h x 15.2 = 121.60 |
| INGENIERO SSOMA | 1 | 1 | 0 | 1 | 2 | 0 | MOI, sin costo | 0 |

| Equipo | Partida (clave) | HM operativas | HM stand-by | Tarifa HM | Costo |
|---|---|---|---|---|---|
| RETROEXCAVADORA JOHN DEERE 310G | PT-01:2.2 | 8 | 0 | 38.23 | 8 x 38.23 = 305.84 |
| GRUPO ELECTROGENO 11KW | 3.1 | 8 | 0 | 9.2 | 8 x 9.2 = 73.60 |

Horas D1: MOD 48 h, MOI 2 h. Costo personal del dia 681.60; equipos del dia 379.44.

### D.3 RDT D2 - mar 20.10 - RECHAZO y CORRECCION; inasistencia

- **Version 1 (a rechazar)**: igual a la version final salvo T1 ejecutado = **9.5** ml y una observacion "PRUEBA FUNCIONAL D2 v1: metrado con error, rechazar". Rechazo (jefe de oficina tecnica): motivo "PRUEBA FUNCIONAL: el metrado de la guia no coincide con el control de campo; corregir a 8.9 ml".
- **Version final (correccion con `motivoCorreccion` = "PRUEBA FUNCIONAL: metrado corregido a 8.9 ml")**: T1 D, PT-01 guia 2.3: programado 8.9, **ejecutado 8.9** (igual al programado); T2 D, 3.1: programado 1, ejecutado 1. Sin C ni NC.
- Inasistencia: 1 persona del catalogo, motivo **Falta**, nota "PRUEBA FUNCIONAL: inasistencia informativa" (no suma horas ni costo).
- Equipo con **HM stand-by**: la retroexcavadora 6 HM operativas + 2 HM stand-by.
- Observaciones: "PRUEBA FUNCIONAL D2: corregido tras rechazo."

| Cargo | Personas | Horas act. 1 | Horas act. 2 | Horas act. 3 | Total h por persona | de ellas extra | Tarifa | Costo (formula) |
|---|---|---|---|---|---|---|---|---|
| CAPATAZ | 1 | 8 | 0 | 0 | 8 | 0 | 15.38 | 1 x 8 h x 15.38 = 123.04 |
| OPERARIO CIVIL | 2 | 5 | 3 | 0 | 8 | 0 | 13.94 | 2 x 8 h x 13.94 = 223.04 |
| OFICIAL CIVIL | 2 | 8 | 0 | 0 | 8 | 0 | 13.37 | 2 x 8 h x 13.37 = 213.92 |
| OPERADOR DE LINEA AMARILLA | 1 | 8 | 0 | 0 | 8 | 0 | 15.20 | 1 x 8 h x 15.2 = 121.60 |
| INGENIERO SSOMA | 1 | 2 | 0 | 0 | 2 | 0 | MOI, sin costo | 0 |

| Equipo | Partida (clave) | HM operativas | HM stand-by | Tarifa HM | Costo |
|---|---|---|---|---|---|
| RETROEXCAVADORA JOHN DEERE 310G | PT-01:2.2 | 6 | 2 | 38.23 | 8 x 38.23 = 305.84 |
| GRUPO ELECTROGENO 11KW | 3.1 | 8 | 0 | 9.2 | 8 x 9.2 = 73.60 |

Nota: con la version 1 el EV de D2 habria sido 9.5 x 100.5718 = 955.43 en guia (+60.30 respecto de la version final): ese valor **no debe aparecer** en ninguna pantalla tras el rechazo ni tras la correccion.

### D.4 RDT D3 - mie 21.10 - metrado MAYOR al programado, HH extra, NC, restriccion

- T1 D, PT-01 guia 2.3: programado 8.9, **ejecutado 10.0** (112.4 % de lo programado; no requiere CNC; sigue dentro del metrado de la guia = 30). T2 D, 3.1: 1 de 1.
- T3 NC "PRUEBA FUNCIONAL espera por liberacion de frente" (sin metrado), vinculada a 2.3 de PT-01. Esa hora si suma a HH y a AC.
- **HH extra**: 2 h extra por persona en CAPATAZ, OPERARIO CIVIL, OFICIAL CIVIL y OPERADOR DE LINEA AMARILLA (jornada 8 h, total 10 h).
- **Restriccion** (texto en la fila T1): "PRUEBA FUNCIONAL: falta liberacion del frente de lingo 1 para continuar perfilado"; con 1 foto del banco "Para restricciones" solo si existe (ver E5). Debe crearse PS-0001-RE-1 en Pendiente (formato de codigo por confirmar); luego Recepcionado y Atendido por el jefe de proyectos; el cambio de estado queda en la lista de Informes.
- Observaciones: "PRUEBA FUNCIONAL D3: sobreproduccion de 1.1 ml sobre lo programado."

| Cargo | Personas | Horas act. 1 | Horas act. 2 | Horas act. 3 | Total h por persona | de ellas extra | Tarifa | Costo (formula) |
|---|---|---|---|---|---|---|---|---|
| CAPATAZ | 1 | 9 | 0 | 1 | 10 | 2 | 15.38 | 1 x 10 h x 15.38 x (1+0.25x2/10) = 161.49 |
| OPERARIO CIVIL | 2 | 6 | 3 | 1 | 10 | 2 | 13.94 | 2 x 10 h x 13.94 x (1+0.25x2/10) = 292.74 |
| OFICIAL CIVIL | 2 | 6 | 3 | 1 | 10 | 2 | 13.37 | 2 x 10 h x 13.37 x (1+0.25x2/10) = 280.77 |
| OPERADOR DE LINEA AMARILLA | 1 | 9 | 0 | 1 | 10 | 2 | 15.20 | 1 x 10 h x 15.2 x (1+0.25x2/10) = 159.60 |
| INGENIERO SSOMA | 1 | 2 | 0 | 0 | 2 | 0 | MOI, sin costo | 0 |

| Equipo | Partida (clave) | HM operativas | HM stand-by | Tarifa HM | Costo |
|---|---|---|---|---|---|
| RETROEXCAVADORA JOHN DEERE 310G | PT-01:2.2 | 8 | 0 | 38.23 | 8 x 38.23 = 305.84 |
| ROTOMARTILLO | PT-01:2.3 | 6 | 0 | 3.5 | 6 x 3.5 = 21.00 |
| GRUPO ELECTROGENO 11KW | 3.1 | 8 | 0 | 9.2 | 8 x 9.2 = 73.60 |

Horas extra del dia: 12 h (6 personas x 2 h). Costo personal del dia con recargo: 894.60 (sin recargo seria 852.00).

### D.5 RDT D4 - jue 22.10 - COMPLETA un paquete y una partida; segundo paquete parcial con CNC; recurso sin tarifa

- T1 D, PT-01 guia 2.3: programado 3.3, **ejecutado 5.1**. Acumulado de PT-01 = 6.0 + 8.9 + 10.0 + 5.1 = **30.0 ml = 100 %**: el paquete PT-01 queda COMPLETO (las 7 partidas al 100 % de su linea). Ejecutado mayor que programado: sin CNC.
- T2 D, PT-02 guia 2.3: programado 5.6, **ejecutado 4.0** (parcial) => **CNC obligatoria** (otra causa o la misma del catalogo).
- T3 D, 3.1 UND: programado 1, ejecutado 1. Acumulado 3.1 = 4 de 4: **partida 3.1 COMPLETA**.
- **TOPOGRAFO** (cargo del catalogo sin tarifa en el DP): 4 h. Debe validar igual; costo 0, suma 4 h a las HH, avisa a administrador y jefe de proyectos y queda en `recursos_sin_tarifa` (regla A5). Si el catalogo de equivalencias resuelve TOPOGRAFO, el resultado cambia: ver E4.
- Observaciones: "PRUEBA FUNCIONAL D4: cierre de PT-01 y de 3.1."

| Cargo | Personas | Horas act. 1 | Horas act. 2 | Horas act. 3 | Total h por persona | de ellas extra | Tarifa | Costo (formula) |
|---|---|---|---|---|---|---|---|---|
| CAPATAZ | 1 | 3 | 4 | 1 | 8 | 0 | 15.38 | 1 x 8 h x 15.38 = 123.04 |
| OPERARIO CIVIL | 2 | 3 | 3 | 2 | 8 | 0 | 13.94 | 2 x 8 h x 13.94 = 223.04 |
| OFICIAL CIVIL | 2 | 2 | 3 | 3 | 8 | 0 | 13.37 | 2 x 8 h x 13.37 = 213.92 |
| OPERADOR DE LINEA AMARILLA | 1 | 4 | 4 | 0 | 8 | 0 | 15.20 | 1 x 8 h x 15.2 = 121.60 |
| TOPOGRAFO | 1 | 2 | 2 | 0 | 4 | 0 | sin tarifa (0) | 0 |
| INGENIERO SSOMA | 1 | 1 | 1 | 0 | 2 | 0 | MOI, sin costo | 0 |

| Equipo | Partida (clave) | HM operativas | HM stand-by | Tarifa HM | Costo |
|---|---|---|---|---|---|
| RETROEXCAVADORA JOHN DEERE 310G | PT-01:2.2 | 5 | 0 | 38.23 | 5 x 38.23 = 191.15 |
| RETROEXCAVADORA JOHN DEERE 310G | PT-02:2.2 | 3 | 0 | 38.23 | 3 x 38.23 = 114.69 |
| CAMION BARANDA | 3.1 | 4 | 0 | 75.0 | 4 x 75.0 = 300.00 |
| GRUPO ELECTROGENO 11KW | 3.1 | 8 | 0 | 9.2 | 8 x 9.2 = 73.60 |

### D.6 RDT D5 - vie 23.10 - igual al programado; cierre de 3.2; PEON

- T1 D, PT-02 guia 2.3: programado 8.9, **ejecutado 8.9** (acumulado PT-02 = 12.9 de 101 ml). T2 D, 3.2 UND: programado 4, **ejecutado 4** => 3.2 COMPLETA (4 de 4).
- **PEON x 2**: el APU tiene un PEON a 11.86 y otro a 20.20; el esperado usa 11.86; si la app congela 20.20 el costo de los 2 PEON sube de 189.76 a 323.20 (E4).
- Observaciones: "PRUEBA FUNCIONAL D5: cierre de 3.2."

| Cargo | Personas | Horas act. 1 | Horas act. 2 | Horas act. 3 | Total h por persona | de ellas extra | Tarifa | Costo (formula) |
|---|---|---|---|---|---|---|---|---|
| CAPATAZ | 1 | 6 | 2 | 0 | 8 | 0 | 15.38 | 1 x 8 h x 15.38 = 123.04 |
| OPERARIO CIVIL | 2 | 6 | 2 | 0 | 8 | 0 | 13.94 | 2 x 8 h x 13.94 = 223.04 |
| OFICIAL CIVIL | 2 | 6 | 2 | 0 | 8 | 0 | 13.37 | 2 x 8 h x 13.37 = 213.92 |
| PEON | 2 | 8 | 0 | 0 | 8 | 0 | 11.86 | 2 x 8 h x 11.86 = 189.76 |
| OPERADOR DE LINEA AMARILLA | 1 | 8 | 0 | 0 | 8 | 0 | 15.20 | 1 x 8 h x 15.2 = 121.60 |
| INGENIERO SSOMA | 1 | 2 | 0 | 0 | 2 | 0 | MOI, sin costo | 0 |

| Equipo | Partida (clave) | HM operativas | HM stand-by | Tarifa HM | Costo |
|---|---|---|---|---|---|
| RETROEXCAVADORA JOHN DEERE 310G | PT-02:2.2 | 8 | 0 | 38.23 | 8 x 38.23 = 305.84 |
| ROTOMARTILLO | PT-02:2.3 | 4 | 0 | 3.5 | 4 x 3.5 = 14.00 |
| CAMION BARANDA | 3.2 | 6 | 0 | 75.0 | 6 x 75.0 = 450.00 |

### D.7 Valores esperados tras VALIDAR cada dia (acumulados)

Formulas: EV_resto = (ml guia acumulados x 100.5718) + (und 3.1 x 311.43) + (und 3.2 x 85.66); EV total = EV_resto x 1.403977; % fisico = EV_resto / 28,441.04; AC = personal + equipos + transversal + materiales, con transversal = 9,670.42 x p (p = % fisico) y materiales = M x p. Hipotesis de materiales: **A** M = 5,307.00; **B** M = 3,570.22 (ver C.5). Si M real es otro, recalcular solo la columna de materiales.

**D.7.1 Avance, EV, PV y desempeno**

| Tras validar | ml guia acum. (PT-01 / PT-02) | EV_resto | EV total | % fisico real | PV total acum. | % programado | SV | SPI |
|---|---|---|---|---|---|---|---|---|
| 19.10 | 6.0 / 0.0 | 914.86 | 1,284.44 | 3.22 % | 1,693.93 | 4.24 % | -409.48 | 0.758 |
| 20.10 | 14.9 / 0.0 | 2,121.38 | 2,978.37 | 7.46 % | 3,387.85 | 8.48 % | -409.48 | 0.879 |
| 21.10 | 24.9 / 0.0 | 3,438.53 | 4,827.61 | 12.09 % | 5,081.78 | 12.73 % | -254.16 | 0.950 |
| 22.10 | 30.0 / 4.0 | 4,665.16 | 6,549.78 | 16.40 % | 6,775.70 | 16.97 % | -225.92 | 0.967 |
| 23.10 | 30.0 / 12.9 | 5,902.89 | 8,287.52 | 20.75 % | 8,513.44 | 21.32 % | -225.92 | 0.973 |

**D.7.2 Costo real (AC), HH e indices**

| Tras validar | AC personal | AC equipos | AC transversales | AC materiales (A / B) | AC total (A / B) | CV (A / B) | CPI (A / B) |
|---|---|---|---|---|---|---|---|
| 19.10 | 681.60 | 379.44 | 311.07 | 170.71 / 114.84 | 1,542.82 / 1,486.95 | -258.37 / -202.51 | 0.833 / 0.864 |
| 20.10 | 1,363.20 | 758.88 | 721.30 | 395.84 / 266.30 | 3,239.23 / 3,109.68 | -260.86 / -131.31 | 0.919 / 0.958 |
| 21.10 | 2,257.80 | 1,159.32 | 1,169.16 | 641.62 / 431.64 | 5,227.89 / 5,017.92 | -400.28 / -190.30 | 0.923 / 0.962 |
| 22.10 | 2,939.40 | 1,838.76 | 1,586.23 | 870.50 / 585.62 | 7,234.89 / 6,950.01 | -685.11 / -400.23 | 0.905 / 0.942 |
| 23.10 | 3,810.76 | 2,608.60 | 2,007.08 | 1,101.46 / 740.99 | 9,527.90 / 9,167.43 | -1,240.38 / -879.91 | 0.870 / 0.904 |

| Tras validar | HH reales MOD (con TOPOGRAFO) | HH MOI (solo horas) | HH ganadas | IP |
|---|---|---|---|---|
| 19.10 | 48 | 2 | 33.34 | 0.694 |
| 20.10 | 96 | 4 | 76.66 | 0.799 |
| 21.10 | 156 | 6 | 123.78 | 0.793 |
| 22.10 | 208 | 8 | 167.80 | 0.807 |
| 23.10 | 272 | 10 | 219.98 | 0.809 |

HH ganadas = 3.2976 x ml guia + 12.19885 x und 3.1 + 5.25 x und 3.2 + 42 x p (transversal 1.1). IP = HH ganadas / HH reales MOD; si la app incluye las horas MOI en las HH reales el IP baja (confirmar en la pantalla qué se cuenta). El valor diario (no acumulado) de EV, personal y equipos se obtiene restando filas consecutivas; por ejemplo EV total de D1 = 1,284.44 y de D2 = 1,693.93.

**D.7.3 Detalle por partida al cierre de D5 (PR, costo directo, sin materiales)**

Metrado acumulado por partida de zanja = metrado contractual x 42.9 / 267 (30 ml de PT-01 + 12.9 de PT-02 = 16.07 %).

| Partida | Metrado acum. | EV = metrado x PU | HH reales atribuidas (solo guia/directas) | Costo MO+equipo atribuido |
|---|---|---|---|---|
| 2.1 | 4.0169 | 1,459.08 | 0.00 | 0.00 |
| 2.2 | 18.0180 | 521.26 | 0.00 | 1,529.20 |
| 2.3 | 42.9000 | 235.52 | 225.00 | 3,191.75 |
| 2.4 | 42.9000 | 1,069.50 | 0.00 | 0.00 |
| 2.5 | 0.1607 | 0.00 | 0.00 | 0.00 |
| 2.6 | 42.9000 | 294.29 | 0.00 | 0.00 |
| 2.7 | 12.8700 | 734.88 | 0.00 | 0.00 |
| 3.1 | 4 | 1,245.72 | 37.00 | 1,108.41 |
| 3.2 | 4 | 342.64 | 10.00 | 590.00 |
| 1.1 (transversal) | 0.8302 | 486.32 | 8.72 (APU x p) | 422.81 (APU x p) |
| 1.2 (transversal) | 0.2075 | 417.21 | 0.00 (APU x p) | 171.04 (APU x p) |
| 4.1 (transversal) | 0.2262 | 1,481.10 | 0.00 (APU x p) | 1,413.23 (APU x p) |

Las HH de los cargos MOI no entran en esta tabla. Se observa que **todo el costo de personal de zanja cae en 2.3** (modo paquete), mientras que el EV se reparte en 2.1 a 2.7; el costo de equipos cae en la partida elegida en cada fila (2.2, 2.3, 3.1, 3.2). Si la app rechaza un equipo sobre una fila derivada (2.2), usar 2.3 y recalcular.

**D.7.4 Plan Maestro (Real / Prog / Acum.) y Curva S**

| Clave | Que mirar | D1 | D2 | D3 | D4 | D5 |
|---|---|---|---|---|---|---|
| PT-01 : 2.3 (guia) | Real acum. (ml) | 6.0 | 14.9 | 24.9 | 30.0 | 30.0 |
| PT-01 : 2.3 (guia) | Prog acum. (ml) | 8.9 | 17.8 | 26.7 | 30.0 | 30.0 |
| PT-01 : 2.1 (derivada) | Real acum. (metrado derivado) | 0.5618 DIA | 1.3951 DIA | 2.3315 DIA | 2.8090 DIA | 2.8090 DIA |
| PT-01 : 2.2 (derivada) | Real acum. (metrado derivado) | 2.5200 M3 | 6.2580 M3 | 10.4580 M3 | 12.6000 M3 | 12.6000 M3 |
| PT-01 : 2.4 (derivada) | Real acum. (metrado derivado) | 6.0000 ML | 14.9000 ML | 24.9000 ML | 30.0000 ML | 30.0000 ML |
| PT-01 : 2.5 (derivada) | Real acum. (metrado derivado) | 0.0225 GLB | 0.0558 GLB | 0.0933 GLB | 0.1124 GLB | 0.1124 GLB |
| PT-01 : 2.6 (derivada) | Real acum. (metrado derivado) | 6.0000 ML | 14.9000 ML | 24.9000 ML | 30.0000 ML | 30.0000 ML |
| PT-01 : 2.7 (derivada) | Real acum. (metrado derivado) | 1.8000 M3 | 4.4700 M3 | 7.4700 M3 | 9.0000 M3 | 9.0000 M3 |
| PT-02 : 2.3 (guia) | Real acum. (ml) | 0 | 0 | 0 | 4.0 | 12.9 |
| PT-02 : 2.3 (guia) | Prog acum. (ml) | 0 | 0 | 0 | 5.6 | 14.5 |
| PT-02 : 2.1 (derivada) | Real acum. (metrado derivado) | 0.0000 DIA | 0.0000 DIA | 0.0000 DIA | 0.3745 DIA | 1.2079 DIA |
| PT-02 : 2.2 (derivada) | Real acum. (metrado derivado) | 0.0000 M3 | 0.0000 M3 | 0.0000 M3 | 1.6800 M3 | 5.4180 M3 |
| PT-02 : 2.7 (derivada) | Real acum. (metrado derivado) | 0.0000 M3 | 0.0000 M3 | 0.0000 M3 | 1.2000 M3 | 3.8700 M3 |
| DIRECTA : 3.1 | Real / Prog acum. (und) | 1 / 1 | 2 / 2 | 3 / 3 | 4 / 4 | 4 / 4 |
| DIRECTA : 3.2 | Real / Prog acum. (und) | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 4 / 4 |

Cada RDT debe quedar asociado a su fecha en las subfilas Real, y las filas de PT-01 y PT-02 de la misma semana (sabado 17.10 a viernes 23.10) suman en esa semana. Si una linea queda en rojo o "falta repartir" tras aprobar, es un hallazgo (el INDICE dice 100 % repartido).

**Curva S (semana sabado 17.10 a viernes 23.10, serie diaria)**

| Dia | % programado acum. | % real acum. | Real en USD (solo roles economicos) |
|---|---|---|---|
| 19.10 | 4.24 % | 3.22 % | EV 1,284.44 (y AC 1,542.82 / 1,486.95) |
| 20.10 | 8.48 % | 7.46 % | EV 2,978.37 (y AC 3,239.23 / 3,109.68) |
| 21.10 | 12.73 % | 12.09 % | EV 4,827.61 (y AC 5,227.89 / 5,017.92) |
| 22.10 | 16.97 % | 16.40 % | EV 6,549.78 (y AC 7,234.89 / 6,950.01) |
| 23.10 | 21.32 % | 20.75 % | EV 8,287.52 (y AC 9,527.90 / 9,167.43) |

En la semana, el punto de cierre (viernes 23.10) debe mostrar 20.75 % real contra 21.32 % programado. La serie real no debe pasar de la fecha de corte (23.10, o del ultimo dia validado). En modo fisico no deben verse USD; en modo economico solo los 5 roles economicos (ver B.7).

**D.7.5 Dashboard y PPC**

- KPIs al cierre de D5: avance 20.75 %; SPI 0.973; CPI 0.870 (A) o 0.904 (B); IP 0.809; HH ganadas 219.98.
- Pareto de CNC: **2 eventos** (D1 de PT-01 y D4 de PT-02), con las causas elegidas del catalogo (texto exacto, si no, no aparecen: leccion de la prueba MARCOBRE).
- PPC (hipotesis a verificar): se cuentan solo actividades D; un paquete declarado aporta 7 filas (guia + 6 derivadas) y la CNC va solo en la fila guia. Actividades acumuladas D1..D5 = 8 / 16 / 24 / 39 / 47; con CNC = 1 / 1 / 1 / 2 / 2; PPC = 87.50 % / 93.75 % / 95.83 % / 94.87 % / 95.74 %. Si la app cuenta de otra forma, anotar la diferencia como hallazgo en vez de forzar el numero.
- Tipo de dashboard (Parcial o Completo) del servicio: por confirmar (E).

**D.7.6 Avisos y otros efectos que verificar**

- Registrar D1..D5: aviso a validadores. Validar: aviso al autor. Rechazar D2 v1: aviso al autor con el motivo. Validar D4: aviso a administrador y jefe de proyectos por TOPOGRAFO sin tarifa y entrada en `recursos_sin_tarifa`.
- Restriccion de D3: creada sola, en Pendiente, con prioridad (Alta, Media o Baja a elegir), pasa a Recepcionado y Atendido; visible en Informes.
- Inasistencia de D2: aparece en la pestana Inasistencias (rango 20.10 a 20.10, nota maxima 500) y no cambia HH ni AC. Si el RDT D2 version 1 estaba RECHAZADO, su inasistencia no aparece hasta la version corregida.

### D.8 Pruebas negativas y de permisos (adicionales, opcionales)

| Caso | Esperado |
|---|---|
| Actividad D con ejecutado < programado y sin CNC | Error de validacion (CNC requerida) |
| Declarar en PT-01 una cantidad mayor a 30 ml | Error "La cantidad declarada supera el metrado de la partida guia del paquete" |
| Registrar otro RDT con misma OT + fecha + turno | 409 `PARTE_DUPLICADO` |
| Reemplazar un RDT VALIDADO | No permitido; solo rechazarlo (administrador o jefe de proyectos) |
| Rechazar sin motivo | Error |
| Supervisor operativo valida su propio RDT | No debe poder (solo administrador, jefe de proyectos, jefe de oficina tecnica) |
| Jefe de oficina tecnica corrige un RDT rechazado | No debe poder (si crear y validar) |
| Rechazar D3 ya VALIDADO (administrador) | Sale del PR; al volver a validar exige justificacion; PR vuelve a la fila de D2 hasta revalidar |
| Servicio fuera de EJECUCION | Crear responde 400 `SERVICIO_NO_EN_EJECUCION` |

## E. Preguntas abiertas para Victor

1. **Fechas futuras.** Hoy es 19.10: D2 a D5 serian del 20 al 23.10. El servidor no tiene regla de fecha futura y el selector no tiene maximo, pero el informe si limita "Hasta" a hoy. Se permiten RDT con fecha futura en esta prueba, o se corre un dia por dia real, o se desplaza todo a fechas pasadas?
2. **Cuentas y roles.** Que cuentas de prueba existen para: supervisor operativo (crea y corrige), jefe de proyectos y jefe de oficina tecnica (validan; el segundo rechaza), administrador? Quien valida cada dia? (No se escriben claves en este plan.)
3. **Personal y cargos.** El catalogo de cargos usado es de db/097 (2026-10-15). Hay personas cargadas en `recursos_personal` para estos cargos (CAPATAZ, OPERARIO CIVIL, OFICIAL CIVIL, PEON, OPERADOR DE LINEA AMARILLA, INGENIERO SSOMA, TOPOGRAFO)? Si no, quien las carga? Nota: hay una lista "Personal para el servicio JAHUAY" con nombres reales (WhatsApp, 19.10) que es de otro servicio; no se uso.
4. **Tarifas y MOI.** Cuales cargos estan en `dp_moi` (INGENIERO SSOMA es supuesto)? Cual PEON congela la app, 11.86 o 20.20? TOPOGRAFO debe quedar sin tarifa a proposito para probar la regla A5, o ya tiene equivalencia? Que monto de materiales muestra el PR antes de empezar (5,307.00 u otro)?
5. **Fotos.** El banco "Foto de campo" existe (pagina `/proyectos/{id}/informes/foto` y su API). No se encontraron fotos reales de campo de TECNET en `D:\VICTOR\CLAUDE CODE\`, ni en `docs\06-material-de-apoyo\Imagenes para fronted` (solo `inicio.jpg` y `entorno de trabajo.jpg`, capturas de la interfaz), ni en el repo de la app. Lo mas parecido son las imagenes de muestra del sello del plan Foto de campo (en `docs/02-trabajo-activo/03-evidencia/2026-10-19-foto-de-campo-con-sello-y-app-android/`) y fotos de ensayos de otro proyecto (`pg_dossier_calidad`). Hay fotos reales de la obra o se omite la foto de la restriccion en esta prueba?
6. **Servicio.** El servicio esta ya en EJECUCION y con el DP reimportado con `dp_partida_costos`? Que tipo de dashboard tiene (Parcial o Completo)? Cual es el nombre exacto de la disciplina civil y que numero de semana se usa?
7. **Plan Maestro y cronograma.** 3.1 y 3.2 estan programadas en forma estimada (1 und por dia y 4 und el 23.10); se aceptan asi para el PV? El control del cliente trae 6 buzones y el presupuesto 4: la prueba usa 4. Las transversales siguen el % del resto, no su fecha del cronograma (1.1 el 19 y 20.10): se acepta?
8. **Cuanto cuenta.** Las HH MOI cuentan en las HH reales del IP? El PPC cuenta las filas derivadas y a que fila va la CNC?
9. **Limpieza posterior.** Los RDT de prueba quedan en el servicio real PS-0001: quien los borra o rechaza al terminar, y se acepta que contaminen avance, AC y Curva S hasta entonces?

*Este plan fue preparado sin escribir en la app ni en la base de datos.*
