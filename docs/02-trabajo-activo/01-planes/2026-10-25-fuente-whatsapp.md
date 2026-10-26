# Plan — Fuente-WhatsApp (el grupo del servicio como fuente de pedidos, notas y archivos)

## Identificación y estado

- Tema: apartado «Fuente-WhatsApp» en `py_control_proyectos_web`, hermano de «Fuente-Gmail» y «Fuente-Drive» (paso 2 de la reestructuración Fuentes / Gestión documentaria).
- Fecha: 2026-10-25.
- Estado: `Implementando` (2026-10-25).
- Gate Spec: aprobado por Victor (2026-10-25) con sus respuestas: se vincula su propio número, el grupo es «Villa Fase 2» (servicio «Facilidades de Villa de Ejecución Fase 2»), «ok dale».
- Gate 1: aprobado por Victor (2026-10-25, «continúa»).
- Gate 2: pendiente de la revisión de Victor (`db/122` aplicada, verificado en pantalla, decisión de Restricciones tomada, envío automático activo; solo falta R2).

## Referencia al Spec aprobado

Reglas dadas por Victor:

1. Del grupo se extraen **imágenes y archivos**, y **texto solo si es relevante**.
2. Los **archivos** van a Gestión documentaria según su área; si no tienen área, a «Sin clasificar». Todo se guarda en **Cloudflare (R2)**.
3. Los **pedidos de campo** van a **Restricciones**. Se identifica a quien lo pidió por su **número de celular** y su nombre si existe; si no existe, se agrega.
4. Las **notas relevantes** (por ejemplo «el día tal hubo una capacitación») van al panel de notas de **Restricciones-Notas**. Si esa información ya está en un correo u otro apartado, la nota **pierde validez**.
5. Restricciones-Notas tiene dos paneles: **restricciones** (solo lectura e informativas: quién las emitió y cuándo) y **notas**.
6. Un solo grupo de WhatsApp por ahora. Se usa el puente que ya existe (`mcp_whatsapp`), vinculado como dispositivo al número de Victor, **solo lectura**.

Decisiones del Orquestador (aceptadas sin objeción): el sistema solo **sugiere** la clasificación (restricción / nota / archivo / ruido) y todo cae en una bandeja **«Por revisar»** que se confirma con un clic; las repeticiones se detectan por la huella del contenido y se registran todas las fuentes donde apareció; una **tabla única de contactos** (celular, nombre, cargo, empresa); el grupo se identifica por su código, y **ningún otro chat del teléfono sale del equipo de Victor**.

## Objetivo, alcance y no alcance

- **Resultado esperado:** los mensajes del grupo llegan a la app ya sugeridos y Victor los confirma en una bandeja; los pedidos de campo se vuelven restricciones con su emisor, y las notas relevantes quedan en el panel de notas.
- **Alcance (tanda A):** tablas (`db/122_fuente_whatsapp.sql`), ruta de ingreso protegida con un secreto propio, reglas de sugerencia, contactos, restricciones con origen WhatsApp y emisor, panel de notas con vigencia, pantalla Fuente-WhatsApp (bandeja y mensajes recientes), panel de notas en Restricciones-Notas, script local que lee el puente y envía solo el grupo elegido, flujo 26, actualización de los flujos 14, 16 y 22.
- **No alcance (por ahora):** guardar los archivos en R2 (R2 no está pagado ni configurado: la ruta de ingreso los acepta y los deja «pendientes de almacén» hasta entonces); clasificar con IA (primero reglas; la IA se agrega después, igual que en Fuente-Gmail); el árbol de Gestión documentaria (paso 4); Fuente-Drive (paso 3).
- **Validación esperada:** pruebas automáticas de las reglas puras; `tsc` y `vitest` sin errores nuevos; verificación local con Playwright en PS-0000 con mensajes de prueba; la prueba con el grupo real queda a la espera de que Victor revincule el puente (el vínculo guardado es del 2 de agosto y el grupo aún no aparece en la base local).

## Diseño propuesto

