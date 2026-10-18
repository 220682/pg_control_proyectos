# Informe de Auditoría — Notificaciones: estándar de avisos y apoyo al supervisor operativo

Plan: [`2026-10-16-notificaciones-estandar-y-supervisor-operativo.md`](../01-planes/2026-10-16-notificaciones-estandar-y-supervisor-operativo.md). Auditor: Sonnet, esfuerzo medio. Fecha: 2026-10-18. Solo lectura; no se usó navegador ni servidor, y no se leyó `.env.local`, la memoria de cuentas ni `.playwright-mcp/`.

**Resumen en una línea:** el código de la rama `local-worker-7` está completo, aislado de `main` y en verde (2005 pruebas, `tsc` limpio, lint con los mismos 9 errores previos ajenos). Lo que impide cerrar limpio es **documental** (Punch List con 44 ítems en `Sin verificar` que ya están conformes, libro de hallazgos incompleto) y **tres cosas que solo Victor puede cerrar** (cambio de correo, artefacto «Matriz de permisos», limpieza de datos de prueba). No hay nada bloqueante en el código.

## Alcance auditado

Plan completo (Spec, Punch List de 71 ítems en 9 tandas, libro de hallazgos), 16 resúmenes de cierre (`resultados/T1A` a `T9`), progreso, evidencia (`03-evidencia/…/` y `t7/`), flujos 02, 03, 04, 05, 06, 07, 08, 12, 14 y 16, tabla `coherencia-flujos-codigo.md`, y el código de la rama `local-worker-7` del repositorio de la app (rutas de avisos, RQ, perfil propio, catálogo, migraciones 108 y 109). Queda fuera, por instrucción del brief, todo cambio ajeno sin commitear (flujos 09, 18, 19, 20, 22, parte de 14 y 16, `design.md`, mockups).

## Material revisado

* Plan, progreso y los 16 `resultados/*.md`. Capturas: solo se comprobó que existen por ítem (no se abrieron todas).
* App (`py_control_proyectos_web`, worktree `.worktrees/local-worker-7`, HEAD `9611338`, árbol limpio): `catalogo.ts` completo, `grupo-proceso.ts`, rutas `api/perfil/{route,contrasena,correo}`, `api/proyectos/[id]/requerimientos/[rqId]/{estado,comentarios}`, `api/notificaciones/{route,[id]/revisar}`, `derivar-logistica.ts`, `cambiar-estado-rq.ts` (recepción al abrir), `perfil-propio.ts`, `db/108` y `db/109`, y el código de `main` que consume `notificaciones` y el estado del RQ.
* Documental: flujo 04 completo, fragmentos de 05, 08, 13, 14; aprendizaje `2026-10-18-notificaciones-aprendizajes-de-trabajo.md`.

## Verificación de rama

Hecha con comandos, en este orden (primer chequeo del brief): **conforme**.

* `main` de la app sigue en `69ebf94` (igual a `origin/main`). `git rev-list --count main..local-worker-7` = **17** y `local-worker-7..main` = **0** (la rama está al día con `main`, 17 por delante).
* `git branch --contains` para los 17 commits del brief (`cc44f47`, `814efb4`, `c067583`, `69ce6aa`, `817e9d8`, `bcba4da`, `853bf57`, `e3c4dfa`, `04739ec`, `041e9e4`, `b6017c2`, `9529853`, `83bd0f9`, `21a0e59`, `1d036ec`, `85626fd`, `9611338`) devuelve **solo `local-worker-7`**. Ninguno está en `main`. `git log main..local-worker-7` lista exactamente esos 17 y ninguno más.
* Reparto por tanda (cada resumen de cierre nombra a Worker 7 y su tanda): T2 `cc44f47`/`814efb4`; T9 `c067583`; T4 `69ce6aa`/`817e9d8`; T6 `bcba4da`/`853bf57`/`e3c4dfa`; T6b `04739ec`; T3 `041e9e4`/`b6017c2`/`9529853`; T5 `83bd0f9`/`21a0e59`/`1d036ec`/`85626fd`; T7fix `9611338`. Las tandas de verificación (T1, T7) y de documentación (T8) no tocaron el código de la app. Ningún resumen indica que el Orquestador haya escrito código.
* Repositorio documental: `main`, 27 commits por delante de `origin/main` (0 por detrás); sin push todavía.

