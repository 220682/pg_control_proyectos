# Resumen de cierre — T1A

## Tanda, rol y modelo

T1A (primera mitad de T1) · Worker de verificación · Sonnet · esfuerzo medio. Operación en producción (`py-control-proyectos-web.vercel.app`) con Playwright y la sesión de Victor.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| T1-01 | **Observado** (2 de 6 cuentas) | El `+` en el correo funciona. Creadas e ingresadas con éxito: `+logistica1` y `+logistica2` (supervisor_logistica), ambas miembros de `PS-0000`; ambas ingresaron (`/api/notificaciones` 200, `/api/admin/usuarios` 403, `GET .../requerimientos` de PS-0000 200). | Las otras cuatro (`+jefeproy`, `+ofitec`, `+supop2`, `+admin2`) no se crearon: Supabase respondió `email rate limit exceeded` (cada alta envía un correo de invitación y se agotó el tope por hora; falló también un reintento posterior). Lo resuelve el Orquestador/Victor: esperar a que se libere el tope y repetir, o configurar un SMTP propio en Supabase. Las filas siguen en la tabla de `cuentas-prueba.md` marcadas «SIN CREAR», con la clave ya reservada. |
| T1-02 | **Conforme** (con matiz) | `respaldo-avisos-victor.json` (17 avisos PENDIENTE, los que devuelve `?visto=false`) y `respaldo-avisos-victor-todos.json` (los 18 recibidos; el 18.º, de PS-0002, está en estado REVISADO). | Eran 17 pendientes + 1 revisado = 18. Ninguno es de aprobación de RQ. |
| T1-03 | **No ejecutado** | Antes: 18 avisos recibidos, 17 PENDIENTE. Estado de RQ guardado en `estado-rq-antes.json`: **0 RQ** en PS-0000 a PS-0004, por lo que no hay RQ que proteger. | El clasificador de permisos del entorno **denegó** la llamada en lote a `POST /api/notificaciones/<id>/atender` (escritura externa en producción). No se intentó rodearlo. Queda pendiente: que Victor o el Orquestador autorice esa acción, o aplique `cerrar-avisos-restantes.sql` (cubre los 18 ids). |
| T1-06 | **Conforme** | `datos-de-prueba.md`. PS-0000: EJECUCION, Plan Maestro v3 APROBADO, 33 RDT (31 validados, 2 registrados; 2 marcados «PRUEBA» por especialidad), 0 RQ. | Brecha: no existe ningún RQ de prueba. |

## Rama, commits y archivos tocados

Sin rama ni commits (no corresponde). Archivos creados en `docs/02-trabajo-activo/03-evidencia/2026-10-16-notificaciones-estandar-y-supervisor-operativo/`: `respaldo-avisos-victor.json`, `respaldo-avisos-victor-todos.json`, `estado-rq-antes.json`, `datos-de-prueba.md`, `cerrar-avisos-restantes.sql`; y este resumen. Editada la tabla de `cuentas-prueba.md` (memoria, fuera del repo). Los archivos de `.playwright-mcp/` de la raíz son residuos del navegador, sin tocar.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| T1A-H1 | conflicto con un flujo o pregunta para el Responsable humano | El alta de usuario envía una invitación por correo vía Supabase y su tope por hora bloquea crear cuentas en lote (se agotó tras 2 altas). | Decidir: espaciar altas por horas, o SMTP propio en Supabase. |
| T1A-H2 | mejora de trabajo | Crear usuarios con `fetch` a `/api/admin/usuarios` (POST) y asignar OT con `PATCH /api/admin/usuarios/<id>` (`asignarProyectos`) desde la sesión del admin funciona y evita pasar claves por el chat; el reintento solo sirve cuando pase el tope. | `docs/03-aprendizaje-continuo/` |
| T1A-H3 | observación sobre la política | El clasificador de permisos deja pasar altas de usuarios en producción pero bloquea el cierre en lote de avisos aunque el brief lo ordena; conviene que el brief indique la regla de permiso necesaria o que el Orquestador lo ejecute. | Gate 2 |
| T1A-H4 | mejora de trabajo | El filtro `?visto=false` de `/api/notificaciones` devuelve solo los PENDIENTE (17), no los 18 recibidos; el conteo «18» incluía uno REVISADO. | `docs/03-aprendizaje-continuo/` |
| T1A-H5 | archivo o carpeta huérfano | La página de login guardaba una contraseña antigua autocompletada para `victorperez.nj@gmail.com` (no es la vigente). Sin acción. | Informativo |

## Traspaso

- Hecho: respaldo de avisos, estado de RQ (vacío), datos de PS-0000, 2 cuentas de prueba (logística) con ingreso comprobado.
- Falta: crear `+jefeproy`, `+ofitec`, `+supop2`, `+admin2` (rate limit) y asignarlas a PS-0000 (`PATCH` con `asignarProyectos: ['0a20df2f-c5e9-4296-9c08-f89af499182d']`); cerrar los 18 avisos (autorización o SQL); luego comparar RQ (debe seguir vacío).
- Nota: el sistema contiene también otros 3 usuarios no míos; no se tocaron. La sesión del navegador quedó cerrada.
- Comprobación SQL: los nombres de columna del SQL (`visto`, `respuesta`, `respondido_en`) vienen del brief y no se verificaron contra la base.

## Llamadas y contexto

Aproximadamente 45 llamadas.

## Skills revisados

Ninguno aplica (verificación puntual con navegador; no se usó `verificar-permisos-por-rol`).

## Fuentes de verdad revisadas

Ninguna actualizada. Pendiente para el Orquestador: tabla de cuentas por rol (memoria) con 4 filas sin crear.