**Camino del dato:** teléfono → puente en el PC de Victor (`messages.db`) → script local que toma **solo** el grupo configurado y manda lotes a la app (`/api/fuente-whatsapp/ingresar`, con el secreto `WHATSAPP_INGRESO_SECRETO`) → tablas de la app → bandeja «Por revisar».

**Sugerencia por reglas:** pedido de campo si el texto pide, avisa que falta o impide algo (palabras como «falta», «no hay», «necesitamos», «solicito», «urgente», «no llegó»); archivo si trae imagen o documento; nota si informa un hecho con fecha o actividad (capacitación, charla, reunión, visita, llegada); ruido si es saludo, «ok», «gracias» o sticker. Cada mensaje guarda la sugerencia y la confianza; quien confirma puede cambiarla.

**Confirmar:** restricción (se crea con origen WhatsApp, emisor por celular y nombre, y la prioridad elegida), nota (queda vigente en el panel de notas, con la fecha del hecho), archivo (queda con su área o en «Sin clasificar») o descartar. Una nota **pierde validez** cuando se marca que la información ya está en otro apartado.

**Contactos:** al llegar un mensaje se busca el celular en la tabla de contactos; si no existe se crea con el nombre que muestra WhatsApp, y se puede completar cargo y empresa.

**Permisos (provisorio, igual que Fuente-Gmail):** ven administrador, jefe de proyectos, jefe de oficina técnica y supervisor de oficina técnica; confirman y gestionan administrador y jefe de proyectos.

## Entorno, repositorios, ramas y worktrees

Directo en `main` en `py_control_proyectos_web` y en este repositorio. El script local vive en `py_control_proyectos_web/scripts/whatsapp/` y usa solo la librería estándar de Python.

## Fases y dependencias

1. Tanda A1: base de datos, reglas puras y pruebas.
2. Tanda A2: ruta de ingreso, servidor y rutas de la pantalla.
3. Tanda A3: pantalla Fuente-WhatsApp y panel de notas en Restricciones-Notas.
4. Tanda A4: script local, flujo 26 y actualización de flujos 14, 16 y 22.
5. Tanda B (cuando Victor revincule el puente y R2 exista): prueba con el grupo real y copia de archivos.

## Punch List embebida

