# Plan — Gestión documentaria (documentos pedidos, enviados, observados y aprobados)

## Identificación y estado

- Tema: apartado «Gestión documentaria» en `py_control_proyectos_web`, hermano de «Gestión de interesados».
- Fecha: 2026-10-25.
- Estado: `Implementada y desplegada` (2026-10-25), a la espera de la revisión de Victor (sin auditoría, por pedido suyo). **Pantalla rediseñada el 2026-10-25** (cuadro con una fila por documento, vista compacta y en casillas, correo en panel fijo a la derecha, «Otros correos» por tema y «Sin ubicar»): ver el flujo 24 y la última fila del registro de decisiones.
- Gate Spec: aprobado por Victor (2026-10-25) — pidió la interfaz, pidió «mejora mi idea», respondió las decisiones de una fila por documento, semáforo ajustable y área primero, y dijo «dale».
- Gate 1: aprobado por Victor (2026-10-25, «ok, continua»). Victor pidió no hacer auditoría ni revisión: él revisa las áreas y los documentos al final.
- Gate 2: pendiente.

## Referencia al Spec aprobado

Pedido de Victor (2026-10-25), en sus palabras: otra interfaz, en Planificación, que **extraiga en un cuadro la gestión documentaria** de los correos: qué correo **pide** algo, cuál **responde**, cuál **observa**, cuál **aprueba**; un resumen ordenado de lo que está pendiente de aprobación, emisión, aprobado, etc., con filtros. Decisiones posteriores:

1. **Una fila por documento** (no por correo).
2. **Semáforo:** rojo a los 7 días por defecto, con un desplegable para elegir en cuántos días se enciende; cada documento muestra además una **nota** que dice de qué se trata.
3. Lo primero que se distingue es **a qué área le corresponde** y luego **qué documento es**: una ficha técnica pedida para SSOMA, para Oficina Técnica o para Calidad son documentos distintos.
4. Pocas columnas: cada documento es una ficha compacta que lleva el **correo, el remitente** y otros datos menores.
5. **Áreas:** **SSOMA** (incluye medio ambiente), Oficina Técnica, Calidad, **Administración** (incluye accesos y otros) y **Gerencia** (contratos y compras, por ahora); se afinan después.
6. La contratista usa **un correo por área**; el cliente puede que no. Se trata igual: el área se decide por quién envía, mirando la dirección **y** el nombre.
7. El correo se ve desde esta misma interfaz, en el panel lateral que ya existe, como lectura principal. Victor pidió además poder **ir al correo**: se agrega un botón secundario «Abrir en Gmail» en ese panel (lleva al mensaje del buzón correcto; funciona si esa persona tiene ese Gmail abierto en su navegador).
8. Esta interfaz es la **segunda de tres**: la 1 extrae y agrupa los correos (Gestión de interesados), la 2 es el seguimiento documentario (este plan) y la 3 muestra los archivos en jerarquía (plan `2026-10-25-repositorio-de-archivos-documentarios.md`, es lo siguiente). Las versiones de cada documento y la versión aprobada se resuelven en la 3.

## Objetivo, alcance y no alcance

- **Resultado esperado:** una pantalla por servicio que lista cada documento con su área, su tipo, su estado actual, a quién le toca mover, cuántos días lleva esperando (con semáforo) y la nota de qué trata.
- **Alcance:**
  1. Base de datos: documentos, relación nota ↔ documento, tabla «remitente → área» que aprende de las correcciones (`db/120_gestion_documentaria.sql`; el número se confirma al construir).
  2. Servidor: listado con filtros, creación y edición por el administrador, asignación de una nota a un documento, reglas de estado y de «a quién le toca», aprendizaje de remitente → área.
  3. Pantalla: ficha compacta por documento con historial desplegable; resumen por área; filtros; desplegable del semáforo; exportación a Excel.
  4. Carga inicial a partir de las 309 notas ya clasificadas (script local; los datos de correos no van al repositorio).
  5. Chip «Gestión documentaria» en el grupo Planificación, permisos, flujo 24 nuevo y actualización de los flujos 14, 16 y 23.
- **No alcance:** responder correos desde la app; redirigir a Gmail; que el agente Haiku en la nube arme los documentos nuevos (es la tarea posterior ya conversada); definir con detalle qué ve cada área (Victor lo afina luego); el servidor de adjuntos en R2 (otro pendiente del plan de Gestión de interesados).
- **Validación esperada:** pruebas automáticas de las reglas puras (estado, a quién le toca, días y semáforo, área por remitente); `tsc`, `eslint` y `vitest` sin errores nuevos; verificación en la app publicada con Playwright en PS-0002 y PS-0003.

