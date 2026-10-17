# Resumen de cierre — Tanda E

## Tanda, rol y modelo

Tanda E (Informes, chips, listado, nuevo y foto de campo), Ola 3, carril W3. Worker 3, Sonnet. Aprobación de P7 por Victor el 2026-10-16 (Registro de decisiones, fila «Relevo 4»): `geolocation=(self)` aplicado en `next.config.ts`; `camera=()` sin tocar.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| E1 | Conforme | `npm test` 140 archivos / 1445 pruebas en verde; `registro-informes.test.ts` recorre los 13 roles (informes: 13 con acceso; foto de campo: solo administrador, jefe de proyectos, jefe de oficina técnica y supervisor operativo) en matriz derivada, panel izquierdo, panel derecho y accesos rápidos. `next.config.ts`: `geolocation=(self)`. | Lo observado en vivo por rol lo cierra la tanda L. |
| E2 | Observado | Listado con las 9 columnas, filtros (tipo, estado, autor, desde, hasta), estados vacío, carga y error con reintento, tabla con scroll horizontal; `listado-utils.test.ts` prueba filtros, querystring y que los COSTOS no salen sin economía. | Sin captura ni datos reales: migraciones 098 a 102 posiblemente sin aplicar (P33) y sin cuentas de prueba (P36). Lo cierra L. |
| E3 | Observado | `NuevoInforme.tsx`: selector de formato (Costos deshabilitado con título), tipo, fecha o período con los 4 atajos + personalizado, resumen (días, trabajados, diarios emitidos, sin diario, columnas por día o semana, título «Informe del período») y avisos de cruce con `resumirPeriodo`; `contarDiasDelPeriodo` probada. | Sin captura ni prueba contra base. Lo cierra L. |
| E4 | Observado | `FotoCampo.tsx`: botón «Tomar foto» con `<input type="file" accept="image/*" capture="environment">`, reducción a 1600 px (JPEG, calidad descendente hasta 3 MB), partida opcional, descripción, GPS opcional con mensaje, reintento sin señal (sin cola); `foto-utils.test.ts`. | La cámara con `capture` y el GPS necesitan un celular real (P8): lo confirma Victor / tanda L. |

Comandos finales: `npm test` verde (140 / 1445); `npx tsc --noEmit` sin salida; `npm run lint` 9 errores y 22 avisos (igual que la línea base, ninguno nuevo); `npx next build --webpack` compila y lista `/proyectos/[id]/informes`, `/informes/nuevo`, `/informes/foto`.

## Rama, commits y archivos tocados

Rama `local-worker-3`, push hecho. Commits: `9851fbe` (E1–E2) y `b455b98` (E3–E4, último). `git branch --contains HEAD` devuelve solo `local-worker-3`. Árbol limpio (el `.snap` de curva-s se restauró con `git checkout`).

