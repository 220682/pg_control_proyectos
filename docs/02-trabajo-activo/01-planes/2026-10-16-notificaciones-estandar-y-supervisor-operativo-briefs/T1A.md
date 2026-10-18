# Brief T1A — Cuentas de prueba, respaldo y cierre de avisos viejos, datos de prueba

## Rol, modelo y tanda

Worker de verificación · Sonnet · esfuerzo medio · tanda **T1A** (primera mitad de T1). Se lanza como «Worker verificación · T1A». No escribe código de la app ni hace commits: la evidencia queda en archivos y el Orquestador los commitea.

## Ítems de la tanda

| ID | Qué | Evidencia mínima |
|---|---|---|
| T1-01 | Crear las cuentas de prueba y comprobar que cada una inicia sesión | Lista de cuentas por rol **sin claves** y un ingreso exitoso por cuenta |
| T1-02 | Respaldar los avisos pendientes de la bandeja de Victor (se esperan 18) | `respaldo-avisos-victor.json` (id, mensaje, tipo, destinatario, estado) |
| T1-03 | Cerrar como atendidos esos avisos, sin borrar filas y **sin aprobar ningún RQ** | Conteo antes y después; las filas siguen; ningún RQ cambió de estado |
| T1-06 | Comprobar los datos de prueba de `PS-0000` | `datos-de-prueba.md`: estado del servicio, si tiene Plan Maestro aprobado, RDT y RQ de prueba existentes |

Decisiones ya tomadas por Victor (no se vuelven a preguntar): los correos de las cuentas son alias `+` de `victor.sup22@gmail.com`; las claves las genera el agente; el cierre de los 18 avisos es orden directa (P3).

## Dónde se trabaja

No hay rama ni worktree. Se opera la app **en producción** con el navegador (herramientas `mcp__playwright__*`; cárgalas con ToolSearch en una sola llamada). El dominio estable de producción está en la memoria `observaciones-lote-4-despliegue.md` (ruta abajo). Toda escritura de prueba va solo en `PS-0000`.

## Qué leer, y qué no (en este orden)

1. `C:\Users\BRANDY\.claude\projects\D--VICTOR-CLAUDE-CODE-pg-control-proyectos\memory\cuentas-prueba.md` (cuentas y tabla de roles; ahí se anotan las claves nuevas) y `...\memory\observaciones-lote-4-despliegue.md` (solo el dominio de producción).
2. App, `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`: `src/app/api/admin/usuarios/route.ts` (POST: campos que recibe), `src/app/(workspace)/admin/usuarios/formulario.tsx`, `src/app/api/notificaciones/[id]/atender/route.ts` completo (48 líneas) y `src/lib/requerimientos/aprobacion.ts` (solo la función `codigoDesdeMensajeAprobacion`).
3. Flujo `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\04-flujos-de-negocio\02-usuarios.md` (corto).

No leas el plan completo ni los demás flujos.

## Qué puede trabajar

Crear archivos solo en `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\02-trabajo-activo\03-evidencia\2026-10-16-notificaciones-estandar-y-supervisor-operativo\` y el resumen en `...\01-planes\2026-10-16-notificaciones-estandar-y-supervisor-operativo-briefs\resultados\T1A.md`; y editar la tabla «Cuentas de prueba por rol» de la memoria `cuentas-prueba.md`. No tocar código, flujos, `AGENTS.md` ni otros usuarios, servicios o RQ.

## Cómo hacerlo

**T1-01.** Inicia sesión con la cuenta de administrador de la memoria (usa el valor directo en el formulario; nunca lo pegues en el chat, en un archivo ni en una captura). Crea en Usuarios, con nombre «PRUEBA <rol>» y la contraseña que tú generes (20 caracteres aleatorios, con `node -e "console.log(require('crypto').randomBytes(15).toString('base64url'))"`):

| Correo | Rol |
|---|---|
| `victor.sup22+logistica1@gmail.com` | supervisor_logistica |
| `victor.sup22+logistica2@gmail.com` | supervisor_logistica |
| `victor.sup22+jefeproy@gmail.com` | jefe_de_proyectos |
| `victor.sup22+ofitec@gmail.com` | jefe_de_oficina_tecnica |
| `victor.sup22+supop2@gmail.com` | supervisor_operativo |
| `victor.sup22+admin2@gmail.com` | supervisor_administracion |

Crea **primero solo `+logistica1`**. Si la app o Supabase rechazan el `+`, **detente y devuelve el error al Orquestador** (plan B: otros buzones de Victor; no inventes correos). Si funciona, crea las otras cinco. En el mismo paso en que creas cada cuenta, anota correo y clave en la tabla de `cuentas-prueba.md` (si una cuenta se crea y la clave no queda anotada, elimínala y recréala). Cada cuenta debe quedar miembro de `PS-0000` (asignar OT desde Usuarios; sin eso la app responde «No tienes esta OT a cargo»). Comprueba el ingreso de cada una (cerrar sesión entre una y otra) y anota «ingresó: sí/no». Cada alta envía un correo de invitación a un buzón de Victor: es lo esperado.

**T1-02.** Con la sesión de Victor (`victorperez.nj`), obtén sus avisos con `fetch('/api/notificaciones?direccion=recibidos&visto=false')` dentro de la página (browser_evaluate). Guarda el JSON tal cual (id, mensaje, tipo, estado, destinatario, creado_en) en `respaldo-avisos-victor.json`. Si no son 18, anótalo y continúa con los que haya.

**T1-03.** Antes de tocar nada, guarda el estado de los RQ de los servicios a los que pertenecen esos avisos (consulta los RQ por la pantalla o API existentes). Luego, **por id**, cierra cada aviso con `POST /api/notificaciones/<id>/atender` y el cuerpo `{"respuesta":"Cerrado por limpieza de pruebas (orden de Victor, 2026-10-16)"}`. **EXCEPCIÓN CRÍTICA:** si `codigoDesdeMensajeAprobacion(mensaje)` devuelve un código para ese aviso, `atender` con el rol administrador **aprueba y deriva el RQ**: **no lo llames** para ese aviso. Déjalo sin cerrar, lístalo en `avisos-no-cerrados.md` y escribe `cerrar-avisos-restantes.sql` (un `update notificaciones set estado='ATENDIDO', visto=true, respuesta=..., respondido_en=now() where id in (...)`) para que Victor lo aplique. Después compara el estado de los RQ con el de antes: debe ser idéntico. Cuenta pendientes antes y después.

**T1-06.** En la pantalla del servicio `PS-0000` y en sus listas, anota: estado, si el Plan Maestro está aprobado, qué RDT y RQ existen, y cuáles están marcados «PRUEBA». **No crees datos nuevos ni cambies estados**: si falta algo (por ejemplo, Plan Maestro aprobado), repórtalo como brecha.

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes y escribe el traspaso. Una captura por ítem como máximo, sin claves a la vista. No uses `atender` ni ninguna acción de aprobación fuera del T1-03. Si una pregunta de negocio o un conflicto con un flujo aparece, devuélvela al Orquestador en el momento.

## Resumen de cierre

Usa la plantilla `docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` y guárdalo en `resultados/T1A.md`. Hallazgos en los cinco grupos. Nunca escribas claves en él.

## Criterios de salida

Seis cuentas creadas con ingreso comprobado (o el bloqueo del `+` reportado), respaldo con todos los avisos, avisos cerrados salvo los de aprobación de RQ (listados con su SQL), RQ sin cambios, y `datos-de-prueba.md` escrito.