## Cumplimiento de SDD, plan, Punch List y evidencia

**Estado real de la Punch List (71 ítems), contrastado con los resúmenes y la evidencia:**

| Estado | En el plan hoy | Real según resultados |
|---|---|---|
| Conforme | 21 | **65** |
| Observado | 4 | **5** |
| Sin verificar | 46 | **1** |

* **Conformes que el plan aún marca `Sin verificar` (44):** T1-07 (maqueta aprobada por Victor el 2026-10-18), T3-01 a T3-09, T4-01 a T4-07, T5-01 a T5-08 (la 109 está aplicada y se usó en vivo), T6-01 a T6-08 (T6-02, T6-03 y T6-07 salieron `Observado` y se resolvieron con T6b y las decisiones de Victor; T7-05 confirmó los cierres en vivo), T7-01 a T7-06, T7-08, T8-01, T8-02, T8-03 y T8-08.
* **Siguen Observados (5):**
  * T1-01: 2 de 6 cuentas (tope de correos de Supabase); el Orquestador decidió probar con las existentes más roles temporales. No hubo cuentas reales de jefe de proyectos, jefe de oficina técnica ni segundo supervisor operativo.
  * T7-09: cambio de correo en espera de Victor (ver abajo).
  * T8-05: artefacto «Matriz de permisos» no actualizado.
  * T8-06: el libro tiene filas `Pendiente de decisión` (y le faltan hallazgos; ver APLICAR AHORA).
  * T9-04: las capturas del perfil son a 1440 px (T7C); **no hay captura a 390 px** de los tres bloques del perfil, que el ítem exige.
* **Sin verificar de verdad (1):** T7-07 (limpieza de datos de prueba, no ejecutada).
* **Cambios de alcance durante el plan (todos con registro):** T9 (3 ampliaciones de Victor), T3-08 y T3-09 (de T1B), T6b (decisiones del 2026-10-18), T7fix (grupo estable, cantidad vieja tras reenviar, respuesta atrasada de la bandeja, rótulo «Jefatura» del panel izquierdo) y consolidado de RQ sin Devolver (R13). Q5 (dejar de avisar documentos de cierre) y Q4 (aviso de RDT registrado) se implementaron.

**Criterios de aceptación (15):** cumplidos con evidencia en vivo o en pruebas los 1 a 14 (el 6 con la salvedad de que la campana baja al recargar, no en la misma pantalla: T7B-H3; el 7 con cuentas por rol salvo jefe de proyectos y jefe de oficina técnica, probados con roles temporales y con pruebas de los 13 roles); **el 15 (cambio de correo con confirmación) queda sin cumplir** hasta la acción de Victor. El 9 se cumple «consta por qué no»: `informe.emitido` está reservado y documentado en el flujo 04.

**T7-09 (correo): se toma como pendiente de Victor, no como fallo del código.** Evidencia revisada en `resultados/T7C.md`: la ruta rechaza clave incorrecta, pide la actual, envía la confirmación, muestra «Pendiente de confirmar» y mantiene vigente el correo anterior (comportamiento correcto). El correo nuevo no entró aún; causas posibles ya anotadas por el Worker (segunda confirmación del correo actual por «secure email change», redirección del enlace a `localhost:3000` desde el servidor local, o enlace caducado). El resumen T7C está sin commitear (ver pendientes).

## Verificación de la revisión de fuentes de verdad por fase