## Diseño propuesto

**Estados del documento:** Solicitado → Enviado → Observado → Levantado → Aprobado. Se derivan de los movimientos de las notas del documento: Solicitud = Solicitado; Enviado = Enviado; Observado = Observado; Enviado después de una observación = Levantado; Aprobado = Aprobado. El administrador puede corregir el estado a mano.

**A quién le toca:** pasa a la parte contraria de quien escribió el último correo. Nosotros = remitente del dominio de la contratista; cliente = cualquier otro. Una solicitud del cliente le toca a la contratista; un envío de la contratista le toca al cliente. Aprobado = a nadie.

**Días esperando:** desde el último movimiento, mientras no esté aprobado. Rojo al llegar al plazo elegido (3, 5, 7, 10, 15 o 30; 7 por defecto), ámbar desde la mitad del plazo, verde antes. El plazo elegido se guarda en el navegador de cada persona.

**Área:** se decide por la dirección del remitente y, si no basta, por su nombre. Con la carga inicial se llena una tabla «remitente → área»; cuando Victor corrige un área, esa corrección queda para los correos que lleguen después. Lo que no se puede decidir queda en «Sin área» para que el administrador lo asigne.

**Ficha (dos líneas, poco ancho):**
- Línea 1: tipo y nombre del documento con revisión, chip del área, chip del estado, semáforo con los días.
- Línea 2: remitente, asunto y fecha del último correo, y «le toca a: nosotros / cliente».
- Debajo, la **nota** que explica de qué se trata.
- Al desplegar: historial de correos del documento (cada uno abre en el panel lateral existente) y adjuntos.

**Filtros:** servicio, área, tipo, estado, «a quién le toca», remitente, fechas, «solo pendientes». Arriba, un resumen por área (por emitir, esperando al cliente, observados, aprobados) que filtra al tocarlo.

**Tipos de documento:** plano, ficha técnica, procedimiento o PETS, informe, trámite, valorización y otros.

**Notas por asignar:** las notas de temas documentales de «Gestión de interesados» que aún no pertenezcan a un documento aparecen en un contador «Por asignar», para vincularlas a un documento existente o crear uno nuevo.

**Permisos (provisorio, igual que Gestión de interesados):** ver = administrador, jefe de proyectos, jefe de oficina técnica y supervisor de oficina técnica; gestionar = administrador (y jefe de proyectos según la nota ¹⁹ del flujo 14, hasta que se aplique la decisión final de «todos ven, solo el administrador edita»).

## Entorno, repositorios, ramas y worktrees

Trabajo directo en `main`, sin worktree (como en el plan anterior). Código en `py_control_proyectos_web`; documentación aquí. No se hace push hasta que la migración esté aplicada en Supabase (si no, la pantalla falla en producción); Victor aplica el SQL y se le da la ruta completa del archivo.

## Skills aplicables

`seguir-flujo-de-planes` (activación y antes del cierre), `cerrar-tanda` (al terminar cada tanda), `trasladar-hallazgos` (tanda final), `verificar-permisos-por-rol` (permisos del chip y de la ruta).

## Fases y dependencias

| Fase | Contenido | Depende de |
|---|---|---|
| F1 | Migración y tipos | — |
| F2 | Reglas puras con pruebas: estado, a quién le toca, días y semáforo, área por remitente | F1 |
| F3 | Rutas API (listar, crear, editar, asignar nota, exportar) | F2 |
| F4 | Pantalla, chip, permisos y matriz base | F3 |
| F5 | Carga inicial desde las 309 notas (script local) | F1, F2 |
| F6 | Flujo 24, flujos 14, 16 y 23, índices, evidencia y verificación en producción | F4, F5 |

## Equipo del plan

Orquestador (esta sesión, Sonnet 5.5). Sin Workers separados: el alcance es acotado y se construye en tandas pequeñas desde la sesión. Documentador en Haiku para la tanda final si hace falta.

## Archivos / componentes afectados

