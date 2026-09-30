# Progreso — Niveles, Paquetes, Plan Maestro (lienzo) y RDT desde el Plan Maestro

## Referencia al plan

- Plan: `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt.md` (19 tandas, 109 ítems, 4 carriles).
- Encargos: `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/` (índice de tandas, reglas de contexto, contratos por carril, protocolo de migraciones, un brief por tanda, carpeta `resultados/`).
- Specs aprobados: `…/2026-09-30-niveles-presupuesto-y-cronograma.md`, `…/2026-09-30-paquetes-y-plan-maestro-grilla.md`, `…/2026-09-30-rdt-desde-plan-maestro.md`.
- Evidencia y auditoría: se crean cuando haya algo que registrar (`03-evidencia/` y `04-auditoria/`, mismo nombre de archivo).

## Estado general y fase actual

- Gate Spec: aprobado por Victor (2026-09-30), los tres Specs.
- Gate 1: aprobado por Victor (2026-09-30): plan, tabla de cambios a flujos en bloque, carpetas de trabajo, migraciones aplicadas por los Workers.
- Carpetas de trabajo creadas (2026-09-30, autorizadas por Victor).
- **Ola 1 lanzada (2026-09-30):** F0-A (maquetas), F1-A (carril 1, puerto 3101), F3-A (carril 2, puerto 3102) y F2-A (carril 3, puerto 3103, con las migraciones 079 a 081). Estado del plan: «Implementando». Skills revisados por el Orquestador: `seguir-flujo-de-planes`. Pendiente: medir cada sesión y consolidar sus resúmenes aquí al llegar.

## Tabla de roles / Workers y estado

| Rol | Estado |
|---|---|
| Orquestador | Activo. Este chat llegó a ~564k de contexto; se recomienda traspaso a un chat nuevo antes de lanzar la ola 1. |
| Planner | Terminó el plan (y sus dos ajustes). No tiene más trabajo pendiente. |
| Workers | Ola 1: F3-A **cerrada** (7 ítems conformes, commit `72aace7` en `local-worker-2`, `resultados/F3-A.md`). F0-A, F1-A y F2-A **cortadas a medias** por el límite de uso de la cuenta (error 429, se reinicia 4:50 pm Lima): trabajo parcial guardado, tandas NO cerradas ni medidas. |
| Auditor | No asignado (va después de F5). |

## Skills revisados