Archivos: `next.config.ts`; `src/lib/config/registro-accesos.ts`, `panel-izquierdo.ts`, `cobertura-pantallas.ts` y las pruebas `equivalencia-f1b`, `nav-proyecto`, `panel-derecho`, `panel-izquierdo`, `registro-accesos` (conteos y rápidos), nueva `registro-informes.test.ts`; `src/app/(workspace)/proyectos/[id]/informes/{page,nuevo/page,foto/page}.tsx`; `src/components/informes/{ListadoInformes,NuevoInforme,FotoCampo}.tsx`, `listado-utils.ts`, `foto-utils.ts` y sus pruebas.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| E-H1 | conflicto con un flujo o pregunta para el Responsable humano | El brief habla del «panel izquierdo grupo Reportes» y de «Acciones del izquierdo»: ambos existen en `ESTRUCTURA_IZQUIERDA`; se añadieron `informe-servicio` a Reportes y `foto-campo` a Acciones. El flujo 16 y el 14 deben reflejarlo. | Documentador (tanda M): flujos 16 y 14. |
| E-H2 | regla de negocio acordada | Se conservó el id `informe-servicio` (etiqueta «Informes de supervisión», informativo, `requiereServicio: 'si'`, permiso `puedeVerInformes`, 13 roles). Nuevo acceso `foto-campo` (acción, grupo Supervisión operativa, `requiereServicio: 'si'`, permiso `puedeTomarFotoCampo`: administrador, jefe de proyectos, jefe de oficina técnica, supervisor operativo), acceso rápido nº 8 (los rápidos pasan de 7 a 8). Registro: 54 a 55 accesos, nav de servicio 41 a 42, panel derecho 32 a 33, panel izquierdo 28 a 30 chips. | Documentador (M): filas de la matriz de permisos (artefacto) y flujo 14; el Auditor verifica trazabilidad. |
| E-H3 | conflicto con un flujo o pregunta para el Responsable humano | «Trabajados» y «sin diario emitido» del resumen de Nuevo se definieron así (según la maqueta): trabajados = días con parte RDT no rechazado; diarios emitidos = informes DIARIO EMITIDO (sin COSTOS) con fecha en el período; sin diario = días trabajados sin diario emitido. El brief no lo define. Nota: el aviso del servidor usa otra cosa («días sin ningún parte RDT»). | Victor confirma la definición; Documentador la integra al flujo si procede. |
| E-H4 | conflicto con un flujo o pregunta para el Responsable humano | El brief no incluye el editor/detalle: los enlaces «Continuar/Ver» del listado apuntan a `/proyectos/[id]/informes/[informeId]` (tanda F), que aún no existe: dará 404 hasta F. Tras crear, Nuevo no redirige al editor: muestra el código, los avisos y un enlace al listado. | Tanda F: crear la ruta; luego Nuevo puede redirigir al editor. |
| E-H5 | conflicto con un flujo o pregunta para el Responsable humano | No incluidos por no estar en el brief: «Mis formatos» (formatoUsuarioId) en Nuevo y el botón «Descargar» del listado (no hay API de descarga todavía). Fotos del listado: se cuentan por consulta directa a `fotos_campo` (informe_id) en la página, porque la API de listado no devuelve el conteo. Autores: nombres por consulta a `perfiles` en la página. | Orquestador: decidir si «Mis formatos» entra en F; si W1 debe sumar `fotos` a la API de listado. |
| E-H6 | mejora de trabajo | Un heredoc de Bash largo con comillas simples falló sin escribir nada; con archivos grandes conviene la herramienta Write. | `docs/03-aprendizaje-continuo/` (entorno Windows). |
| E-H7 | observación sobre la política | El brief pide commit al cerrar E1–E2 y al cerrar E3–E4; se hicieron dos commits, el segundo con las pantallas Nuevo y Foto, y el registro ya apuntaba a `/informes/foto` desde el primero (ruta sin página en ese commit intermedio, sin prueba que lo detecte). | Auditor: valorar si hace falta una prueba de que cada ruta del registro tenga página. |

## Traspaso

Hecho: E1 a E4 en `local-worker-3` (commits `9851fbe`, `b455b98`), pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde.
Falta: ruta de detalle/editor `/informes/[informeId]` (tanda F); capturas, inicio de sesión y prueba en celular real (cámara `capture` y GPS, P7/P8) y con migraciones 098 a 102 aplicadas (tanda L); filas de la matriz y flujos 14 y 16 (tanda M).
Verificación: `npm test` (140 archivos, 1445 pruebas), `npx tsc --noEmit`, `npm run lint` (9 errores, 22 avisos, línea base), `npx next build --webpack`.
Pendientes: E-H3 y E-H5 requieren decisión.

## Llamadas y contexto

Unas 38 llamadas.

## Skills revisados

`cerrar-tanda` (secuencia seguida: pruebas, commit verificado, resumen) y `verificar-permisos-por-rol` (aplicado mediante `registro-informes.test.ts`, 13 roles; lo observado en vivo lo cierra L). Sin otros aplicables.

## Fuentes de verdad revisadas

Ninguna editada. Pendientes para el Documentador (M): flujo 14 (acceso `informe-servicio` renombrado y `foto-campo` nuevo, con sus roles), flujo 16 (Reportes, Acciones, accesos rápidos de 7 a 8), el artefacto «Matriz de permisos» y `design.md` si cambia algo visual.

Filas para la matriz derivada: `informe-servicio` — informativo, servicio obligatorio — administrador, jefe de proyectos, jefe de oficina técnica, supervisor de oficina técnica, planner, supervisor de costos, jefe de costos, supervisor operativo, supervisor de logística, supervisor de administración, supervisor SSOMA, asistente, RRHH: sí (13). `foto-campo` — acción, servicio obligatorio — sí: administrador, jefe de proyectos, jefe de oficina técnica, supervisor operativo; no: los otros 9.