Nuevos: `db/120_gestion_documentaria.sql`, `src/lib/gestion-documentaria/*`, `src/app/api/gestion-documentaria/**`, `src/app/(workspace)/proyectos/[id]/gestion-documentaria/page.tsx`, `src/components/gestion-documentaria/*`, script local de carga inicial (fuera del repositorio o excluido de git si contiene datos). Modificados: `permisos.ts`, `registro-accesos.ts`, `matriz-base-flujo14.ts`, `cobertura-pantallas.ts` y sus pruebas, `db/README.md`. Documentación: flujo 24 (nuevo), flujos 14, 16 y 23, índice de flujos, `docs/README.md` (conteo de flujos), Matriz de permisos (artefacto; esta cuenta no lo abre, ver memoria).

## Punch List embebida

| # | Ítem | Verificación |
|---|---|---|
| 1 | Migración y tipos | SQL revisado, Victor lo aplica; tipos compilan |
| 2 | Reglas puras | `vitest` verde con casos de cada estado y del semáforo |
| 3 | Rutas API con permisos | Sin sesión 401; rol sin permiso 403; administrador 200 |
| 4 | Pantalla | Playwright: ficha compacta, nota visible, desplegable de semáforo, filtros, correo en panel lateral, ancho de Victor |
| 5 | Carga inicial | Conteo de documentos por área y por estado revisado con Victor |
| 6 | Permisos por rol | `verificar-permisos-por-rol` |
| 7 | Documentación | Flujo 24 y flujos 14, 16, 23 coherentes; Matriz anotada |

## Riesgos y bloqueos

- **Agrupar correos en documentos** exige juicio (qué correos son el mismo documento). La carga inicial la hace el Orquestador y Victor la revisa; los nuevos quedan en «Por asignar» hasta que exista el agente Haiku.
- **Áreas por remitente:** un mismo correo puede servir a varias áreas; se resuelve con la corrección manual que queda aprendida.
- **Matriz de permisos** sin acceso desde esta cuenta: se anota el chip nuevo en el flujo 14 y se avisa a Victor.
- **Migración:** hasta que Victor aplique el SQL no se empuja el código.

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-25 | Interfaz nueva «Gestión documentaria» en Planificación, junto a Gestión de interesados | Victor |
| 2026-10-25 | Una fila por documento; rojo a los 7 días con plazo elegible; la ficha lleva una nota de qué trata | Victor |
| 2026-10-25 | Primero el área y luego el tipo de documento; áreas: SSOMA, Oficina Técnica, Calidad, Administración (accesos y otros) y Gerencia (contratos y compras, por ahora); se afinan después | Victor |
| 2026-10-25 | Medio Ambiente se unifica con SSOMA: queda una sola área, **SSOMA** | Victor |
| 2026-10-25 | El área se decide por quien envía (dirección y nombre), igual para contratista y cliente; el correo se ve en el panel lateral, sin redirigir a Gmail | Victor |
| 2026-10-25 | AESA queda fuera de los 4 servicios | Victor |
| 2026-10-25 | Rediseño de la pantalla: a Victor no le gustó la lista de fichas. Quedó un cuadro con **una fila por documento** (no por correo) y su vida en casillas (pedido, envío, respuesta, nuevo envío, aprobado); lo que pedimos nosotros usa un ciclo corto (pedido, entregado); dos vistas con interruptor, **compacta por defecto**; el correo se abre en un **panel fijo a la derecha** y solo se desliza el panel central; ningún correo queda fuera (con archivo / sin archivo, «Otros correos por tema» y «Sin ubicar», sin crear «comentarios»); menos filtros (buscador, quién lo pide, área, estado); se quitan las tarjetas por área y el plazo del semáforo ajustable | Victor («continuemos, impleméntalo») |

## Enlaces a progreso y evidencia homónimos

Sin carpetas aparte: el avance está en este plan y la evidencia (conteos de la carga inicial y capturas de producción) se anota en el «Mensaje de cierre».

## Libro de hallazgos

### Mejoras (de trabajo)

- Ver una captura propia antes de entregar un cambio visual (banco temporal + Chrome headless) y las trampas de las escrituras en producción y de los comandos con marcadores: extraídas el 2026-10-26 a [`2026-10-26-ver-captura-y-escrituras-en-produccion.md`](../../03-aprendizaje-continuo/2026-10-26-ver-captura-y-escrituras-en-produccion.md).

### Reglas de negocio acordadas en esta tarea

