# Plan — Estado del servicio (minutas y correos del cliente)

## Identificación y estado

- Tema: apartado «Estado del servicio» en `py_control_proyectos_web`.
- Fecha: 2026-10-24.
- Estado: `Desplegado, leyendo dos buzones; clasificación manual del histórico a medias; pendientes R2, disparador horario y Gate 2` (código en producción con `2568fe1`, migración y claves listas).
- Gate Spec: aprobado por Victor (2026-10-24) — pidió «mejóralo, propón mejoras, ejecuta» y eligió «Spec + construir todo lo que no necesita mis claves».
- Gate 1: pendiente (el flujo se salta el Punch List formal por orden directa de Victor; la verificación queda en la evidencia).
- Gate 2: pendiente.

## Referencia al Spec aprobado

Pedido de Victor (2026-10-24), en sus palabras: un apartado **Estado del servicio** donde se guardan las **minutas** de la reunión semanal con el cliente y donde se **conectan dos correos electrónicos** (reciben casi la misma información). El sistema lee los correos dos veces al día (7 a. m. y 2 p. m., con botón para cambiar las horas), analiza uno solo cuando el mismo correo llega a los dos, y lo manda al servicio que corresponde; si el servicio no existe, va al portafolio (Servicios Marcobre). Dentro de cada servicio se arman **temas** (por ejemplo PETS): cada correo agrega una **nota** al tema (enviado a revisión, aprobado, observado…), y si falta un tema, el sistema lo crea. Se debe poder abrir el correo completo y sus adjuntos desde la app y filtrar por fecha para no ver todo el histórico.

## Objetivo, alcance y no alcance

- **Resultado esperado:** una pantalla por servicio (y una por portafolio) que muestra, por tema, la línea de tiempo de notas sacadas de los correos del cliente, más las minutas de la reunión semanal.
- **Alcance de este plan:**
  1. Base de datos: buzones, configuración de horarios, correos, adjuntos, temas, notas, minutas y registro de sincronizaciones (`db/119_estado_servicio.sql`).
  2. Servidor: lectura de Gmail (solo lectura, OAuth), anti-duplicado, clasificación (reglas + IA), sincronización por horario, descarga de adjuntos.
  3. Pantallas: Estado del servicio (por servicio), Estado del portafolio (correos sin servicio y temas generales), Configuración de correos y horarios.
  4. Permisos, chip en el panel, flujo 23 nuevo y actualización del flujo 14.
- **No alcance:** responder correos desde la app; leer otros proveedores distintos de Gmail; WhatsApp; convertir las minutas en acuerdos con seguimiento (queda como mejora futura).
- **Validación esperada:** pruebas automáticas de las piezas puras (huella, horarios, reglas, lectura del correo, cifrado); `tsc` y `lint` sin errores nuevos; la conexión real a Gmail y a la IA **no se prueba** hasta que Victor entregue las claves.

## Mejoras propuestas (todas incluidas salvo que se diga lo contrario)

1. **Anti-duplicado en dos pasos:** primero el `Message-ID` del correo (idéntico en ambos buzones), luego una huella del contenido. El segundo ejemplar se guarda como duplicado, no se analiza ni crea nota, y la nota recuerda que llegó a los dos buzones.
2. **Los hilos heredan el tema:** si una respuesta pertenece al mismo hilo de un correo ya clasificado, va al mismo tema sin gastar IA.
3. **Clasificación en dos etapas:** reglas primero (código `PS-####` en el asunto o cuerpo, nombre del servicio, palabra del tema); la IA solo cuando las reglas no alcanzan. Si la confianza es baja, el correo va a **Por revisar** en lugar de adivinar.
4. **Cada nota trae un «movimiento»:** Enviado, Aprobado, Observado, Solicitud, Información. El encabezado del tema muestra el último movimiento como estado (ejemplo: PETS — Observado).
5. **«Sin respuesta»:** un tema cuyo último movimiento fue «Enviado» o «Solicitud» y lleva 3 días o más sin novedad se marca para prepararlo antes de la reunión semanal.
6. **Ver el correo completo y sus adjuntos** desde la propia app (los adjuntos se guardan en Storage al sincronizar, hasta 10 MB cada uno).
7. **Filtros:** rango de fechas, tema, movimiento y texto. Por defecto se muestran los últimos 30 días.
8. **Registro de sincronizaciones** visible (cuándo corrió, cuántos correos nuevos, duplicados, por revisar, errores) y botón «Sincronizar ahora».
9. **Reasignar a mano:** un correo mal clasificado se mueve a otro tema, servicio o portafolio; la corrección queda marcada como manual y la IA no la vuelve a tocar.
10. **Horarios editables:** el botón de horarios guarda las horas en base de datos; un disparador externo llama al endpoint cada hora y el servidor decide si toca correr (no hay que cambiar el despliegue para cambiar la hora).