Skills de `.claude/skills/` de `pg_control_proyectos`: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`. El repositorio de la app no tiene carpeta de Skills (comprobado). El Orquestador usó `seguir-flujo-de-planes` al pasar el Gate 1.

## Avances terminados

- Specs, plan, Punch List, briefs y contratos por carril; subidos a `main` de `pg_control_proyectos`.
- Política nueva aplicada al estándar: carpeta `04-auditoria`, revisión de Skills, resumen de cierre por tanda, flujo SDD con enlace al artefacto visual y primera lectura obligatoria en `AGENTS.md`, Skill `seguir-flujo-de-planes`.
- Protocolo de migraciones y credenciales escrito (`00-protocolo-migraciones.md`).
- Carpetas de trabajo de la app `local-worker-2`, `-3` y `-4` creadas desde `main`; `local-worker-1` ya existía. Las cuatro en `45c9e0a`, limpias, con `node_modules` enlazado al del repositorio principal y `.env.local` copiado (autorización permanente).

## Trabajo actual

Retomar la ola 1: relanzar F0-A, F1-A y F2-A con Workers nuevos que continúen desde el trabajo parcial (ver Handoff del 2026-09-30, segundo).

## Pendientes

1. **Lanzar la ola 1** (hasta 4 Workers a la vez): F0-A (maquetas de Niveles y Paquetes, trabaja en `pg_control_proyectos`, sin carpeta de la app), F1-A (carril 1, `local-worker-1`), F3-A (carril 2, `local-worker-2`), F2-A (carril 3, `local-worker-3`; escribe **y aplica** las migraciones 079–081: es la primera en el orden). Usar la «Plantilla del prompt de lanzamiento» del índice de tandas. Cada Worker usa `cerrar-tanda` y deja `resultados/<tanda>.md`.
2. **Reglas de permiso:** el sistema de permisos denegó al Planner tocar lo relacionado con credenciales; puede bloquear también a los Workers al aplicar migraciones. Victor pidió «ir viendo lo de las reglas». **Estado (2026-09-30):** el sistema impide que un agente modifique sus propias reglas de permiso (lo denegó al intentarlo); las reglas las agrega Victor, y el Orquestador ya le entregó la lista exacta (scripts `migrar_<tanda>.py` permitidos y lectura de la carpeta de credenciales prohibida). Comprobar con Victor, **antes de la ola 2** (F1-B y F4-A aplican migraciones), que las agregó. Si el sistema pide aprobación para un script, Victor lo aprueba en el momento o lo corre él con el prefijo `!` (ver el protocolo).
3. Victor revisa las maquetas de F0-A antes de las tandas de interfaz de Niveles y Paquetes, y las de F0-B antes del lienzo y del selector del RDT.
4. Medir cada sesión de Worker con el script de `…-paneles-servicio-persistente-briefs/medicion.md` (meta: ≤ 80 llamadas, ≤ 200k de contexto).

## Commits, ramas y worktrees usados

- `pg_control_proyectos`: `main`, último commit de este trabajo `f90090d`, sincronizado con GitHub.
- `py_control_proyectos_web`: `main` = `45c9e0a`, igual a `origin/main`. Ramas y carpetas: `local-worker-1` a `local-worker-4` en `.worktrees/`, todas en `45c9e0a`. Turbopack no corre con el `node_modules` enlazado: usar `--webpack` (por eso el navegador va solo en F5).

## Hallazgos registrados en el momento

- PS-0006 ya no existe (eliminado en la limpieza del plan de paneles). Quedan PS-0004 y PS-0005; todos los servicios existentes son de prueba; F5-B crea un servicio de prueba dedicado.
- Credenciales: están en `C:\Users\BRANDY\Downloads\DIARIO\entorno_variable.txt` (nombres `PR_DB_URL` y `SUPABASE_ACCESS_TOKEN`). **No abrir ni mostrar ese archivo.** El `.env.local` de la app no las trae.
- El servidor de base de datos de Claude (`postgresql`) no conecta porque su ruta en la configuración de Victor no existe; el real está en `D:\VICTOR\CLAUDE CODE\mcp_postgresql`. No hace falta para este plan. Victor decide si se corrige.
- El artefacto «Flujo SDD a Cierre» está desactualizado (no incluye `04-auditoria` ni la revisión de Skills). Victor decide si se actualiza.
- Otra sesión dejó sin subir un cambio en `04-flujos-de-negocio/14-accesos-y-restricciones.md` (sincronización del artefacto de la matriz). No es de este plan: no tocarlo ni incluirlo en commits.
- `Trazabilidad.xlsx` (Victor lo edita) aparece modificado: no incluirlo en ningún commit.

## Bloqueos, riesgos y decisiones requeridas

- Riesgo: permisos para migraciones (ver pendiente 2).
- Abierto sin bloquear: nombre del rol extra cuando un archivo trae más de 5 niveles.
- Idea de Victor (2026-09-30): las maquetas nuevas de Niveles y Paquetes tienen mejor diseño que las demás pantallas; unificar el estilo de todas en un plan aparte. No es de este plan; el Orquestador no la ha comparado aún.
- La nota sobre el plan semanal (3WLA) en `planes-futuros.md` no se agregó; solo si Victor lo pide.

## Próximo paso verificable

Con contexto limpio: leer este archivo y el índice de tandas, lanzar la ola 1 y comprobar que cada Worker crea su `resultados/<tanda>.md`.

## Medición de Workers (script de `medicion.md` del plan de paneles; metas: ≤ 80 llamadas, ≤ 200k de contexto, ≤ 12M de caché)

| Tanda | Sesión | Llamadas | Herramientas | Contexto máx. | Caché | ¿Cumple? | Nota |
|---|---|---|---|---|---|---|---|
| F3-A | `agent-aecdc3c15a32996b` | 14 | 15 | 99k | 1,1M | Sí | Cerrada (el resumen decía ~19 llamadas; manda la medición) |
| F0-A (1.ª sesión) | `agent-a8d82746485b2169` | 17 | 32 | 140k | 1,5M | Sí | Cortada por límite de uso |
| F1-A (1.ª sesión) | `agent-a46c4b15b573649e` | 12 | 22 | 114k | 0,9M | Sí | Cortada por límite de uso |
| F2-A (1.ª sesión) | `agent-a02847794eaaf438` | 23 | 25 | 117k | 2,0M | Sí | Cortada por límite de uso |
| F0-A (cierre) | `agent-a9251d5b33bb0a5e0` | 8 | 8 | — | — | Sí | sesión de cierre |
| F4-A | `agent-a4b8f156afc8bfd8f` | ~31 | 31 | — | — | Sí | migraciones sin aplicar |
| F1-B | `agent-afb2521e5141dc180` | ~40 | 41 | — | — | Sí | migraciones sin aplicar |
| F0-B | `agent-ac9205eddb66f403b` | ~34 | 43 | — | — | Sí | usó navegador (desvío menor) |
| F2-A (cierre) | `agent-abbaf56e5b94e969a` | 33 | 33 | — | — | Sí | sesión de cierre; migraciones sin aplicar |
| F1-A (cierre) | `agent-ae31f694a87b97cf3` | 10 | 10 | — | — | Sí | sesión de cierre |

## Ola 1, relanzamiento (2026-09-30, tarde)

Verificado con comandos antes de relanzar: `local-worker-1` en `61cdc02` (WIP F1-A, 9 archivos), `local-worker-2` en `72aace7` (F3-A), `local-worker-3` en `3dd2c00` (WIP F2-A, 8 archivos), `local-worker-4` intacta en `45c9e0a`; `main` de la app = `origin/main`; `pg_control_proyectos` sincronizado, solo `Trazabilidad.xlsx` modificado (no se incluye). Relanzados tres Workers (F0-A, F1-A, F2-A) con la instrucción de revisar el WIP y no rehacerlo; F2-A comprueba primero si las migraciones 079 a 081 ya existen en la base.

### Resultados consolidados de la ola 1

- **F0-A (maquetas de Niveles y Paquetes): cerrada, 7 de 7 ítems conformes** (`resultados/F0-A.md`). El Worker revisó el WIP `d0b700e` contra el brief y no hizo falta corregir nada. Verificación solo estructural (sin navegador, según el brief); el Orquestador comprobó además que en el ejemplo de 5 niveles el nivel 2 propone «Área». **Nadie ha abierto las maquetas a simple vista: Victor las revisa.** Seis preguntas de diseño para Victor en el resultado. Al aprobar: quitar «pendiente de aprobación» en `design.md` y `mockups/README.md`. Sin hallazgos nuevos. Sesión de cierre: 8 llamadas (medición del script pendiente de anotar).
- **F1-A (Niveles, lógica pura): cerrada, 6 de 6 ítems conformes** (`resultados/F1-A.md`, commit `57984ff` en `local-worker-1`, sin push ni merge). El WIP estaba completo; solo corrigió un error de tipo en una prueba. Verificado por el Orquestador: árbol limpio, `tsc` en 0, 23 pruebas del módulo verdes; el Worker reporta 72 archivos y 698 pruebas verdes en la suite y lint de 27 problemas, igual a los 27 que midió F3-A en una rama idéntica a `main` (ninguno en `src/lib/niveles`). `npm run lint` en el repositorio principal da 24585 porque recorre `.worktrees`: no sirve de base. Archivos reales de prueba: solo de 2 y 3 niveles; el caso de 5 niveles usa datos sintéticos rotulados. **Hallazgo para F1-B y F1-C:** Bancoductos tiene partidas directas de un subpresupuesto (p. ej. `1.3`) junto a paquetes de partidas; las pantallas no deben marcarlas como error. Sin reglas de negocio nuevas ni huérfanos.
- **F2-A (Paquetes, datos y API): cerrada; migraciones 079 a 081 ya aplicadas (comprobado)**. *Actualización 2026-09-30, tarde:* a pedido de Victor, el Orquestador corrió la consulta de solo lectura `migrar_F2-A.py check`: `select 1` correcto; existen `paquete_trabajo_vinculos` (0 filas) y las columnas `orden` y `nivel` de `paquetes_trabajo`; conteos sin cambios (`paquetes_trabajo` 0, `cronograma_actividad_partidas` 48, `cronograma_actividades` 65, `dp_partidas` 48). Por lo tanto la sesión cortada ya las había aplicado; no se corrió `apply`. Las políticas de la tabla no se consultaron. Script temporal borrado. El texto siguiente es el informe original del Worker, previo a esta comprobación:
   (`resultados/F2-A.md`, commit `73a8680` en `local-worker-3`, sin push ni merge). Ítems 2 a 6 conformes; el ítem 1 (migraciones 079 a 081) queda **Observado**: el clasificador de permisos denegó el script («Credential Exploration») y el Worker, según el protocolo, no lo rodeó. Verificado por el Orquestador: árbol limpio, `tsc` en 0, 41 pruebas de Paquetes verdes (el Worker reporta 72 archivos y 703 pruebas en la suite); el script y los tres SQL fueron leídos: el script solo lee `PR_DB_URL`, no la imprime y limpia los errores, y los SQL son aditivos (una tabla nueva y dos columnas nuevas). **Se desconoce si 079 a 081 ya existían en la base.** Pendiente de Victor: aprobar o correr con `!` `python "<scratchpad>\migrar_F2-A.py" check` y luego `… apply`; después borrar el script. Mientras tanto, `GET` y `POST` de paquetes fallarían en vivo (las pruebas son con datos simulados). Decisiones técnicas del Worker: `MOVER` vale en cualquier estado no archivado y `EDITAR`/`ARCHIVAR` solo en borrador (**el brief no lo fija: confirmar con Victor**); `PUT vinculos` trata lo recibido como estado final y rechaza quitar un vínculo que está en un paquete vigente. `vitest.config.ts` (congelado) no define el alias `@`: las pruebas de ruta usan `vi.mock`. `FormularioPaquetesTrabajo.tsx` sigue enviando la forma vieja y dejará de funcionar contra la API nueva: es trabajo de F2-B.

### Resultados consolidados de la ola 2

- **Permisos (2026-09-30, tarde):** Victor agregó con `/permissions` las cuatro reglas Allow de `migrar_*.py` (`check` y `apply`, en Bash y PowerShell) y las tres reglas Deny sobre la carpeta de credenciales y `entorno_variable`. Comprobado: `migrar_F4-A.py check` corrió sin bloqueo. F2-A y F4-A se bloquearon antes de que existieran.
- **F4-A (RDT, datos y real por clave): código cerrado, migraciones 082 a 084 sin aplicar** (`resultados/F4-A.md`, commit `a037e98` en `local-worker-4`, sin push ni merge). Ítems 2 a 5 conformes; ítem 1 **Observado**. Reportado por el Worker: 689 pruebas verdes, `tsc` en 0, lint 27 igual a `main`; 14 pruebas nuevas. Verificado por el Orquestador: los tres SQL (aditivos; 082 agrega `paquete_trabajo_id` a las actividades y a sus partidas, 083 agrega `es_derivada`, `declaracion_id` y `metrado_derivado` con un check, 084 solo índices) y `migrar_F4-A.py check`: `select 1` correcto, 082 a 084 no aplicadas, conteos `rdt_actividades` 86, `rdt_actividad_partidas` 33, `rdt_partes` 71, `paquetes_trabajo` 0, `dp_partidas` 48, `plan_maestro_partidas` 240. **No se aplicó `apply`:** los nombres de los campos derivados quedaron «por confirmar con Victor» (el Gate 1 no los fijó); se consultan antes.
  - **Riesgo para F4-B y F4-C:** `recalcular_pr_desde_rdt` (`db/053`, congelado) suma el metrado de la actividad por cada vínculo de partida; con filas derivadas contaría el metrado en cada partida derivada en vez de `metrado_derivado`. Hay que decidir cómo se guardan las derivadas (actividades derivadas propias) o autorizar un ajuste a 053. Decisión a llevar a Victor antes de F4-B.
  - El catálogo lee columnas de `plan_maestro_partidas` que crea el carril 2 (076 a 078); hasta aplicarlas devuelve `lineasPlanMaestro: []` con el error en `erroresParciales`. `partidas` y `subpresupuestos` se conservan para no romper `FormularioCrearRdt` hasta F4-C. `claveReporte` duplicada localmente: unificar en F5-A.
- **F0-B (maquetas del lienzo, paneles ocultables y selector del RDT): cerrada, 7 de 7 ítems conformes** (`resultados/F0-B.md`, commit `0fecae8` en `main` de `pg_control_proyectos`, verificado por el Orquestador: 3 maquetas nuevas, `design.md` v1.6.0, índice y README enlazados). El cálculo de la maqueta coincide con el anexo de 4 semanas (físico acumulado 22,56 / 48,78 / 76,22 / 100 %; económico 1 850 / 2 150 / 2 250 / 1 950 = 8 200; HH 172). **Desvío menor:** el Worker abrió las maquetas en un navegador con un servidor local temporal, ya detenido y limpio, aunque las reglas reservan el navegador a las tandas finales; sin efecto sobre datos ni archivos. Móvil verificado solo por CSS, no por captura. Seis preguntas de diseño para Victor en el resultado. Al aprobar: quitar «pendiente de aprobación» y «vigente cuando Victor apruebe» en `design.md` y `mockups/README.md`. Sin reglas de negocio nuevas ni huérfanos.
- **F1-B (Niveles: importación del DP y del cronograma, bloqueo de recarga): código cerrado, migraciones 073 a 075 sin aplicar** (`resultados/F1-B.md`, commit `2652116` en `local-worker-1`, sin push ni merge). Reportado por el Worker: 723 pruebas verdes (25 nuevas), `tsc` en 0, lint 27 igual a `main`. Ítems 2 a 6 conformes (los de lógica, sin ejecutar las rutas: `vitest.config.ts` congelado no tiene el alias `@/`, por eso la lógica se sacó a funciones puras y las rutas quedan para verificar en vivo en F5); ítem 1 **Observado**. Verificado por el Orquestador: árbol limpio, commit presente, y lectura de `075`: misma firma de 13 parámetros, `p_subpresupuestos` admite el arreglo histórico o el objeto nuevo (compatible con la app actual de `main`), solo borra en las tablas nuevas; `074` crea `servicio_encabezados` y una función, y escribe un mapa por defecto pendiente solo en tablas nuevas. **Script `migrar_F1-B.py`: aplica directamente, no tiene modo `check` y no encaja con las reglas Allow de Victor (`check` / `apply`); antes de usarlo hay que darle los dos modos.** El clasificador lo denegó al Worker (el candado se creó y se borró; no se aplicó nada). **Orden crítico:** la rama ya llama a `reemplazar_dp` con el objeto nuevo; sin la 075 aplicada, importar un DP falla, así que no desplegar ni probar la importación antes de aplicar las tres. La consulta de vínculos de `evaluarRecarga` usa una unión de PostgREST que no pudo probarse sin la base: verificar en vivo. La API nueva acepta `soloAnalizar`, `mapaNiveles` y `confirmarPerdida`, y responde 409 con `bloqueadoPorPlanAprobado` o `requiereConfirmacion` con `perderia` (insumo para F1-C).

## Decisiones de Victor sobre las maquetas (2026-09-30, tarde)

- **Maquetas de Niveles y Paquetes (F0-A), las seis preguntas:** aprobadas como se recomendaron. (1) Una fila de muestra por grupo de hermanas con botón «Ver N hermanas». (2) Las filas «para revisar» bloquean el botón de aprobar hasta resolverlas. (3) El restante por partida se muestra en ambas listas. (4) La marca de paquete alterna dos colores entre paquetes contiguos, más el borde. (5) En pantallas angostas, pestañas para Cronograma y DP. (6) El plegado de un paquete se reinicia al abrir la pantalla. Las cuatro maquetas de F0-A quedan **aprobadas**, con esos ajustes aplicados.
- **Lienzo del Plan Maestro (F0-B):** aprobado («el Plan Maestro me gusta»).
- **Paneles ocultables (F0-B), corrección:** no usar botones de texto en la barra (distorsionan el panel izquierdo). Un solo **icono por panel**, dentro del propio panel y en su **borde interior** (el lado que da al contenido), como el icono naranja de su captura, y que siga visible con el panel oculto.
- **Selector del RDT (F0-B), corrección:** **no se propone pantalla nueva.** Se usa la pantalla **Crear RDT que ya existe** (`FormularioCrearRdt`, que tiene más datos que la maqueta). Se conserva el cuadro «Elegir actividad del Plan Maestro» (paquetes plegables con sus partidas, directas aparte, modo «por avance del paquete»), que a Victor le gusta, abierto desde esa pantalla.
- **Seguimiento:** tanda de ajustes de maquetas (F0-R) por lanzar cuando Victor responda las cinco preguntas restantes de F0-B. La idea de unificar el estilo de todas las pantallas sigue registrada para un plan aparte.

## Migraciones aplicadas (2026-09-30, tarde; las aplicó el Orquestador con autorización de Victor y el candado del protocolo)

- **Por qué el Orquestador y no los Workers:** el sistema denegó los scripts a los Workers de F2-A, F1-B y F4-A antes de que Victor agregara sus reglas de permiso; Victor aprobó aplicarlas («aplica las migraciones») y con ese aviso se corrieron los mismos scripts, que lee y limpia credenciales (solo se usa el nombre de la variable `PR_DB_URL`), vía directa, cada archivo en su transacción, con candado (creado y borrado), scripts temporales borrados y árboles de trabajo limpios.
- **079 a 081 (Paquetes, F2-A):** ya estaban aplicadas (las aplicó la sesión cortada); comprobado por consulta.
- **082 a 084 (RDT, F4-A):** aplicadas. Existen `paquete_trabajo_id` en `rdt_actividades` y en `rdt_actividad_partidas`, `es_derivada`, `declaracion_id`, `metrado_derivado`, el check `rdt_actividad_partidas_derivada_declaracion_chk` y tres índices. Conteos antes y después iguales (`rdt_actividades` 86, `rdt_actividad_partidas` 33, `rdt_partes` 71, `paquetes_trabajo` 0, `dp_partidas` 48, `plan_maestro_partidas` 240). Nombres de los campos derivados: se dejan como se propusieron (Victor aprobó aplicar sin objetar los nombres).
- **073 a 075 (Niveles, F1-B):** aplicadas. Antes de aplicar se leyó completa la 075 y se comparó su cuerpo con el de `reemplazar_dp` de la 071 vigente: solo agrega los borrados en las tablas nuevas, el soporte del objeto nuevo y el mapa por defecto; nada del cuerpo actual cambió. Después: `reemplazar_dp` con **una sola firma de 13 parámetros**; creadas `servicio_niveles` y `servicio_encabezados` y la función `niveles_dp_por_defecto`; el único servicio con DP quedó con su mapa por defecto pendiente de confirmar (4 niveles, 8 subpresupuestos y 8 paquetes de partidas como encabezados); ningún servicio sin mapa. Conteos de los datos existentes iguales antes y después (`proyecto_dp` 1, `dp_partidas` 48, `dp_subpresupuestos` 8, `dp_paquetes` 8, `cronograma_actividades` 65, `cronograma_actividad_partidas` 48, `proyecto_pr` 2, `pr_partidas` 57).
- **Pendiente:** 076 a 078 (Plan Maestro, F3-B) y las reservadas 085 y 086. Comprobado solo lo anterior; las políticas de acceso de las tablas nuevas no se consultaron.
- **Mejora de trabajo:** un script de migración debe traer siempre los modos `check` (solo lectura, por defecto) y `apply`, para encajar con las reglas de permiso estrechas de Victor.

## Última actualización y responsable

2026-09-30, Orquestador.

## Handoffs

### Handoff del 2026-09-30 (Orquestador → Orquestador con contexto limpio)

- **Objetivo y estado:** ver «Estado general». Gate 1 cumplido; carpetas listas; ola 1 sin lanzar.
- **Qué leer, en este orden:** la sección «Flujo con Orquestador» de `AGENTS.md` (con su primera lectura obligatoria) y el Skill `seguir-flujo-de-planes`; este archivo; `…-briefs/00-indice-de-tandas.md`, `00-reglas-de-contexto.md` y `00-protocolo-migraciones.md`. **No** releer los 21 flujos ni los tres Specs completos: los Workers leen solo lo que su brief nombra.
- **Terminado y no terminado:** ver «Avances terminados» y «Pendientes».
- **Pruebas ejecutadas:** ninguna de código todavía (no hay Workers lanzados). Se verificó: sincronización de ambos repositorios, carpetas de trabajo limpias, tamaños de briefs ≤ 8 KB.
- **Cómo habla Victor y cómo hay que hablarle:** lenguaje simple, sin códigos internos de ítems ni siglas, una decisión por pregunta con recomendación; verificar antes de afirmar; no declarar cerrado nada sin la lista de verificación del Skill.
- **Límites:** el Orquestador no implementa, no hace merge ni push de la app sin autorización en el Gate 2, no edita `AGENTS.md` ni los flujos por su cuenta.
- **Próximo paso concreto:** lanzar F0-A, F1-A, F2-A y F3-A con la plantilla del índice.

### Handoff del 2026-09-30 (segundo: Orquestador → Orquestador con contexto limpio)

- **Estado de la ola 1:** F3-A cerrada y verificada (commit `72aace7`, árbol limpio, 696 pruebas, `tsc` en 0; el lint lo tomó igual a `main` sin compararlo). Las otras tres se cortaron por límite de uso de la cuenta; ninguna escribió su `resultados/<tanda>.md`.
- **Trabajo parcial guardado (sin verificar, hay que revisarlo antes de seguir):**
  - F0-A: sin commit en `pg_control_proyectos` (se subió como «WIP F0-A» junto con este traspaso): maquetas `cronograma-niveles.html`, `importar-dp-niveles.html`, `paquetes-agrupar.html`, `paquetes-declarar.html`, más cambios a `design.md`, `mockups/README.md` e `index.html`. Falta comprobar contra el brief `f0-tanda-a.md` qué ítems están completos.
  - F1-A: commit `61cdc02` «WIP» en `local-worker-1` con `src/lib/niveles/**` (9 archivos, con pruebas). Sin verificar `npm test`/`tsc`.
  - F2-A: commit `3dd2c00` «WIP» en `local-worker-3` con `db/079`–`081` y `src/lib/paquetes-trabajo/` (5 archivos). **No se sabe si las migraciones 079–081 se aplicaron** (no hay resultado ni candado en `resultados/`); el Worker nuevo debe comprobarlo con `select 1` y consultas de existencia antes de aplicar, sin asumir.
- **Cómo retomar:** lanzar Workers nuevos con la plantilla del índice, añadiendo al prompt: «Hay trabajo parcial ya commiteado como WIP: revísalo contra tu brief, completa lo que falte y no lo rehagas». Puertos de prueba usados: 3101 a 3103 (el índice no los fija; el brief de F3-A dice 3112, sin efecto).
- **Límite de uso:** el reinicio fue 4:50 pm (Lima). Con 4 Workers a la vez se agotó la cuenta; considerar lanzar 2 o 3 a la vez.
- **Medición:** pendiente con `medicion.md` del plan de paneles; mide F3-A y las tres cortadas (anotar «cortada por límite»).
- **Commits:** nada de la app subido (sin push, sin merge). Ramas `local-worker-1` y `-3` con un commit WIP cada una; `local-worker-2` con F3-A; `-4` intacta.
- **Pendientes de Victor sin cambios:** reglas de permiso antes de la ola 2; maquetas de F0-A a su revisión; rol extra con más de 5 niveles; ruta del servidor de base de datos; nota 3WLA solo si la pide. Hallazgo nuevo (de F3-A): usar `git stash -u` en un árbol compartido es riesgoso (mejora de trabajo, consolidar al cierre).