**Libro de hallazgos (segundo chequeo):** no queda ninguna fila en `Registrada` (0 coincidencias). Mejoras M1 a M9: `Trasladada` al archivo `03-aprendizaje-continuo/2026-10-18-notificaciones-aprendizajes-de-trabajo.md` (8 puntos). Reglas R1 a R15: `Trasladada` a los flujos con enlace. Abiertas, esperando decisión: **R16, R17, P-1, P-3, P-4, P-5, P-6, P-7, P-8** (P-2 se puede cerrar: ver clasificación). Huérfanos O1 a O3: reportados a Victor, sin borrar nada. Conclusión: lo que el brief permite (solo `Trasladada` y abiertas listadas) se cumple para lo que está en el libro; **el libro está incompleto** (hallazgos de T7 sin anotar; ver APLICAR AHORA).

**Política de coherencia (AGENTS.md):**

* Flujos: 04 reescrito (22 eventos, 123 líneas), 05, 06, 12, 14 (filas de Devolver, Corregir y reenviar, Editar mi celular, Cambiar mi correo, Cambiar mi contraseña; notas 14 y 15), 02, 03, 07, 08 y 16 con «Jefatura». `python scripts/verificar-referencias.py`: 0 huérfanos, 0 enlaces rotos, 2 menciones sin archivo ajenas al plan. Observación: el flujo 13 (orden de trabajo) no menciona el aviso al supervisor operativo asignado, que T6-H7 pedía revisar; lo cubren 04 y 08.
* **Muestreo de 9 eventos del catálogo contra el flujo 04 y el código** (el brief pedía 6): `rq.pendiente_aprobacion`, `rq.comentario`, `rq.devuelto`, `servicio.asignado`, `servicio.retirado`, `rdt.validado`, `rdt.nuevo`, `rdt.recursos_sin_tarifa`, `checklist.completo`. Plantilla, destinatario, grupo (`grupoNav` literal en cada ruta) y cierre coinciden con el flujo; el recuento del catálogo es 22 eventos, igual que en el flujo y en la tabla `coherencia-flujos-codigo.md` (22 de 22). **Una discrepancia flujo-código** (ver PROPONER A RESPONSABLE, V7): el flujo 05 dice que todo paso repetido da 409, pero «Aprobar» repetido responde 200 (idempotente).
* **Flujo 14 y artefacto «Matriz de permisos»: NO van juntos todavía.** El flujo 14 está al día; el artefacto no pudo abrirse con la cuenta del Orquestador (T8B, verificado el 2026-10-18). Se reporta como **pendiente de Victor**, no como cumplido. Las filas exactas están en `resultados/T8B.md`.

## Clasificación de hallazgos

### APLICAR AHORA

(Documental, sin decisión de negocio; lo hace el Orquestador antes del Gate 2. Yo no edité el plan por mi rol.)

1. **Actualizar la Punch List del plan** a los estados reales (tabla arriba): 44 ítems pasan de `Sin verificar` a `Conforme` con el enlace a su resumen de cierre; T7-09 y T9-04 quedan `Observado` con su causa; T7-07 queda `Sin verificar`.
2. **Poner al día el encabezado y los cierres del plan:** la línea «Estado» arrastra el historial de «Planificando» y «No hay Workers, ramas ni migraciones todavía»; «Siguiente paso» sigue en el Gate 1; la «Tabla de esfuerzos reales usados» dice «pendiente» en las 9 tandas; «Informe de Auditoría» dice «Pendiente» (enlazar este archivo). En el progreso, la tabla dice T7 «En curso» y T1C «falta que Victor la apruebe» (ya la aprobó), y el registro no anota T7fix, T7C ni el cierre de T8B.
3. **Completar el libro de hallazgos** con lo que está solo en los resúmenes: T7B-H1 (el aviso de prueba de `PS-0005` llegó a la cola de supervisores operativos, incluida una persona real), T7B-H2 (el formulario «Adjudicar servicio» muestra `PS-0001` pero el servidor crea `PS-0005`), T7B-H3 (la campana baja al recargar), T7B-H5 («Editar checklist» exige responsable aunque el documento ya tenía rol), T7B-H7 (el servicio de prueba consumió el N° real `PS-0005`), T7C-H1 (en local el enlace de confirmación apunta a `localhost:3000` si falta `NEXT_PUBLIC_SITE_URL`), T3-H7 y T8B-H3 (`puedeEditarPerfilExtendido` quedó sin uso: añadir como huérfano O4, sin borrar). Los que son método (roles temporales y revertir, entrar con cuenta en una sola llamada, URL de redirección del correo en pruebas locales) van al archivo de aprendizaje.
4. **Commitear la evidencia del plan que sigue suelta:** `resultados/T7C.md` (modificado) y las tres capturas `t7c-09-p7/p8/p9-*.png` (sin seguimiento). Son de este plan y no las toco yo.
5. **Cerrar P-2** en el libro: el celular se guardó y persistió tras recargar con un rol que antes no podía (T7C, `t7c-09-p2/p3`), lo que confirma que el `PATCH /api/perfil` con el cliente de administrador funciona.
6. **Flujo 13:** agregar una línea de remisión al aviso de asignación (o dejar anotado que no hace falta porque lo cubren 04 y 08).

