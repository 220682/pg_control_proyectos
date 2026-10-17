# Resumen de cierre — Tanda F

## Tanda, rol y modelo

Tanda F (Informes, editor y vista), Ola 3, carril W3. Worker 3, Sonnet. Parte de `b455b98` (D y E incorporadas). La tanda G (descargas) no estaba incorporada.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| F1 | Observado | `EditorInforme.tsx` + `BloqueVista.tsx`: lista de bloques, hoja A4 de vista previa, bloques de datos del sistema. `tsc`, lint y build compilan; ruta `/proyectos/[id]/informes/[informeId]` listada. | En el borrador la API no entrega los valores de los bloques de datos (GET devuelve solo el informe; los datos se componen al emitir). La hoja muestra un aviso en esos bloques, no cifras. Sin captura ni base (098 a 102, sin cuentas). Pregunta H1. Lo cierra L. |
| F2 | Conforme (lógica) / Observado (en vivo) | Botones subir, bajar, ocultar y quitar; Alt+↑/↓ (Home/End) sobre el bloque; arrastrar. `editor-utils.test.ts` prueba mover, quitar, ocultar, agregar y teclado. | Recorrido real con teclado y captura: tanda L. |
| F3 | Observado | Bloques libres: TEXTO, FOTOS (asignación desde el banco del día), TABLA (filas y columnas), CLIMA_TURNO, FIRMAS; más edición de los bloques de datos que escribe el usuario (incidencias, semáforo, logros y alertas, restricciones, próximas, partida). | Las claves de `config` las definió esta tanda (ver H2); G debe leerlas igual. Sin prueba contra base. |
| F4 | Observado | Período cambiable (PATCH desde/hasta con errores y avisos del servidor), guardado automático (1,2 s, cola, estados guardando/guardado/error, no pierde cambios, aviso al cerrar), descarga con formato y alcance. | La ruta `/descargar` es de G: el botón apunta a `GET .../informes/[informeId]/descargar?formato=&alcance=` y dará 404 hasta incorporar G. Sin base. |
| F5 | Observado | «Mis formatos» en el editor (guardar los bloques con nombre; usar uno reemplaza los bloques, quitando los de costos que no correspondan) y en «Nuevo» (se elige uno y se crea con `formatoUsuarioId`). | Sin base ni sesión. Lo cierra L. |
| F6 | Observado | `VistaEmitido.tsx`: solo lectura desde la foto fija, rótulo de valores al corte, lista de versiones, aviso y enlace en un REEMPLAZADO, Nueva versión (POST `nueva-version`, luego abre el borrador), Emitir en el editor (guarda antes). `accionesInforme` probada con los 13 roles (editar, emitir, nueva versión propia y ajena, descargar, COSTOS). | Recorrido en vivo por rol: L. Los valores congelados se muestran con un visor genérico (forma de `datos` no documentada por bloque). |

Comandos finales: `npm test` 141 archivos / 1458 pruebas en verde (en una corrida, `inasistencias-route.test.ts` falló una vez por tiempo y pasó en cada repetición; el `.snap` de curva-s se restauró con `git checkout`); `npx tsc --noEmit` sin salida; `npm run lint` 9 errores y 22 avisos (línea base, ninguno nuevo); `npx next build --webpack` compila.

## Rama, commits y archivos tocados

Rama `local-worker-3`, push hecho. Commit `37a5ea8` (un solo commit para F1 a F6: los archivos se entrelazan). `git branch --contains HEAD` devuelve solo `local-worker-3`. Árbol limpio.

