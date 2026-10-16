# Resultado — Tanda D: Informes, API

## Tanda, rol y modelo

Worker 1, Sonnet 5.5, esfuerzo medio. Tanda D, Ola 2, carril W1 (despues de C). Unas 45 llamadas.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| D1 | Observado | `informes-rutas.test.ts`: GET (emitidos de todos + borradores propios, sin foto fija, COSTOS filtrado), POST (código con `siguiente_codigo_informe(p_proyecto, p_tipo, p_ot)` y `p_ot` = `proyectos.numero`; copia RESTRICCIONES y PROXIMAS_ACTIVIDADES del último emitido; COSTOS sin economía 403; período 400). | No probado en base (098-102 sin aplicar). Lo cierra la tanda L. |
| D2 | Observado | Mismas pruebas: GET/PATCH/DELETE, borrador ajeno 404, PATCH y DELETE de emitido 409, período por llamada directa 400, COSTOS sin economía 403. | No probado en base. Tanda L. |
| D3 | Observado | `emitir`: arma datos, `congelar`, RPC `emitir_informe` (probada con RPC simulada) y 1 notificación MENSAJE a cada miembro menos el autor. `nueva-version`: borrador v+1, mismo código, `reemplaza_a`. | No probado en base: `componer-datos.ts` (lectura de PR, RDT, Curva S) y la RPC real solo se ven con 098-102 aplicadas. Tanda L. |
| D4 | Observado | GET solo los propios (con bloques de Costos solo con economía); POST con bloques de Costos exige economía. | No probado en base. Tanda L. |
| D5 | Observado | `fotos-campo-rutas.test.ts`: JPEG por bytes, tope 3 MB, descripción obligatoria, GPS válido, `wbs` del servicio, ruta `informes/{proyectoId}/fotos/{uuid}.jpg` en `documentos-proyecto`, banco `?fecha=` (día Lima), URL firmada de 60 s, asignar a bloque de borrador propio, borrar solo foto propia sin informe emitido. | Storage y base simulados. Tanda L. |
| D6 | Observado | Campo `avisos` en POST y PATCH: cruce con semanal emitido (se permite) y días sin parte RDT. | Los días sin diario salen de partes RDT (`diasSinParte`), no de diarios emitidos: confirmar. Sin base. |
| D7 | Observado | 71 pruebas de ruta + 20 unitarias; tabla de 13 roles abajo. | Tabla armada con pruebas de ruta por rol (sesión simulada); sin suplantación en vivo (098-102 sin aplicar). «Observado» lo cierra la tanda L. |

Comandos: `npm test` 135 archivos y 1391 pruebas en verde; `npx tsc --noEmit` sin errores; `npm run lint` 9 errores y 22 avisos (iguales a los preexistentes, ninguno nuevo); `npx next build --webpack` compilado en verde.

## Tabla esperado contra observado (13 roles, pruebas de ruta)

Esperado = lo que dicen `permisos.ts` y el brief; observado = código de estado devuelto por la ruta (`it.each` sobre los 13 roles). Todas las celdas coinciden. SI = permitido (200/201), 403 = bloqueado por rol. Todos con alcance sobre el servicio; sin alcance, 403 en todas (probado aparte).

| Rol | Ver lista, informe, fotos | Crear y emitir TECNICO | Crear y emitir COSTOS | Mis formatos con Costos | Foto de campo (subir, asignar, borrar) | Nueva versión de informe ajeno |
|---|---|---|---|---|---|---|
| administrador | SI | SI | SI | SI | SI | SI |
| jefe_de_proyectos | SI | SI | SI | SI | SI | SI |
| jefe_de_oficina_tecnica | SI | SI | SI | SI | SI | 403 |
| supervisor_operativo | SI | SI | 403 | 403 | SI | 403 |
| supervisor_costos | SI | 403 | SI | SI | 403 | 403 |
| jefe_de_costos | SI | 403 | SI | SI | 403 | 403 |
| supervisor_oficina_tecnica, planner, supervisor_logistica, supervisor_administracion, supervisor_ssoma, asistente, rrhh | SI | 403 | 403 | 403 | 403 | 403 |

Los informes COSTOS no aparecen en la lista ni se leen sin economía (403). Borrador ajeno: 404 para todos los roles.

## Rama, commits y archivos tocados

