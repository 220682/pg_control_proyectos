# 04 - Prueba del RDT en PS-0001, versión 2 (guion)

> Se corre cuando estén implementados los Lotes 0 a 4 del plan [Correcciones de la prueba del RDT en PS-0001](../01-planes/2026-10-21-correcciones-prueba-rdt-ps0001.md). Repite la prueba del 19.10 ([plan](02-prueba-rdt-ps0001-plan.md), [ejecución](03-prueba-rdt-ps0001-ejecucion.md)) con las mejoras ya aplicadas y con esperados que **no** salen de la app.
> Calculador de esperados: `scripts/esperados_rdt_ps0001.py` (ver [scripts/README.md](../../../scripts/README.md)). Verificado el 2026-10-21 contra el plan original: EV, PV, personal, equipos y transversales coinciden al centavo.

## 0. Reglas del juego (lo que falló la vez anterior)

1. **Los esperados se fijan antes y no se tocan.** Antes del primer RDT se corre `python scripts/esperados_rdt_ps0001.py --json > esperados-v2.json` y se guarda en la carpeta de evidencia. Si la app difiere, es hallazgo; no se recalcula el esperado «para que cuadre».
2. **No se sustituyen personas ni cargos.** Cada cargo del guion se carga con una persona real que tenga ese cargo (o su equivalente declarada para el servicio). Si no hay, se anota y no se improvisa.
3. **Se compara en las cinco pantallas** (Status, PR, Dashboard, Curva S, Plan Maestro) tras cada validación, y se llena `observados-v2.json` con lo que se lee.
4. **Cada diferencia lleva una causa verificada** (dato, regla o error) o queda como «sin explicar».

## 1. Precondiciones

| # | Condición | Quién |
|---|---|---|
| P1 | Los 5 RDT de la prueba anterior rechazados o borrados, y PR recalculado en cero. **Cumplida (2026-10-21):** los 5 RDT se borraron por script (`scripts/prueba_rdt_ps0001/limpiar.py`) con respaldo previo | Victor |
| P2 | Supervisor a cargo de PS-0001 decidido (Braulio o López Cáceres) | Victor |
| P3 | Equivalencias de cargo del servicio declaradas en Importar DP: OPERARIO → OPERARIO CIVIL, OFICIAL → OFICIAL CIVIL, INGENIERO DE SEGURIDAD → INGENIERO SSOMA | Victor (con la pantalla del Lote 2) |
| P4 | Lotes 0 a 4 desplegados en producción (anotar el commit) | Orquestador |
| P5 | Personas del catálogo con los cargos del guion: CAPATAZ, OPERARIO CIVIL (2), OFICIAL CIVIL (2), PEON (2), OPERADOR DE LINEA AMARILLA, INGENIERO SSOMA | Victor |
| P6 | Plan Maestro APROBADO, servicio en EJECUCIÓN, DP con costos | Orquestador |

## 2. Calendario

Hoy es 21.10.2026 al escribir esta guía. La fecha futura está bloqueada, así que **cada RDT se carga el día que corresponde o después**: D1 (19.10), D2 (20.10) y D3 (21.10) pueden cargarse ya; D4 (22.10) y D5 (23.10) cuando llegue su fecha. Si se corre antes, el esperado de cada día sigue valiendo, pero las pantallas solo mostrarán los días ya cargados.

## 3. Recorrido (igual al del 19.10, con cargos y datos de [plan 02, sección D](02-prueba-rdt-ps0001-plan.md))

| Día | Qué se carga | Se prueba además |
|---|---|---|
| D1 19.10 | PT-01 guía 6,0 de 8,9 con CNC; 3.1 1 und; C vinculada | Autocompletado de «Met. prog.» y de la descripción; «Met.», «Met. acum.» y «Avance del paquete» del **paquete** (30), no de la partida (267); el equipo se carga **sin elegir partida** |
| D2 20.10 | v1 con 9,5 ml → rechazo con motivo → corrección a 8,9; inasistencia; retro con stand-by | El motivo del rechazo se ve en la fila del Status y en «Revisar RDT»; ese RDT rechazado no suma su metrado al acumulado; HM del Status = operativas + stand-by |
| D3 21.10 | 10,0 ml (mayor que lo programado); HH extra 2 h; NC; **restricción escrita en la actividad** | La restricción crea `PS-0001-RE-n` en Pendiente y aviso; aparece en Informes (cierra el «pendiente de verificación» del Lote 0) |
| D4 22.10 | Cierra PT-01 y 3.1; PT-02 parcial con CNC | Dos paquetes en un RDT; columna «Paquete» del Status menciona la directa |
| D5 23.10 | PT-02 8,9 ml; 3.2 completa; 2 PEON | Cierre de 3.2 |

## 4. Pruebas negativas nuevas (además de las de D.8 del plan 02)