## Decisiones técnicas y por qué

| Decisión | Motivo |
|---|---|
| Gmail API con OAuth de solo lectura, sin librería nueva (`fetch`) | No se guarda ninguna contraseña; el token de refresco se guarda cifrado (AES-256-GCM, clave en variable de entorno). No suma dependencias. |
| IA con la API de Claude (`claude-haiku-5-5`) solo si hay clave | Lo mecánico va en el modelo pequeño. Sin clave el sistema funciona solo con reglas y deja lo dudoso en Por revisar. |
| Disparador externo cada hora + horas en base | `vercel.json` es fijo; un cron por hora permite que el botón de horarios mande. Requiere un plan de Vercel que admita cron horario, o un disparador gratuito externo con la cabecera `Authorization: Bearer <CRON_SECRET>`. **No se agrega `vercel.json` hasta que Victor confirme su plan.** |
| Un portafolio por defecto (Servicios Marcobre) para lo que no tiene servicio | Ya es el portafolio por defecto de la app (`NOMBRE_PORTAFOLIO_DEFECTO`). |
| Permisos: ver = administrador, jefe de proyectos, jefe de oficina técnica y supervisor de oficina técnica; gestionar (temas, reasignar, minutas, horarios, buzones) = administrador y jefe de proyectos | Propuesta mía, **por confirmar con Victor**: los correos del cliente pueden traer precios y contratos. |

## Lo que necesito de Victor (bloquea solo la parte real con Gmail/IA)

1. Crear un cliente OAuth en Google Cloud (tipo «aplicación web», permiso `gmail.readonly`, redirección `<sitio>/api/estado-servicio/google/callback`) y pasar `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET`.
2. Definir `ESTADO_SERVICIO_CLAVE` (32 bytes en base64) y `CRON_SECRET` en Vercel.
3. Opcional: `ANTHROPIC_API_KEY` para la clasificación con IA.
4. Decir qué plan de Vercel tiene (para el disparador horario) o aceptar un disparador externo.
5. Aplicar `db/119_estado_servicio.sql` en el SQL Editor de Supabase.
6. Compartir la Matriz de permisos como editor para actualizarla.

## Entorno, repositorios, ramas y worktrees

Trabajo directo en `main`, sin worktree (orden de Victor en la sesión). Código en `py_control_proyectos_web`; documentación aquí. No se hace push hasta que `db/119` esté aplicada (si no, la pantalla falla en producción).

## Fases y dependencias

| Fase | Contenido | Depende de |
|---|---|---|
| F1 | `db/119` y tipos | — |
| F2 | Piezas puras con pruebas: huella, horarios, reglas, lectura de correo, cifrado | F1 |
| F3 | Gmail, IA y sincronización | F2 |
| F4 | Rutas API | F3 |
| F5 | Pantallas, permisos, chip | F4 |
| F6 | Flujo 23, flujo 14, índice, evidencia | F5 |

## Archivos / componentes afectados