### PROPONER A RESPONSABLE

(Decide Victor, o Victor con el Orquestador, en o antes del Gate 2.)

* **V1. Cambio de correo (T7-09).** Acción de Victor: abrir en `victor.sup22@gmail.com` el correo de confirmación hacia `+logistica1b`, y mirar si llegó un segundo correo dirigido a `+logistica1` (confirmación doble) y abrir también ese. Si no llega o falla, repetir el cambio con el servidor de la rama escuchando en la URL del enlace. Después falta: ingreso con el correo nuevo, comprobar que el anterior ya no entra, que `/mi-entorno?code=` no deja error visible, y actualizar la fila de Logística 1 en la memoria de cuentas. Si prefiere cerrar sin esto, el Gate 2 debe aceptar el criterio 15 como parcialmente verificado (ruta y estado «pendiente» probados; efecto final no).
* **V2. Artefacto «Matriz de permisos».** Aplicar las filas de `resultados/T8B.md` (Editar mi celular, Cambiar mi correo, Cambiar mi contraseña, Devolver RQ, Corregir y reenviar RQ devuelto, y las filas de interfaces pendientes de otros planes) o compartir el artefacto como editor con `victor.sup22@gmail.com`. Hasta entonces la política «flujo 14 y matriz van juntos» queda **incumplida de forma declarada**, no resuelta.
* **V3. Limpieza de datos de prueba (T7-07, Q6) y qué queda en producción.** La recomendación (conservar cuentas, eliminar datos «PRUEBA», archivar el servicio) ya la aprobó Victor en el Gate 1 pero no se ejecutó. Hay que autorizarla de forma explícita porque «Eliminar proyecto» es destructivo. Lo que está hoy en producción: servicio `PS-0005` «PRUEBA T7» (consume el N° real: el próximo servicio real saldrá como `PS-0006`); RQ `PS-0000-LL-SO-001` (Atendido), `-002` (Atendido) y `-003` (Solicitado); RDT de `jeyger22` del 17-10 (validado) y del 14-10 (rechazado) en `PS-0000`, con 8 h de una persona real del personal y sobre una actividad del Plan Maestro (puede alterar mínimamente el acumulado de ese servicio de prueba); mensaje de «Entorno» al administrador; comentarios y avisos; cuentas `+logistica1` (celular `999000111`, correo pendiente) y `+logistica2` (clave cambiada, anotada solo en la memoria); y un aviso de «falta subir» de `PS-0005` que llegó a la cola de todos los supervisores operativos (una persona real).
* **V4. R16 (D9) y R17 (D8).** Victor no ha respondido: al reemplazar un RDT se cierran los avisos «registrado» y «rechazado» del anterior (y «registrado» también al validar o rechazar), y un solicitante que además es de un rol de cola recibe dos avisos por un comentario. Hoy el flujo los documenta como comportamiento actual con la marca «por validar».
* **V5. Observaciones sobre la política.** P-1 (las pre-autorizaciones del Gate 1 no bastan para escrituras masivas en producción: añadir al estándar que se confirmen en el entorno o se entreguen como SQL; ocurrió con el cierre de los 18 avisos). P-3 (`cerrarAvisos` no cae al cierre por texto sin la migración 108; ya aplicada, así que el riesgo actual es solo que los avisos de checklist, RDT y `servicio.asignado` anteriores a T6b no tienen referencia y no se cierran solos: decidir si se cierran a mano o con una regla por texto). P-4/O1 (`marcar-visto` no cierra informativos: quitar el alias o igualarlo; hoy ninguna pantalla lo usa). P-5 (depende de V1). P-6 (`supervisor_ssoma` sin etiqueta en el perfil; arreglo de una línea, para un plan futuro). P-7 (columna de «lote» para unir filas de una tarjeta por rol; mejora futura, postergar). P-8 (= V2; la política no prevé que la cuenta del agente no pueda abrir el artefacto: proponer que Victor lo comparta como editor de forma permanente).
* **V6. Endurecimiento sugerido, no bloqueante.** (a) Cambiar la contraseña con `updateUserById` no cierra las demás sesiones abiertas del usuario; evaluar cerrarlas. (b) `POST /api/notificaciones` sin servicio («Entorno») permite que cualquier rol envíe a cualquier usuario o rol, sin tope de largo del mensaje ni de envíos; el flujo 14 lo documenta así, pero conviene decidir un tope. (c) `PATCH …/estado` hace `await request.json()` sin protección: un cuerpo inválido da 500 en vez de 400 (patrón previo al plan).
* **V7. Aprobar un RQ dos veces o desde otro estado.** El flujo 05 (línea 27) dice que repetir un paso da 409; el código de «Aprobar» (`derivar-logistica`) responde 200 con `derivado: false` y `estado: "APROBADO"` (hay una prueba que lo exige: «aprobar dos veces no duplica»). Decidir si se corrige el flujo (comportamiento idempotente) o el código (409). No edité el flujo: contradice lo escrito y requiere consulta.
* **V8. Tres arreglos de T7fix sin verificar en vivo.** Los puntos del arreglo «cantidad vieja tras reenviar», «grupo estable en la tarjeta con dos roles» y «respuesta atrasada del filtro» se cubren con pruebas unitarias y compilación, pero T7C (posterior) no los volvió a mirar en pantalla. Una pasada corta con Playwright después del merge, o aceptar la prueba unitaria.
* **V9. Cuentas y alcance de la verificación en vivo.** Cuatro de seis cuentas de prueba nunca se crearon (`+jefeproy`, `+ofitec`, `+supop2`, `+admin2`); las reglas de jefe de proyectos y jefe de oficina técnica (por ejemplo, Devolver) solo se probaron con el administrador y con pruebas de los 13 roles. Aceptarlo en el Gate 2 o crear esas cuentas.
* **V10. `.playwright-mcp/` en el repositorio documental.** Hay 151 archivos de esa carpeta **con seguimiento** (91 `.yml`, 58 `.log`, 2 `.jpeg`), commiteados en planes anteriores (el último, 2026-10-02), aunque desde este plan la carpeta está en `.git/info/exclude`. No leí su contenido; sí comprobé que ninguno menciona los correos de las cuentas de este plan. Victor decide si se retiran del seguimiento y del historial antes del push de los 27 commits. Aparte, `login-ojo-contrasena.png` en la raíz es un archivo ajeno sin seguimiento.