Integrada el 2026-10-26 en el flujo 24 (sección «Las familias de documentos»): un documento agrupa por tema, con 15 familias fijas iguales en todos los servicios; los correos nuevos se asignan solos (hilo, luego familia del asunto); un tema que aparece una sola vez queda como documento propio. Además:

Las del apartado «Referencia al Spec aprobado» y «Diseño propuesto»; ya integradas en el [flujo 24](../../04-flujos-de-negocio/24-gestion-documentaria.md) (2026-10-25); el flujo 23 solo ganó el botón «Abrir en Gmail» y la mención de que una nota puede pertenecer a un documento. Contradicciones con lo ya escrito: ninguna detectada hasta ahora (el flujo 23 solo habla de temas y notas, no de documentos).

### Observaciones sobre la política

Ninguna.

### Carpetas/archivos huérfanos

Reportados a Victor el 2026-10-26, sin borrar nada: en la app, `scripts/revision/zz-agrupar.mjs` y `scripts/revision/zz-docs.mjs` (locales, sin commit; el primero quedó reemplazado por `reagrupar-familias.mjs`) y los archivos ajenos ya conocidos (`db/095`, `db/114`, `scripts/cargar-rq-ps108-fase2.mjs`); en este repositorio, las capturas sueltas de la raíz (`estado-ps0002.png`, `fuente-whatsapp-nuevo.png`, `gestion-interesados-panel.png`, `login-ojo-contrasena.png`, `prueba-sello-T3.jpg`, `restricciones-admin.png`), carpetas de evidencia sin commit de otros planes y los xlsx/pdf de cronogramas en «Informacion para pruebas».

## Informe de Auditoría

Pendiente.

## Mensaje de cierre

2026-10-25: app en `main` (3ed3353, Vercel en verde), `db/120` aplicada por Victor y carga inicial hecha: **93 documentos** (PS-0001 16, PS-0002 10, PS-0003 32 con notas de movimiento, PS-0004 43 según el ensayo; 53 quedaron «Sin área»). Verificado en producción en PS-0003 con el administrador: tarjetas por área, filtros (la tarjeta Oficina Técnica/Observados filtra 5 de 32), ficha de dos líneas con semáforo, historial, correo en panel lateral con botón «Abrir en Gmail» (el enlace se genera; falta que Victor compruebe que Gmail lo abre), pestaña «Por asignar» (20). Pendientes: Victor revisa áreas y documentos (hay falsos como «mail delivery subsystem» para borrar); el artefacto Matriz de permisos; permisos finales «todos ven, solo admin edita»; creación automática de documentos para correos nuevos; lo siguiente es el plan Archivos documentarios.

## Elementos postergados propuestos para planes futuros

- Agente Haiku en la nube que arme y actualice los documentos desde los correos nuevos.
- Afinar qué ve y qué hace cada área.
- Alertas cuando un documento pase a rojo.

## Handoff — 2026-10-26 (relevo de sesión)

**Objetivo y estado.** Gestión de emails (antes «Gestión documentaria», ruta `/proyectos/{id}/gestion-emails`). Victor pidió que, tras el cambio de nombre, conserve «la interfaz que ya existía». Se probaron dos versiones y Victor rechazó ambas: (1) la de tarjetas por área y ficha por documento (commit 3ed3353, restaurada en app 7a45824) y (2) la de la maqueta «Gestión documentaria — maquetas» (cuadro por documento, vista compacta o en casillas, correo en panel fijo; app a57f459/5c566b0, hoy publicada en ff6ebef). Verificado con diff que la (2) es idéntica, salvo nombres, a la que estaba en línea justo antes del cambio de nombre (5c566b0). No existe en el historial una tercera pantalla de correos publicada.

**Último commit.** App `ff6ebef` y docs `679660b`, ambos en `main`, sin diferencia con `origin` (0/0). Los archivos sin commitear son ajenos (xlsx/pdf de cronogramas, pngs sueltos, evidencias, `db/095`, `db/114`, `scripts/cargar-rq-ps108-fase2.mjs`): no se tocan.

**No terminado.** Se le preguntó a Victor cuál es la pantalla correcta (captura, o si se refiere a otra pantalla, p. ej. «Fuente-Gmail», antes «Gestión de interesados»). Sin respuesta. No se cambió nada más.

**Próximo paso.** Esperar la captura o la aclaración de Victor; recién entonces tocar el código. No volver a adivinar la versión: identificarla con evidencia antes de revertir.