Nuevos: `db/119_estado_servicio.sql`, `src/lib/estado-servicio/*`, `src/app/api/estado-servicio/**`, `src/app/(workspace)/proyectos/[id]/estado-servicio/page.tsx`, `src/app/(workspace)/programas/[id]/portafolios/[portafolioId]/estado-servicio/page.tsx`, `src/app/(workspace)/admin/estado-servicio/page.tsx`, `src/components/estado-servicio/*`. Modificados: `permisos.ts`, `registro-accesos.ts`, `matriz-base-flujo14.ts`, `cobertura-pantallas.ts` y sus pruebas, página del portafolio (enlace), `db/README.md`. Documentación: flujo 23 (nuevo), flujos 14 y 16, índice de flujos.

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-24 | Proveedor de los dos correos: Gmail / Google Workspace | Victor |
| 2026-10-24 | Avanzar con Spec + construir lo que no necesita claves | Victor |
| 2026-10-24 | Permisos propuestos (ver tabla), por confirmar | Orquestador |
| 2026-10-24 | No se agrega `vercel.json` con cron hasta saber el plan de Vercel de Victor | Orquestador |
| 2026-10-24 | No se hace commit ni push mientras `db/119` no esté aplicada (la pantalla fallaría en producción) | Orquestador |
| 2026-10-24 | «Apruebo todo, luego vemos qué modificamos»: se autoriza commit, push y cargar claves y migración | Victor |
| 2026-10-24 | Google Cloud (proyecto My Project Engineer): Gmail API habilitada, permiso `gmail.readonly`, cliente OAuth «Estado del servicio» creado; la app queda en modo «Prueba» (Google no deja publicar con `vercel.app`) | Orquestador |
| 2026-10-24 | Vercel (Producción): `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `ESTADO_SERVICIO_CLAVE` y `CRON_SECRET` cargadas como secretas | Orquestador |
| 2026-10-24 | `db/119` verificada en Supabase (8 tablas con RLS, 1 fila de configuración); app `220d3d5` en producción, pantalla `/admin/estado-servicio` abre con 3 de 4 requisitos en verde (falta la IA, opcional) | Orquestador |
| 2026-10-24 | Acceso visible «Correos del cliente» en el panel izquierdo (app `66a7fc1`): el único enlace estaba en el encabezado de login/inicio y no se llegaba desde el panel de trabajo; Victor dijo «dale» | Victor |
| 2026-10-25 | Primera lectura real con Gmail (`oficinatecnica@promcoser.com.pe`): 200 correos leídos, todos en «Por revisar» (sin IA ni temas); la lectura ahora corta por tiempo y el botón repite pasadas (app `4022ee7`). Ver evidencia | Orquestador |
| 2026-10-25 | Arrancar con trabajo manual (lo hace el agente) y ver luego cómo automatizar: API de Claude o agente en la nube | Victor |
| 2026-10-25 | Segundo buzón `proyectos@promcoser.com.pe` conectado; ambos se leen desde el 7 de septiembre. Original de un correo repetido = el de oficina técnica | Victor / Orquestador |
| 2026-10-25 | Los adjuntos dejan de copiarse a Supabase (`e3e3925`, ~200 MB ya guardados bajo `estado-servicio/`, sin borrar); los archivos irán a Cloudflare R2 | Victor |
| 2026-10-25 | Cuenta de Cloudflare creada por Victor (id de cuenta en el panel `dash.cloudflare.com`); falta activar R2 con su método de pago, crear bucket y token, y el código de subida | Victor |
| 2026-10-25 | Clasificación del histórico: se ubican solo los 4 servicios vigentes; lo ajeno no se ubica ni se migra; los administrativos sin servicio nombrado quedan archivados en «Por revisar». Los dos correos de Tecnovias con contraseña no se tocan | Victor |
| 2026-10-25 | Ronda de aprendizaje con 4 subagentes Sonnet (240 correos) y ronda masiva con 9 subagentes Haiku (801); salidas sin aplicar ni validar con script (el verificador de seguridad de comandos cayó). Ver evidencia | Orquestador |

Pendiente: entender por qué en el Edge de Victor `/admin/estado-servicio` lo redirige al portafolio (con la misma cuenta abre bien en el navegador de pruebas; descartados los roles y «Ver como»), conectar el Gmail desde `/admin/estado-servicio` (el consentimiento de Google lo completa Victor), definir el disparador horario (Vercel Hobby solo permite crons diarios; propuesta: workflow de GitHub Actions), decidir qué hacer con la caducidad de 7 días del permiso en modo «Prueba», y probar «Sincronizar ahora». Hasta entonces la lectura real de Gmail y la IA siguen **sin probar**.

## Libro de hallazgos

### Mejoras (de trabajo)

| ID | Fecha | Quién | Qué | Destino propuesto | Estado | Enlace |
|---|---|---|---|---|---|---|
| M1 | 2026-10-25 | Orquestador | Clasificar un buzón grande: ronda de aprendizaje con Sonnet y el resto con Haiku, sobre una exportación fuera del repo; validar ids por script y no por conteo | `03-aprendizaje-continuo/` | Trasladada | [`2026-10-25-clasificar-correos-en-tandas.md`](../../03-aprendizaje-continuo/2026-10-25-clasificar-correos-en-tandas.md) (cierre de sesión, 2026-10-25) |

### Reglas de negocio acordadas en esta tarea

Las reglas del pedido van directo al flujo 23 (nuevo). No contradicen ningún flujo escrito.

Acordadas por Victor el 2026-10-25 para la **carga manual del histórico** (7 sep al 25 oct), no para la lectura automática; por eso no se editó el flujo 23:

* Se ubican y se migran solo los correos de los **4 servicios vigentes**; el resto (otros trabajos de Promcoser, publicidad, avisos automáticos) no se ubica ni se migra.
* Los correos **administrativos** de campamento y personal que no nombran el servicio quedan **archivados en «Por revisar»**, sin revisarlos.
* El original de un correo que llega a los dos buzones es el de **oficina técnica** (`oficinatecnica@`); el de `proyectos@` queda como copia.
* Los archivos adjuntos van a **Cloudflare R2**, no a Supabase.
* Los dos correos de Tecnovias con usuario y contraseña en el texto **no se tocan**.

### Observaciones sobre la política

| ID | Fecha | Quién | Observación | Estado |
|---|---|---|---|---|
| O1 | 2026-10-25 | Orquestador | El [flujo 23](../../04-flujos-de-negocio/23-estado-del-servicio.md) dice que los adjuntos se guardan en Storage (bucket `documentos-proyecto`), que se descargan desde la pantalla y que «sin servicio identificable → portafolio». Lo desplegado desde `e3e3925` ya no copia adjuntos (queda solo nombre, tipo y tamaño) y la carga manual deja sin ubicar lo ajeno. Cuando se implemente R2, el flujo debe reescribirse con Victor; no se editó por cuenta propia | Pendiente de Victor (Gate 2) |

### Carpetas/archivos huérfanos

Ninguna.

## Mensaje de cierre

Pendiente de Gate 2. Al cierre de sesión del 2026-10-25: los dos buzones están leídos desde el 7 de septiembre (1 341 correos, 300 copias, 1 041 por ubicar); las 9 salidas de la ronda masiva existen en el scratchpad y **no están validadas ni aplicadas a la base**. Siguiente sesión: (1) correr `validar.mjs` (ids, orden, destinos), (2) unir las dos rondas, normalizar los temas y simular, (3) aplicar solo los 4 servicios con confianza alta o media, (4) activar R2 con Victor (método de pago) y subir los adjuntos de esos correos, (5) decidir el disparador horario, la caducidad de 7 días de Google y la IA. Estado al 2026-10-24: F1 a F6 construidas y verificadas (evidencia en [`verificacion.md`](../03-evidencia/2026-10-24-estado-del-servicio/verificacion.md)); flujo 23 nuevo, flujos 14 y 16 e índices actualizados. Falta, de parte de Victor: claves de Google, `ESTADO_SERVICIO_CLAVE`, `CRON_SECRET`, plan de Vercel, aplicar `db/119_estado_servicio.sql`, confirmar los roles de la nota ¹⁹ del flujo 14 y actualizar la Matriz de permisos.