### NO PROMOVER

* Lint: los 9 errores y 22 avisos son los previos de `main` y ajenos al plan. Verificado: de los 8 archivos con error, solo `ListadoRequerimientos.tsx` fue tocado por la rama, y su error (`useEffect` que llama `setFilasVista(filas)`, línea 117) existe idéntico en `main`.
* T7A-H4 (error del Worker, no de la app), T7C-H2 (el 400 en consola es la respuesta esperada de la API ante clave incorrecta), T7B-H4 (scroll horizontal interno en la tabla de «Corregir y reenviar» a 390 px: lo permite la regla de interfaz), T1A-H5, T1B-H4, T5-H4 a H6 (decisiones de implementación informativas), T2-H7 (salto de numeración 102 a 108 sin colisión).
* Los hallazgos de método ya recogidos en el archivo de aprendizaje (heredocs, CRLF y `[id]`: T3-H6, T4-H5, T5-H7, T8A-H8, T8B-H5): no duplicar.
* O2 y O3 (consulta de respaldo con columnas antiguas y comprobaciones de `api/areas`): reportados a Victor; sin acción en este plan.
* Resueltos y sin necesidad de registro adicional: T7A-H1 y T7B-(b) (cantidad vieja), T7A-H2 y T7B-(c) (grupo del aviso de aprobación), T7B-H6 (respuesta atrasada), T3-H1 y T3-H2 (grupo «Proyecto» → «Jefatura»), todos cubiertos por T5 y T7fix.

