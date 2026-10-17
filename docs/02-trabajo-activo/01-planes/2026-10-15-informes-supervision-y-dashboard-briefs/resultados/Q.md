# Resumen de cierre — Tanda Q (pestaña «Inasistencias»), completa

## Tanda, rol y modelo

Worker 3, Sonnet 5.5. Tanda Q completa: Q1–Q3 en 93c5d45 (ver `Q1-Q3.md`), Q4–Q6 en fec676c.

## Estado de los ítems

| ID | Estado | Evidencia | Causa / quién resuelve |
|---|---|---|---|
| Q1 | Conforme | Ver `Q1-Q3.md` (12 pruebas con bordes) | — |
| Q2 | Conforme con datos simulados; no probado en base | Ver `Q1-Q3.md` | Lectura real de la 096 la cierra L |
| Q3 | Conforme con datos simulados | Ver `Q1-Q3.md` (PDF leído con `pdf-parse`) | — |
| Q4 | Conforme en código; capturas Observado | Pestañas «Informes / Inasistencias» (`InformesPestanas.tsx`, patrón nuevo porque E no usó pestañas), `PestanaInasistencias.tsx`: Diario (una fecha) / Semanal (Desde-Hasta), servicio «Todos mis servicios» o uno, tabla con scroll horizontal (`tablaWrapClase`), estados vacío, carga y error con Reintentar, botón PDF. `inasistencias-utils.test.ts` (5 pruebas). `page.tsx` solo envuelve el listado y pasa la lista de servicios del alcance (administrador, todos; resto, `proyectosACargo`) | Capturas escritorio y 390 px no tomadas: sin cuentas de prueba (P36) y migraciones 096/098–102 posiblemente sin aplicar; las cierra la tanda L |
| Q5 | Conforme | `inasistencias-aislamiento.test.ts`: ningún archivo de `src/lib/informes`, rutas de informes, `src/components/informes` ni `src/lib/pdf` (fuera de la pestaña) menciona inasistencias; ningún bloque de ningún formato lo es; el listado conserva sus props y la pestaña vive aparte (el listado queda montado, solo oculto) | — |
| Q6 | Conforme en ruta con suplantación de rol simulada; Observado en vivo | `inasistencias-roles.test.ts`: 13 roles x alcance (tabla abajo) | Prueba en sesión real con las dos cuentas: tanda L |

## Tabla de permisos (esperado / observado en prueba de ruta)

| Rol (los 13 de `ROLES`) | Pestaña visible | Servicio propio | Servicio ajeno (ruta y PDF) | «Todos» |
|---|---|---|---|---|
| administrador | esperado sí / observado sí | 200 / 200 | 200 / 200 (ve todos) | sin filtro de servicio / sin filtro |
| los otros 12 roles | sí / sí | 200 / 200 | 403 / 403 (alcance, no rol) | limitado a sus servicios / limitado |
| sin sesión | — | 401 / 401 | — | — |
| rol ajeno o lista vacía | no / no | 403 / 403 | — | — |

Diferencias con la tabla de permisos: ninguna. El bloqueo de servicio ajeno es por **alcance**, no por rol.

## Rama, commits y archivos tocados

Rama `local-worker-3`, commit fec676c, subido (`git branch -r --contains HEAD` da `origin/local-worker-3`). Árbol limpio. Nuevos: `InformesPestanas.tsx`, `PestanaInasistencias.tsx`, `inasistencias-utils.ts` y su prueba, `inasistencias-aislamiento.test.ts`, `inasistencias-roles.test.ts`. Editados: `informes/page.tsx` (envoltorio y lista de servicios), `inasistencias-route.test.ts` (timeout de 30 s en las pruebas de PDF, que fallaban por tiempo bajo carga).

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| Q-H1 | pregunta para el Responsable humano | (de Q1–Q3) el período no exige «Desde ≥ inicio de ejecución» con «Todos mis servicios» | Confirmar con Victor |
| Q-H4 | mejora de trabajo | Las pruebas de PDF con `pdf-parse` superan 5 s cuando corre toda la suite en paralelo; se fijó timeout de 30 s en ese bloque | Aprendizaje menor |
| Q-H5 | mejora de trabajo | `python -` con heredoc dentro de un Bash que también escribe archivos falló por comillas; Write + script en archivo separado funciona | Aprendizaje menor |
| Q-H6 | conflicto con un flujo (a revisar) | La pestaña es un patrón nuevo en Informes (E no usaba pestañas). Flujo 14 y matriz de permisos: añadir la pestaña «Inasistencias» (los 13 roles, dentro de sus servicios) | Documentador/Orquestador; yo no edité fuentes |

## Traspaso

Hecho: Q1–Q6 con código, pruebas y push. Falta: capturas de escritorio y 390 px y prueba en vivo con las dos cuentas (L); actualizar flujo 14/16 y la matriz. Verificación: `npm test` 1481 de 1481 en verde (dos corridas; una primera tuvo 2 fallas por tiempo, ya corregidas); `npx tsc --noEmit` sin errores; `npm run lint` 9 errores y 22 avisos (iguales a la base, ninguno nuevo); `npx next build --webpack` correcto. `.snap` de curva-s restaurado.

## Llamadas y contexto

Unas 17 llamadas en esta mitad.

## Skills revisados

`verificar-permisos-por-rol` (leído y aplicado: esperado/observado por rol, alcance distinto de rol, solo lectura), `cerrar-tanda` (secuencia seguida; el commit de documentación es del Orquestador).

## Fuentes de verdad revisadas

Ninguna editada. Pendientes: flujo 14, flujo 16 y artefacto «Matriz de permisos» (pestaña Inasistencias dentro de Informes).