Rama `local-worker-1`: 8be999c (D1-D4) y 0369ab8 (D5-D7), subidos; `git branch -a --contains` muestra `local-worker-1` y `origin/local-worker-1`; árbol limpio.
Rutas nuevas: `src/app/api/proyectos/[id]/informes/{route,[informeId]/route,[informeId]/emitir/route,[informeId]/nueva-version/route,formatos-usuario/route}.ts`, `src/app/api/proyectos/[id]/fotos-campo/{route,[fotoId]/route}.ts`. Lib: `src/lib/informes/{reglas-informe,componer-datos,ruta,notificar-emision,fotos-campo,fake-admin-test}.ts`; `estados.ts` ampliado (`puedeCrearAlgunInforme`; nueva versión propia de COSTOS con `puedeCrearInformeCostos`). Pruebas: `informes-rutas.test.ts`, `fotos-campo-rutas.test.ts`, `reglas-informe.test.ts`. Sin cambios en `tipos.ts`, `permisos.ts`, `db/**`, `rdts/**`.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| D-H1 | conflicto con un flujo o pregunta para el Responsable humano | `puedeCrearInforme` son 4 roles (supervisor operativo, administrador, jefe de proyectos, jefe de oficina técnica), pero COSTOS lo crean los 5 con economía; `supervisor_costos` y `jefe_de_costos` no están en los 4. Se implementó: TECNICO/EJECUTIVO/FOTOGRAFICO/PERSONALIZADO exigen los 4; COSTOS exige los 5. Esos dos roles crean, editan, emiten y versionan solo COSTOS. | Victor confirma; si procede, flujo 14 y matriz de permisos. |
| D-H2 | conflicto con un flujo o pregunta para el Responsable humano | El brief no define el semáforo, las incidencias ni logros y alertas. Sin regla de negocio, esos bloques (más RESTRICCIONES, PROXIMAS_ACTIVIDADES y FOTOS_DESTACADAS) congelan lo que el usuario escribió en su `config`; no se calcula ningún semáforo. | Victor decide si el semáforo es automático (umbrales de SPI) y de dónde salen incidencias. |
| D-H3 | conflicto con un flujo o pregunta para el Responsable humano | Un informe DIARIO se exige de un solo día (Desde = Hasta); `periodo.ts` no lo exigía. Un bloque AVANCE_PARTIDA sin `config.wbs` impide emitir (400). Un formato de usuario con bloques de Costos solo se usa como informe COSTOS; en PERSONALIZADO se rechaza (403). | Victor confirma las tres reglas; luego flujo 18/21. |
| D-H4 | conflicto con un flujo o pregunta para el Responsable humano | «Banco del día» devuelve las fotos de todo el servicio de ese día (Lima, 05:00Z a 05:00Z), no solo las propias; cualquier foto del servicio se puede asignar a un borrador propio mientras no esté en un emitido. | Confirmar si el banco es de todo el servicio. |
| D-H5 | mejora de trabajo | Heredocs de bash con comillas y acentos fallaron dos veces ("unexpected EOF"); la herramienta Write evita el problema. Un cliente de servicio falso en memoria (`fake-admin-test.ts`) permitió probar las 13 combinaciones de rol sin base. | `docs/03-aprendizaje-continuo/`. |
| D-H6 | observación sobre la política | El brief pide "la tabla de los 13 roles" del Skill con suplantación en vivo, pero con migraciones sin aplicar solo hay pruebas de ruta; conviene decir en el estándar que esa tabla queda "Observado" hasta L. | Auditor. |

Regla de negocio acordada: ninguna (las decisiones D-H1 a D-H4 esperan a Victor).

## Traspaso

- Hecho: D1 a D7 en código y pruebas, subido. Lo que dependa de la base queda «no probado en base».
- Falta: aplicar 098-102 (Victor) y probar en vivo `componer-datos.ts`, la RPC `emitir_informe`, el contador de códigos, storage y las notificaciones con sesión (tanda L). La interfaz (Ola 3) consume estas rutas; las respuestas son `{ informe }`, `{ informes }`, `{ avisos }`, `{ foto, url }`.
- Pendiente: responder D-H1 a D-H4.
- Verificación: ver los comandos de arriba.

## Llamadas y contexto

Unas 45 llamadas a herramientas, sin cortes.

## Skills revisados

`cerrar-tanda` y `verificar-permisos-por-rol` (aplicados; tabla arriba). Demás: ninguno aplica.

## Fuentes de verdad revisadas

No se editó ningún flujo. Pendiente de decisión: flujo 14 y la Matriz de permisos (D-H1: roles que crean COSTOS), flujos 18 y 21 (D-H2, D-H3, D-H4). La Matriz de permisos y el flujo 14 deben reflejar las rutas nuevas (`informes`, `fotos-campo`) en la tarea de documentación.