### PROPONER SKILL

1. **Comitear solo los hunks propios en archivos con cambios ajenos.** Se repitió en tres planes (Lote 4, Informes y este); la técnica robusta (aplicar las mismas sustituciones al archivo de trabajo y a `git show :archivo`, y actualizar el índice con `hash-object` y `update-index --cacheinfo`) está en el aprendizaje, punto 7.
2. **Edición de archivos en Windows desde el shell** (heredocs con comillas o `\`, CRLF, `git add` con `[id]` → `GIT_LITERAL_PATHSPECS=1`): reincide en al menos cuatro planes; hoy es solo una nota. Un Skill o una lista fija en el brief de código lo evita.
3. **Verificar avisos por rol, por los dos lados.** `verificar-permisos-por-rol` declara que su suplantación no alcanza a la bandeja; este plan usó un procedimiento propio (entrar con la cuenta de cada rol en una sola llamada, roles temporales que se revierten, contar por estado y no por `?visto=false`, no tomar snapshots con claves). Candidato a Skill hermano.

## Pendientes técnicos y documentales

**Técnicos**

* **Riesgos para el merge (paso 8), con evidencia:**
  * **Migraciones 108 y 109: aditivas e idempotentes** (`add column if not exists`, `create index if not exists`, restricciones creadas solo si faltan; la 109 reemplaza la restricción de estado por la anterior más `DEVUELTO`). Están aplicadas: lo confirmó Victor el 2026-10-18 y la evidencia en vivo lo respalda (un mensaje de «Entorno» solo es posible con `proyecto_id` nulo y el flujo Devolver/Reenviar de T7A solo funciona con la restricción nueva).
  * **Código de `main` en producción frente a la base ya migrada:** tolera `proyecto_id` nulo en las listas (el embebido `proyectos(numero,nombre)` es una unión izquierda y las pantallas ocultan el N° OT), pero un destinatario que no sea administrador no puede revisar ni atender un aviso de «Entorno» (responde «No tienes esta OT a cargo») y el enlace del aviso apunta a `/proyectos/null`. Frente a `DEVUELTO`, `normalizarEstadoRequerimiento` de `main` lo lee como Solicitado: **un RQ Devuelto sería aprobable con el código viejo**. Hoy, según los resúmenes, ningún RQ está Devuelto (el `-003` quedó Solicitado tras reenviar); conviene confirmarlo con una consulta (`select estado, count(*) … group by estado`) y no crear Devueltos en producción hasta desplegar la rama.
  * **Avisos viejos sin referencia:** los de checklist, RDT y `servicio.asignado` anteriores a T6b no se cierran solos (P-3); los de RQ viejos se cierran por texto exacto.
  * **Choques con otras ramas** (`git merge-tree`, sin tocar nada): con `local-worker-6` (Cronograma, migración 107) hay conflicto **solo en `db/README.md`** (línea de la tabla de migraciones; trivial). Con `local-worker-5` (permisos) y `plan-maestro-tres-paneles` los archivos en común con `local-worker-7` son **cero**; sus conflictos de fusión (dashboard, curva-s, costo-recursos, plan maestro) son los mismos que tienen contra `main` y no los causa esta rama. El checkout de `main` de la app tiene 19 archivos sin commitear de otro agente (informes, `globals.css`); ninguno coincide con los de esta rama.
  * **Orden recomendado:** merge de `local-worker-7` a `main` con permiso explícito de Victor (16a), desplegar, y recién entonces limpiar datos de prueba (V3), para no dejar el código viejo frente a una base con datos nuevos más tiempo del necesario.
* **Pruebas independientes (paso 6), ejecutadas por mí en el worktree:** `npm test` → 183 archivos pasan y 1 omitido; **2005 pruebas pasan**, 1 omitida (coincide con T7fix). `npx tsc --noEmit` → sin errores. `eslint` → 9 errores y 22 avisos, los mismos que `main` (8 archivos). **No ejecuté `next build`** para no pisar la carpeta `.next` del servidor de desarrollo del puerto 3000 que usa otro agente; me apoyo en los resultados de T3 a T7fix (la compilación pasó en cada tanda).
* **Calidad y seguridad (paso 5, por muestreo):** (a) `api/perfil/*` exige sesión (401), rol conocido (403) y valida el cuerpo; el celular rechaza cualquier clave que no sea `celular`; contraseña y correo usan siempre el id de la sesión; `devolver`, `reenviar` y `corregir` validan permiso, estado de origen (409), motivo (400, tope 500) y alcance; `revisar` solo recepciona si el rol es Logística, el aviso es de un RQ aprobado y con actualización condicional. (b) Ninguna contraseña se devuelve ni se registra (sin `console.*` con contraseñas en el diff de la rama; las respuestas de error son mensajes fijos). (c) Migraciones: ver arriba. (d) Sin secretos: `git grep` de patrones de claves JWT, `sb_secret_`, `sk-` y asignaciones literales no devuelve nada en la app ni en el repositorio documental (solo una clave de ejemplo en una prueba); el único `.env` con seguimiento es `.env.local.example`; los correos de prueba aparecen en los briefs y resúmenes **sin ninguna clave al lado** (la segunda columna de las tablas es el rol). (e) `cobertura-avisos.test.ts` (`SITIOS`) al día: la prueba pasa y T2 comprobó que falla si se agrega una llamada fuera del catálogo.
* Cuentas de prueba reales que quedan con datos de prueba: ver V3.

**Documentales**

* Pendientes del Orquestador: APLICAR AHORA 1 a 6.
* Antes del Gate 2: commit de la evidencia suelta (APLICAR AHORA 4) y decisión sobre el push de los 27 commits del repositorio documental (cuando se haga, `git status` y `git log origin/main..main` de ambos repositorios; el push del código requiere la autorización del Gate 2).
* El índice `04-auditoria/README.md` no lista este informe; lo agrega quien cierre el plan.
* Cambios ajenos sin commitear que **no** son de este plan y no se tocaron: flujos 09, 14 (hunks de recursos y descargas, con notas ⁷ duplicadas: T8B-H2), 16, 18, 19, 20, 22, `design.md`, mockups, `observaciones-victor-lote-3-plan.md`, planes del 2026-10-07, 10-14 y 10-18, `06-pruebas/`, material de apoyo y `login-ojo-contrasena.png`.

## Recomendación

**`Requiere corrección`** (menor y solo documental) hasta que el Orquestador aplique los puntos APLICAR AHORA 1 a 4 (estados reales de la Punch List, encabezado y progreso, libro completo, evidencia commiteada). Con eso hecho, el plan queda **listo para Gate 2** con estos pendientes explícitos para Victor: V1 (correo), V2 (Matriz de permisos) y V3 (limpieza y datos de prueba), más las decisiones de V4, V5 y V7. No hay hallazgos que bloqueen el merge del código: la rama está aislada, al día con `main`, en verde, y la base ya está migrada.