- [x] A1 Reglas puras de sugerencia, huella y celular, con pruebas (11 pruebas).
- [x] A1 `db/122_fuente_whatsapp.sql` escrito y revisado (**no aplicado**: Victor debe correrlo en Supabase; revisada, no probada en base).
- [x] A2 Ruta de ingreso con secreto, límites y sin duplicar (`/api/fuente-whatsapp/ingresar`, pública solo en el middleware; prueba de idempotencia y de grupo no registrado o pausado).
- [x] A2 Rutas para listar, registrar grupo, completar contactos, confirmar, descartar y notas (`/api/proyectos/{id}/fuente-whatsapp`, `.../mensajes/{mensajeId}`, `.../notas`, `.../notas/{notaId}`); servidor probado con la base en memoria (13 pruebas).
- [x] A3 Pantalla Fuente-WhatsApp (código listo; **sin verificar en pantalla** hasta aplicar `db/122`).
- [x] A3 Restricciones-Notas con dos paneles y origen WhatsApp (código listo; **sin verificar en pantalla** hasta aplicar `db/122`).
- [x] A4 Script local probado con una base de prueba (`scripts/whatsapp/enviar_grupo.py`, 5 pruebas; solo sale el grupo configurado).
- [x] A4 Flujo 26 escrito y flujos 14, 16 y 22, README de flujos, `AGENTS.md`, `docs/README.md` y mapa documental al día.
- [x] Reconocer al emisor en usuarios y personal antes de crear un contacto (pedido de Victor; 2 pruebas más).
- [x] Verificación con Playwright (2026-10-25, servidor local): registro del grupo, bandeja «Por revisar (337)», Restricciones-Notas con dos paneles. Se verificó en el servicio real y no en PS-0000 porque el grupo es único. Confirmar un mensaje como pedido de campo quedó cubierto por pruebas, no probado a mano para no crear datos reales.
- [x] `db/122` aplicada por Victor; app publicada en `main` (854af64). Docs: push con el cierre de esta tanda.
- [x] Tanda B: puente revinculado por QR; grupo «Villa Fase 2» (servicio PS-0003) registrado; 337 mensajes enviados con el script (hallazgo: el historial no trae autor → «Emisor desconocido»).
- [x] Variable `WHATSAPP_INGRESO_SECRETO` cargada en Vercel (Production) y verificada; el envío desde el PC llega a producción (341 enviados: 4 nuevos, 337 repetidos).
- [x] Script programado en el PC (2026-10-25): tarea de Windows «Fuente-WhatsApp envio Villa Fase 2», cada 10 min, solo con la sesión abierta; ejecuta `C:\Users\BRANDY\.whatsapp-ingreso\enviar.ps1` (secreto, estado y registro en esa carpeta privada, fuera de los repos). Verificada: el registro muestra la corrida automática («Mensajes nuevos del grupo: 0»).
- [x] Autor y nombres del historial (2026-10-25, pedido de Victor «no reconoce al personal, número desconocido, @ como otros números»): el script toma el autor de cada mensaje de `whatsmeow_message_secrets` (341 de 341 con autor; antes 8), lo cambia de código interno a celular con `whatsmeow_lid_map`, y el nombre de WhatsApp sale de `whatsmeow_contacts` (la tabla que se consultaba antes no existía: nunca llegaba nombre). Menciones `@código` → celular o nombre; la app las muestra `@Nombre` con el catálogo. La app completa el autor de lo ya guardado al reenviar (`--reenviar`). Tarjetas compactas, línea «Escriben:» y casilla para ocultar lo de poca importancia. Pruebas: 2424 de la app y 9 del script. App `850c760`.
- [ ] Reenviar el grupo desde el inicio con `--reenviar` una vez desplegada la app (completa el autor de los 337 mensajes) y verificar en producción.
- [ ] Copia de archivos a R2 cuando exista (depende de que Victor pague y configure R2).

## Decisiones de Victor durante la implementación

- 2026-10-25 · Restricciones-Notas: el panel de restricciones **conserva** crear, recepcionar y atender, y se pueden agregar notas igual; «vamos a dejarlo así». No cambia el flujo 22.
- 2026-10-25 · Contactos: usar la base de usuarios y de personal que ya existe (celular, nombre, cargo) y no duplicarla; solo los externos van a la tabla de contactos de WhatsApp. Aplicado en el flujo 26 y en el servidor (reconocimiento por los últimos 9 dígitos).

## Riesgos y bloqueos

- El puente usa una conexión **no oficial** (whatsmeow): riesgo bajo pero no nulo para el número de Victor; solo lectura. El teléfono debe abrir WhatsApp al menos cada ~14 días.
- El vínculo del puente es del 2 de agosto: hay que **escanear un QR nuevo** (acción de Victor).
- El PC debe estar encendido para que el puente reciba.
- R2 sin configurar: los archivos esperan.
- La base `db/122` debe aplicarla Victor en Supabase antes de que la pantalla funcione.

## Registro de decisiones

- 2026-10-25 · Victor: un solo grupo, «Villa Fase 2», con su número; reglas de destino de pedidos, notas y archivos.
- 2026-10-25 · Orquestador: reglas antes que IA; confirmar con un clic; el filtro por grupo se hace en el PC de Victor, no en la nube.

## Enlaces a progreso y evidencia homónimos

Por crear al cerrar la tanda A.

## Libro de hallazgos

### Mejoras (de trabajo)
_(vacío)_

### Reglas de negocio acordadas en esta tarea
Ver «Referencia al Spec aprobado»; se integran en el flujo 26 y en los flujos 14, 16 y 22.

### Observaciones sobre la política
_(vacío)_

### Carpetas/archivos huérfanos
_(vacío)_

## Informe de Auditoría

Pendiente.

## Mensaje de cierre

Pendiente.