**Leer.** Este plan, el flujo 24, la memoria `gestion-documentaria-estado.md` y `gestion-documentaria-arbol-maqueta-estado.md`.

## Actualización — 2026-10-26 (Gestión de Email reconstruida)

Victor aclaró lo que quería: la pantalla del artefacto «Gestión documentaria — maquetas» (vista compacta y en casillas, correo a la derecha), pero **ocupando poco espacio**, y el nombre **«Gestión de Email»** con E mayúscula. Se reconstruyó (app `7479d38`, en `main`): una sola tabla con tres grupos (Documentos, Otros correos por tema, Sin ubicar), casillas de dos líneas, columnas fijas al deslizar, casilla punteada de «quién tiene la pelota», y una sola barra de herramientas (vista, buscador, tres filtros, pestañas, Nuevo documento, Excel) más el aviso de cobertura con la leyenda en una línea. Se retiró `OtrosCorreosVista.tsx` (sus filas ahora son grupos del cuadro). Flujo 24 y el nombre en los flujos 14, 16, 25 y README actualizados. Verificado con tipos, lint y pruebas; **la revisión visual en producción la hace Victor** (el agente no inicia sesión con contraseñas). Pendiente: que Victor actualice el nombre en la Matriz de permisos.

**Ajuste de estilo — 2026-10-26 (corregido).** Victor rechazó las dos versiones anteriores: la primera comprimía de más y la segunda cambió al estándar del Plan Maestro (letra de 11 px) en vez de copiar la maqueta «Gestión documentaria — maquetas». Decisión final: **la maqueta manda en medidas** (columnas 130 · documento flexible mín. 250 · 120 · 90 · 160 · 150 · 120 · botón; texto de celda 13 px, nombre del documento 14 px, encabezado 12 px en mayúsculas, chips 11 px; casilla de 176 × 84 px con tres líneas: movimiento / «fecha · Cliente|Contratista» / clip + «con archivo» o «Sin archivo»; panel del correo de 400 px; banner verde «Ningún correo queda fuera» con la leyenda) y **los colores también son los de la maqueta** (fondo de tabla #111a2b, cabecera #16213a, grupos #0e1626, chips por movimiento y estado con los mismos hex; módulo `colores.ts` en la app). Las fechas van en corto («02 oct»). Al pasar el mouse sobre una casilla sale un cuadro propio (asunto en negrita, nota y «Clic para abrir el correo»). El encabezado de la página (migas, título, descripción) queda a la izquierda y a la derecha el interruptor de vista y el buscador, como en la maqueta. Los filtros, «Por asignar», «Nuevo documento» y «Excel» se conservan en una fila compacta bajo el aviso. El panel del correo es propio de esta pantalla (CORREO + ✕, asunto de 17 px, De/Para/Fecha, caja «Nota para revisión rápida», cuerpo, «Archivos del correo» con Descargar, «Abrir en Gmail» y las acciones como «Quitar del documento»). **Verificación visual (app 2026-10-26, `b3635ba`):** esta vez sí se vio el resultado — banco local temporal con los datos de la maqueta y Chrome sin ventana por CDP, capturas a 1366 px de ancho de la vista compacta, la vista en casillas, el cuadro al pasar el mouse y el panel derecho, comparadas con la maqueta; el banco se borró y el middleware quedó intacto. Diferencias que no se igualaron por falta de datos: la maqueta dice «N archivo(s)» y la app solo sabe «con archivo» (no hay conteo de adjuntos), «Ver el hilo completo» no existe como función, y el chip «Entregado» no existe en el modelo de movimientos. Victor revisa en la app publicada (su zoom o ancho distinto puede cambiar el aspecto).
**Segunda ronda (app `1f46f21`):** la pantalla usa todo el alto (`data-area-completa`, igual que el Plan Maestro), así que el botón del asistente flota encima y ya no reserva una franja vacía abajo; la tabla tiene scroll propio en ambos sentidos con la barra horizontal siempre visible al pie y la cabecera fija. Verificado con capturas a 1366 × 560.
**Tercera ronda (app `ec67cfb`):** la cabecera del panel del correo es fija y tiene «Abrir en Gmail», «Descargar archivo» (desplegable con la lista si son varios) y cerrar; se quitó la sección «Archivos del correo» del cuerpo. El cuadro con la nota de la casilla se dibuja en el `<body>` con posición calculada, para que no lo recorten los contenedores con scroll (en la app publicada no se veía). Verificado con capturas a 1366 px.
**Cuarta ronda (app `7768298`):** (1) nuevo filtro «Último mov.» (Pedido, Enviado, Observado, Aprobado, Informativo) que mira el movimiento del último correo de cada fila; con él activo se ocultan los correos sin nota. (2) «Abrir en Gmail» daba 404 («cuenta no disponible») porque el enlace usaba `/mail/u/{correo}/#all/{id}`; ahora usa `mail/?authuser={correo}#search/rfc822msgid:{Message-ID}`, que no depende del número de cuenta abierto y sirve en cualquier buzón (si el correo no tiene Message-ID se usa el identificador interno). No se pudo probar contra el Gmail de Victor; él confirma.
**Agrupación por tema en PS-0003 (aplicada el 2026-10-26 por Victor; verificada: 16 documentos):** de 32 documentos pasan a 16 (Planos ×4→1, Cronograma ×4→1, Contrato y adjudicación ×3→1 más 2 correos del tema «Contrato y garantías», Plan y dossier de calidad ×2→1, Movilización/migración/acceso de personal y vehículos ×7→1, y áreas asignadas a lo que estaba «Sin área»); el reporte semanal deja de ser documento. Respaldo previo guardado antes de aplicar; script `scripts/revision/zz-agrupar.mjs` de la app (local, sin commit). Victor lo ejecutó él mismo.
**Familias de documentos para todos los servicios (app `fd65523`, 2026-10-26):** Victor pidió que el agrupamiento por tema valga para todos los servicios y que el sistema lo use al actualizar. Se analizaron los 4 servicios y la lista quedó en 15 familias (las 5 de PS-0003 más Lista de contactos y coordinación, Visita técnica, Informes técnicos e inspecciones, Entregables y codificación de documentos, Plan de trabajo y memoria descriptiva, Fichas técnicas, Cotizaciones y pagos, Documentación SSO, Solicitud de ingreso FOCAM y Combustible; el código de contrato en 2PERSONNEL y la habilitación de personal se suman a Movilización; seguridad de excavaciones, operatividad de equipos y AITAE, a Documentación SSO). Los temas que aparecen una sola vez quedan como documento propio. Hecho: lista en `src/lib/gestion-emails/familias.ts` (9 pruebas); `asignarDocumentoAutomatico` en el servidor, llamado al crear cada nota en el sincronizador (primero por hilo, luego por familia del asunto, creando el documento con origen IA; reportes diarios y reuniones excluidos; si falla, la nota queda en Por asignar); script `scripts/revision/reagrupar-familias.mjs` (simula, respalda y aplica con `--aplicar`). Simulación de los 4 servicios: PS-0001 13→8, PS-0002 9→4, PS-0004 39→10 aprox.; PS-0003 casi sin cambios (renombres y 4 fusiones). Reagrupo aplicado por Victor el 2026-10-26 y verificado en la base con una segunda simulación (sin nada más que cambiar; ningún correo perdido: 32, 36, 134 y 109 correos con nota): PS-0001 13→7, PS-0002 9→4, PS-0003 16→15, PS-0004 39→11. Pendiente: que Victor lo revise en pantalla. Flujo 24 actualizado con la tabla de familias.
**Lección de método:** no entregar un cambio visual sin ver una captura; si la app real no se puede abrir, montar un banco temporal local con los datos de la maqueta.

## Handoff — 2026-10-26 (cierre de sesión)

**Estado.** Pantalla «Gestión de Email» terminada y publicada (app `fd65523`, docs hasta `30170f3`). Las familias de documentos están en el código, en el sincronizador y aplicadas a los 4 servicios (PS-0001 7, PS-0002 4, PS-0003 15, PS-0004 11 documentos), verificado en la base.
**Pendiente de Victor.** Revisar la pantalla de cada servicio; confirmar que «Abrir en Gmail» abre el correo; actualizar la Matriz de permisos con el nombre «Gestión de Email»; R2 (pago), `CRON_SECRET` en GitHub, Fuente-Drive (paso 3) y la regla final «todos ven, solo el administrador edita».
**Pendiente mío (postergado).** Sugerencia automática de documento con el agente Haiku para lo que no encaja en una familia; «Por asignar» también muestra notas ENVIADO de temas como Reportes diarios.
**No tocar.** Archivos ajenos sin commit (ver Huérfanos).
