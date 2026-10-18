# Resumen de cierre — T1B

## Tanda, rol y modelo

T1B (segunda mitad de T1) · Worker de verificación · Sonnet · esfuerzo medio. Navegador único (Playwright). Sin código ni commits.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve, si no es Conforme |
|---|---|---|---|
| T1-03 (comprobación) | Conforme | Con la sesión de Victor: `GET /api/notificaciones?direccion=recibidos` devuelve 18, todos ATENDIDO (antes, según el respaldo: 17 PENDIENTE + 1 REVISADO). Los RQ de `PS-0000` a `PS-0004` estaban en 0 antes de mi prueba (misma lectura que `estado-rq-antes.json`) y solo existe el mío en `PS-0000`. Nota: Victor conserva 6 avisos **enviados** PENDIENTE (informes emitidos y «hola»), que no son de los 18 recibidos | |
| T1-04 | Conforme | `informe-ciclo-rq-hoy.md`: 5 pasos con quién actúa, quién recibe, quién no, texto exacto y qué se cierra. Parte de las bandejas (Jefe de Proyectos y Jefe de Oficina Técnica) se dedujo de la lista de enviados porque no hay cuenta; y la bandeja de `jeyger22` en los pasos 3b y 4 se dedujo de lo que Logística 1 veía como enviado | Cuentas faltantes: Victor / Orquestador |
| T1-05 | Conforme con partes no probadas | `informe-bandeja-supervisor-hoy.md` y 7 capturas (`t1b-*.png` en la carpeta de evidencia): Logística 1 y 2 antes, tras abrir y tras atender; supervisor operativo final | No probado: RDT validado/rechazado y servicio asignado (alterarían datos ajenos; por código no existe aviso de RDT); segundo supervisor operativo (sin cuenta) |

## Rama, commits y archivos tocados

Sin commits ni cambios en la app. Archivos nuevos (los commitea el Orquestador), en `docs/02-trabajo-activo/03-evidencia/2026-10-16-notificaciones-estandar-y-supervisor-operativo/`: `informe-ciclo-rq-hoy.md`, `informe-bandeja-supervisor-hoy.md` y 7 PNG `t1b-*.png`; más este archivo.

Datos de prueba creados en producción (solo `PS-0000`): RQ `PS-0000-LL-SO-001` (estado final ATENDIDO) y un comentario «PRUEBA T1B…» de Logística 2. Dejaron avisos PENDIENTES: 1 al administrador (visible en su campana, 1), 1 al Jefe de Proyectos (sin cuenta) y el «atendido» al supervisor operativo. No cerré ninguno (el brief no autoriza `atender` aparte del recorrido).

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| T1B-H1 | observación sobre la política | Avisos de rol compartidos (H8 confirmado): una sola fila para todo el rol; la primera persona que abre apaga la campana de las demás y nadie ve quién lo abrió. El aviso de Logística se cierra al recepcionar; «En almacén» y «Atendido» no avisan a Logística ni a administración | Spec de Notificaciones (decisión de Victor: ¿aviso por persona o por rol?) |
| T1B-H2 | observación sobre la política | El cierre de avisos del RQ es por texto `Requerimiento <código>%`. El aviso «Nuevo requerimiento …» (derivación directa) no empieza así y no se cerraría. No probado | Spec / Planner |
| T1B-H3 | observación sobre la política | El administrador recibe duplicado el aviso de un RQ (tiene los roles administrador y jefe de oficina técnica): dos tarjetas idénticas, y una quedó REVISADO y la otra PENDIENTE | Spec |
| T1B-H4 | regla de negocio acordada | **Ninguna nueva.** Observado: el solicitante nunca recibe aviso de comentarios sobre su RQ; el aviso «Atendido» al solicitante queda pendiente sin cierre automático; no hay aviso de RDT validado o rechazado ni de asignación de servicio. Son preguntas para Victor, no reglas acordadas | Pregunta para Victor en el Gate |
| T1B-H5 | mejora de trabajo | El formulario de login del navegador de Playwright se rellena solo con la última cuenta usada, y el snapshot muestra su clave en texto. Un snapshot con la clave de Logística 1 quedó en `.playwright-mcp/page-2026-10-18T01-29-44-134Z.yml` (carpeta no ignorada por git, aparece como sin seguimiento). Hay además tres snapshots más antiguos con claves: `page-2026-10-18T01-19-53-009Z.yml`, `page-2026-10-17T13-46-26-861Z.yml`, `page-2026-10-15T15-44-53-756Z.yml` | Archivo huérfano / seguridad: el Orquestador debe **no commitear** `.playwright-mcp/` y Victor decide si borrarlos (yo no borro) |
| T1B-H6 | mejora de trabajo | Cambiar de cuenta cuesta menos en una sola llamada `browser_run_code_unsafe` (limpiar cookies, login, lectura de la bandeja y captura) que con clics sueltos; la campana equivale a `GET /api/notificaciones/count` (solo PENDIENTE recibidos) | `docs/03-aprendizaje-continuo/` |

## Traspaso

- Hecho: T1-03, T1-04 y T1-05 como arriba; sesión del navegador dejada sin cuenta iniciada.
- Falta: cerrar o decidir sobre los avisos de prueba (administrador 1 pendiente por mi comentario); crear las cuentas que faltan si se quiere cubrir jefes y segundo supervisor operativo; decidir qué hacer con `.playwright-mcp/` (contiene claves en texto).
- Verificación: `GET /api/notificaciones?direccion=recibidos` de Victor = 18 ATENDIDO; RQ `PS-0000-LL-SO-001` = ATENDIDO.

## Llamadas y contexto

Unas 50 llamadas (meta 80).

## Skills revisados

Ninguno aplica: el brief indica leer solo los archivos listados. `verificar-permisos-por-rol` no se usó porque no se comprobaron permisos por rol.

## Fuentes de verdad revisadas

Flujo `05-rq.md` (solo lectura; no menciona avisos del ciclo, no se actualizó). Sin conflicto con lo escrito, porque el flujo 05 no describe los avisos. Pendiente para el Orquestador: reflejar en el flujo 05 o en el de notificaciones lo que decida Victor sobre H1 a H4.