| Caso | Esperado |
|---|---|
| Crear un RDT con fecha de mañana (formulario) | El selector no la admite |
| Enviar esa fecha por API | 400 `FECHA_FUTURA` |
| Elegir una persona con un cargo sin tarifa en el presupuesto (p. ej. TOPOGRAFO) | Se rechaza con el mensaje que indica declarar la equivalencia; no se guarda |
| Importar un presupuesto con un cargo que no existe en el catálogo | El import se bloquea y el aviso nombra el cargo |
| Importar con un cargo del personal sin fila en el presupuesto y sin equivalencia | El import se bloquea y el aviso nombra el cargo |
| Equipo: intentar indicar partida | La opción ya no existe |
| Curva S semanal con un RDT del lunes | Fila «S1 al <fecha>» con PV, EV y AC al mismo día; sin «posterior a la fecha de corte» |
| Dashboard «Recursos sin tarifa» | Lista con nombres (vacía si todo resuelve) |
| Validar con un recurso sin tarifa (equipo no resuelto) | Llega el aviso `RDT validado con recursos sin tarifa…` a administrador y jefe de proyectos |

## 5. Dónde leer cada dato

| Dato | Pantalla |
|---|---|
| EV, % físico, PV, SV, SPI, AC por tipo, CV, CPI, HH reales, HH ganadas, IP | PR del servicio |
| Avance, programado, IP, HH, PPC, Pareto, recursos sin tarifa | Dashboard |
| Lectura de la semana | Curva S (granularidad semanal y diaria) |
| Real y programado por paquete y día | Plan Maestro |
| Estado del RDT, HM, personas, HH | Status de RDT |

## 6. Cómo comparar

1. Tras validar cada día, se anotan los valores del PR en `observados-v2.json`, con las claves del calculador (`ev`, `pct_fisico`, `pv`, `sv`, `spi`, `ac_personal`, `ac_equipos`, `ac_transversales`, `ac_materiales`, `ac_total`, `cv`, `cpi`, `hh_reales`, `hh_ganadas`, `ip`):

   ```json
   {"D1": {"ev": 1284.44, "ac_personal": 681.6, "hh_reales": 48}}
   ```

2. `python scripts/esperados_rdt_ps0001.py --comparar observados-v2.json` imprime OK/FALLA por dato; sale con código 1 si algo falla. Tolerancias: montos y HH 0,02; índices 0,005; porcentajes 0,02 puntos.

3. Esperados de referencia (regla nueva de HH, materiales 5.389,32; el calculador es la fuente, esto es solo una vista):

| Dato | D1 19.10 | D2 20.10 | D3 21.10 | D4 22.10 | D5 23.10 |
|---|---|---|---|---|---|
| EV | 1.284,44 | 2.978,37 | 4.827,61 | 6.549,78 | 8.287,52 |
| % físico | 3,22 | 7,46 | 12,09 | 16,40 | 20,75 |
| PV (corte = ese día) | 1.693,93 | 3.387,85 | 5.081,78 | 6.775,70 | 8.513,44 |
| SPI | 0,758 | 0,879 | 0,950 | 0,967 | 0,973 |
| AC personal | 681,60 | 1.363,20 | 2.257,80 | 2.939,40 | 3.810,76 |
| AC equipos | 379,44 | 758,88 | 1.159,32 | 1.838,76 | 2.608,60 |
| AC transversales | 311,07 | 721,30 | 1.169,16 | 1.586,23 | 2.007,08 |
| AC materiales | 173,36 | 401,98 | 651,57 | 884,01 | 1.118,54 |
| AC total | 1.545,47 | 3.245,37 | 5.237,85 | 7.248,40 | 9.544,98 |
| CPI | 0,831 | 0,918 | 0,922 | 0,904 | 0,868 |
| HH reales | 48 | 96 | 156 | 204 | 268 |
| HH ganadas | 31,99 | 73,53 | 118,71 | 160,92 | 211,27 |
| IP | 0,666 | 0,766 | 0,761 | 0,789 | 0,788 |

   Notas: el SPI y el PV de cada día suponen corte = fecha del RDT (fecha futura bloqueada). El CAPATAZ usa 15,38; el DP implica 15,39 (HH 74,04 por 1.139,78): una diferencia de ±0,01 por hora es redondeo, no hallazgo. El IP usa la regla nueva (sin HH de la transversal ni en reales ni en ganadas, a confirmar en el Gate 1 del plan); con `--regla-hh antigua` se obtienen los valores de la prueba del 19.10.

4. **Lo que ya se sabe que difirió el 19.10 y debe pasar ahora:** AC personal (era 2.020,66 por cargos sin tarifa), HH reales (era 290,72), IP (era 0,76), SPI del PR (era 4,89) y la Curva S semanal.

## 7. Automatización

El calculador y la comparación son un script que corre sin la app. El recorrido por pantallas se hizo con Playwright en la prueba anterior (notas de método al final de [03](03-prueba-rdt-ps0001-ejecucion.md)); en la sesión del 2026-10-21 el servidor de Playwright no conectó, por lo que **no hay un script de navegador verificado**. Si se quiere uno, se escribe en una tanda aparte y se prueba antes de confiar en él.

## 8. Cierre de la prueba

Informe `..._prueba-rdt-v2.md` junto al de la v1 en `01_pg_planeamiento/vpc_trabajo/servicios/PS-167-2026_.../`, con la tabla esperado/observado por día, el resultado de cada prueba negativa, lo que quedó sin probar y los RDT que hay que limpiar al terminar (los marcados «PRUEBA FUNCIONAL»).