Archivos nuevos: `src/app/(workspace)/proyectos/[id]/informes/[informeId]/page.tsx`; `src/components/informes/{EditorInforme,VistaEmitido,BloqueVista,DescargarInforme}.tsx`, `editor-utils.ts`, `editor-utils.test.ts`. Editados: `ListadoInformes.tsx` (acción Descargar), `NuevoInforme.tsx` (Mis formatos y enlace «Abrir el editor»), `src/lib/config/cobertura-pantallas.ts` (la prueba de cobertura exige registrar la ruta nueva).

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| F-H1 | conflicto con un flujo o pregunta para el Responsable humano | GET de un borrador no entrega los datos de los bloques del sistema; la hoja del borrador no puede mostrar cifras reales antes de emitir. Se dejó un aviso por bloque. ¿Se quiere una vista previa con datos (nueva ruta de W1 que use `componerDatosPorTipo`)? | Orquestador / Victor; si sí, ruta de W1. |
| F-H2 | regla de negocio acordada | Claves de `config` de los bloques libres, fijadas en esta tanda: TEXTO `{texto}`, TABLA `{columnas[], filas[][]}`, CLIMA_TURNO `{clima, turno, observacion}`, FIRMAS `{firmantes[{nombre,cargo}]}`, FOTOS `{porPagina, mostrar}`; en bloques de datos con valor escrito: INCIDENCIAS/RESTRICCIONES/PROXIMAS_ACTIVIDADES `{items[]}`, LOGROS_ALERTAS `{logros[], alertas[]}`, SEMAFORO `{estado: VERDE\|AMARILLO\|ROJO, texto}` (elegido a mano, sin regla de cálculo), AVANCE_PARTIDA/COSTO_PARTIDA `{wbs}`. Las fotos de un bloque son las de `fotos_campo` con ese `bloqueId`. | Tanda G (exportes) y Documentador: flujo de informes. |
| F-H3 | regla de negocio acordada | Los bloques económicos solo se ofrecen en un informe de formato COSTOS y a quien tiene economía (el servidor ya rechaza el resto con 403). Al aplicar un formato propio a un informe que no los admite se omiten, con aviso. | Documentador: flujo 14. |
| F-H4 | conflicto con un flujo o pregunta para el Responsable humano | Quitar un bloque con fotos asignadas deja esas fotos con un `bloque_id` que ya no existe (siguen ligadas al informe; al emitir quedan en la foto fija bajo un bloque inexistente). La API no tiene un modo de soltarlas en bloque. | Orquestador: ¿W1 libera las fotos al quitar o al emitir? |
| F-H5 | conflicto con un flujo o pregunta para el Responsable humano | El banco de fotos pide un día por vez (`fotos-campo?fecha=`); en un semanal se elige el día con un selector, y solo se ven las asignadas de los días ya visitados. | Orquestador: valorar `?informeId=` en la API. |
| F-H6 | mejora de trabajo | La regla de lint de hooks de React prohíbe mutar refs en el render: el guardado automático se arma desde los manejadores (cola de promesas) y no desde efectos. | `docs/03-aprendizaje-continuo/`. |
| F-H7 | observación sobre la política | Mi lista de «roles con economía» salió mal en la primera prueba (la inventé en vez de leer `puedeVerEconomia`); se corrigió leyendo la fuente. Reafirma «verificar antes de afirmar». | Auditor: sin cambio de política. |

## Traspaso

Hecho: F1 a F6 en `local-worker-3` (`37a5ea8`), con las verificaciones de arriba.
Falta: capturas y recorrido en vivo por rol (migraciones 098 a 102 y cuentas, P33/P36) y la ruta `/descargar` de G (tanda L); responder F-H1, F-H4 y F-H5; filas de la matriz y flujos 14 y 16 (tanda M).
Pendientes: la UI llama a `fotos-campo/[id]` GET por miniatura (una llamada por foto, URL firmada de 60 s).

## Llamadas y contexto

Unas 35 llamadas.

## Skills revisados

`cerrar-tanda` (secuencia: pruebas, commit verificado, resumen) y `verificar-permisos-por-rol` (aplicado con `accionesInforme` probado con los 13 roles; lo vivo lo cierra L).

## Fuentes de verdad revisadas

Ninguna editada. Pendientes para el Documentador: flujo de informes (claves de config, F-H2/F-H3), flujos 14 y 16.

Cierre del Documentador (2026-10-16): «Fuentes de verdad revisadas: ninguna fuente central editada en este cierre; las reglas F-H2 y F-H3 quedan en el libro del plan como R41 y R42, y las decisiones de F-H1, F-H4 y F-H5 en su Registro. Pendientes de decisión o de la tanda M: flujo 22 de informes (R41, R42 y M1), flujos 14 y 16 y la matriz de permisos (acciones de F y ruta `descargar` de G).»

## Corrección F

Sobre `9d8a97c` (incluye G y la corrección de API de W1). Commit en `local-worker-3`: ver `git log` («Correccion F»). Todo «no probado en base».

| Punto | Estado | Qué se hizo |
|---|---|---|
| F-H1 / F1 | Observado | El editor pide `GET informes/[id]` y pinta `datos` por id de bloque en la hoja A4, sin recalcular. Con `errorDatos` muestra un aviso claro y sigue abierto; botón «Actualizar cifras» y recarga al cambiar el período. Se quitó el aviso «sin cifras». Falta verlo con datos reales y capturas (L). |
| F-H5 | Observado | El banco usa `fotos-campo?informeId=` (período completo) con botón «Actualizar»; se quitó el selector de día. |
| F-H2 | Observado | Claves de `config` oficiales. La vista previa lee las mismas que los exportes (no se importó código de `exportar/`); la comparación visual de los tres archivos con la hoja queda para L. |
| F4 | Observado | La ruta `/descargar` ya existe; el botón y el «Descargar» del listado usan la URL del contrato (`formato`, `alcance` válidos); `descargar-rutas.test.ts` pasa. Sin base no se descargó un archivo real. |
| F-H4 | Observado | Tras quitar un bloque se guarda y se refresca el banco (W1 suelta las fotos). |

Comandos: `npm install` (faltaba `docx` en el worktree; sin cambios en `package.json`); `npm test` 149 archivos pasan y 1 omitido, 1560 pruebas; `tsc` sin salida; lint 9 errores y 22 avisos (línea base); build webpack compila.
