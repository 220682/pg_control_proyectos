# Resumen de cierre — T7C (perfil propio: contraseña, celular y correo) — tras el intento de confirmación de Victor

## Tanda, rol y modelo

T7C · Worker de verificación con navegador (Playwright) · Sonnet · esfuerzo medio. Ítems T7-08 y T7-09. Fecha de la prueba: 2026-10-18. Estado: reanudada tras el aviso de Victor de que abrió el enlace; el cambio de correo **no quedó confirmado** (ver T7-09).

Capturas: `docs/02-trabajo-activo/03-evidencia/2026-10-16-notificaciones-estandar-y-supervisor-operativo/t7/` (14 PNG con prefijo `t7c-`, a 1440 px). Ninguna muestra una clave: en el formulario de contraseña los campos van enmascarados y no se activó el ojo.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| T7-08 (contraseña, cuenta Logística 2) | **Conforme** | Actual incorrecta rechazada con «La contraseña actual no es correcta» (`t7c-08-p1`, el servidor responde 400). Nueva corta rechazada con «La contraseña nueva debe tener al menos 8 caracteres.» (`p2`). Confirmación distinta rechazada con «La confirmación no coincide con la contraseña nueva.» (`p3`). Cambio correcto: «Contraseña actualizada. Desde ahora entre con la nueva.» (`p4`). Tras cerrar sesión, la clave anterior ya no entra: «Correo o contraseña incorrectos» (`p5`). La clave nueva entra y lleva a Programas (`p6`). La clave nueva se generó al azar (20 caracteres) y se anotó solo en la memoria local de cuentas, en la fila de Logística 2, antes de enviarse (el archivo temporal del scratchpad y el de `.playwright-mcp/` se borraron). | — |
| T7-09 (celular) | **Conforme** | Logística 1 (rol que antes no editaba el perfil) ve «Editar mi perfil». Celular «abc» rechazado: «Celular no válido. Use de 6 a 20 caracteres…» (`t7c-09-p1`). Celular de prueba guardado: «Celular actualizado.» (`p2`) y se ve en «Mi perfil» tras recargar (`p3`). Perfil antes: celular «—» (`p0`). | — |
| T7-09 (correo, primera mitad) | **Conforme hasta el estado pendiente** | Con clave incorrecta, el cambio de correo se rechaza con «La contraseña actual no es correcta» (`p4`). Con la clave correcta se pidió `victor.sup22+logistica1b@gmail.com`: «Le enviamos un correo de confirmación a … Hasta que lo confirme, sigue valiendo su correo actual.» (`p5`). Tras recargar, «Mi perfil» muestra el correo actual `victor.sup22+logistica1@gmail.com` y «Pendiente de confirmar: victor.sup22+logistica1b@gmail.com. Mientras tanto vale el correo actual.» (`p6`). | — |
| T7-09 (ingreso con el correo nuevo, el anterior ya no entra, redirección `/mi-entorno?code=`) | **Observado** | Servidor de la rama en el puerto 3000 (levantado por el Orquestador). Con el correo nuevo `victor.sup22+logistica1b@gmail.com` y la clave de Logística 1: «Correo o contraseña incorrectos» (`t7c-09-p8`, repetido una segunda vez con el mismo resultado). Con el correo anterior `victor.sup22+logistica1@gmail.com`: **entra** (llega a Programas; `t7c-09-p7` muestra el formulario de ingreso sin error porque aún estaba cargando; el ingreso se confirmó en la repetición). El perfil sigue diciendo «Pendiente de confirmar: victor.sup22+logistica1b@gmail.com. Mientras tanto vale el correo actual.» (`t7c-09-p9`). Consola: 0 errores de la app. La redirección `/mi-entorno?code=` no se pudo comprobar porque no se completó la confirmación. | El cambio de correo sigue pendiente aunque Victor dice haber abierto el enlace. Causas posibles, sin poder distinguirlas desde el navegador: (a) Supabase exige también confirmar desde el correo actual `+logistica1` (secure email change) y falta ese segundo enlace; (b) el enlace redirigió a una dirección donde no se completó el intercambio del código (no hay dato de qué vio Victor en el navegador); (c) el enlace caducó o ya se usó. Dato de Victor: sin dato sobre si llegó un segundo correo y sin dato de lo que vio en el navegador. Decide el Orquestador con Victor. |

## Qué debe hacer Victor

1. Abrir el buzón de `victor.sup22@gmail.com` y buscar el correo de confirmación de cambio de correo dirigido a `victor.sup22+logistica1b@gmail.com`.
2. Abrir el enlace de ese correo.
3. Si Supabase tiene activado «secure email change», puede llegar además un segundo correo de confirmación dirigido al correo actual `victor.sup22+logistica1@gmail.com`; en ese caso también hay que abrir ese enlace. Hasta ahora no se pudo comprobar si es el caso (el mensaje de la app y el perfil solo hablan de un correo de confirmación al correo nuevo).
4. Avisar al Orquestador para reanudar.

Aviso sobre la redirección: la ruta `/api/perfil/correo` pone `emailRedirectTo` como `urlSitioPublica()/mi-entorno`. El `.env.local` del worktree no define `NEXT_PUBLIC_SITE_URL` (ni variables VERCEL; solo se comprobó que no existen, sin leer valores), así que desde el servidor local la dirección de retorno es `http://localhost:3000/mi-entorno`, no el puerto 3107. Al abrir el enlace, el navegador de Victor puede intentar `http://localhost:3000/mi-entorno?code=…` y fallar si no hay nada escuchando en el 3000 (o si Supabase no tiene esa URL en su lista de permitidas, caerá a la URL del sitio configurada). Esto no es un fallo del código: es de cómo se hace la prueba. Opciones al reanudar: levantar el servidor en el 3000 antes de que Victor abra el enlace, o aceptar que el enlace redirija a donde Supabase decida y comprobar `/mi-entorno?code=` entonces con el servidor levantado en la ruta que corresponda.

## Qué pasó al reanudar

Victor avisó que abrió el enlace de confirmación del correo `+logistica1b`; no dijo si llegó un segundo correo ni qué vio en el navegador (sin dato). El correo anterior sigue entrando, el nuevo no entra y el perfil sigue en «pendiente de confirmar». Para cerrar T7-09 hace falta que Victor revise su buzón por un segundo correo de confirmación dirigido a `+logistica1` (abrirlo), o que repita el cambio de correo desde el perfil y abra el enlace con el servidor de la rama escuchando en la URL a la que apunta el enlace. La fila de Logística 1 en `cuentas-prueba.md` **no** se cambió (el correo vigente sigue siendo `+logistica1`).

## Rama, commits y archivos tocados

Rama `local-worker-7` (verificada con `git branch --show-current`), último commit `9611338` (T7fix). Sin commits ni cambios al código ni al `.env.local`. Solo se crearon las capturas `t7c-*` y este resumen, y se actualizó la fila de Logística 2 en la memoria local de cuentas. Servidor del 3107 cerrado en la pausa (netstat sin escucha). Al reanudar se usó el servidor del puerto 3000, levantado y que cierra el Orquestador; no se levantó ni cerró otro.

## Datos de prueba y cambios en cuentas que quedan

- Logística 2: clave cambiada (la nueva está solo en la memoria local de cuentas, fila de esa cuenta, con la nota «T7C-08»). La clave anterior ya no sirve.
- Logística 1: celular de prueba `999000111` guardado; cambio de correo pendiente hacia `victor.sup22+logistica1b@gmail.com`. Mientras no se confirme, sigue entrando con `+logistica1`. Cuando se confirme, hay que actualizar su fila en la memoria local de cuentas (correo nuevo `+logistica1b`).
- Un cambio de correo ya pedido puede dejar a la cuenta con el correo pendiente aunque no se confirme; si Victor decide no confirmar, queda como «pendiente» en el perfil.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| T7C-H1 | observación menor (prueba / configuración) | `emailRedirectTo` usa la URL pública configurada; en local cae a `http://localhost:3000`. Probar la redirección `/mi-entorno?code=` desde el servidor de prueba requiere el puerto 3000 o definir `NEXT_PUBLIC_SITE_URL` en el entorno de prueba. | Orquestador decide cómo probarlo al reanudar |
| T7C-H2 | observación menor (consola) | La consola registra un `[ERROR] 400` por cada rechazo esperado de la API (clave incorrecta); es el comportamiento esperado de la respuesta HTTP, no un fallo de la app. | Sin acción |

## Traspaso

Hecho: T7-08 completo (Conforme); T7-09 celular (Conforme) y correo hasta el estado pendiente de confirmar.
Falta: tras la confirmación de Victor, (a) entrar con `victor.sup22+logistica1b@gmail.com` y la misma clave de Logística 1, (b) comprobar que `victor.sup22+logistica1@gmail.com` ya no entra, (c) comprobar la redirección `/mi-entorno?code=` sin error visible, (d) capturas `t7c-09-p7` en adelante, (e) actualizar la fila de Logística 1 en la memoria local de cuentas, (f) consola y cierre del servidor.
Para reanudar hay que volver a levantar `npm run dev -- --webpack -p 3107` en el worktree.
Verificación: `git branch --show-current` → `local-worker-7`; `git log --oneline -1` → `9611338`; netstat sin escucha en 3107.

## Llamadas y contexto

Unas 40 llamadas en esta parte (una vez reanudada tras el corte por límite de uso).

## Skills revisados

Ninguno aplica (verificación con Playwright siguiendo el brief).

## Fuentes de verdad revisadas

`src/app/api/perfil/contrasena/route.ts`, `src/app/api/perfil/correo/route.ts`, `src/components/ui/PerfilEntorno.tsx`, `src/lib/config/url-sitio.ts` del worktree. No se editó ninguna fuente.

## Snapshots y archivos de `.playwright-mcp/` nuevos

Snapshots nuevos: `page-2026-10-18T21-02-52-974Z.yml`, `page-2026-10-18T21-03-34-910Z.yml`, `page-2026-10-18T21-04-06-958Z.yml` y, al reanudar, `page-2026-10-18T21-47-04-407Z.yml` (todos de pantallas de ingreso o perfil con campos vacíos). Logs: `console-2026-10-18T21-02-45-992Z.log` y `console-2026-10-18T21-47-02-191Z.log`. Se buscaron en ellos todas las claves de la memoria local de cuentas: ninguna aparece. Ingresos y cambios de clave se hicieron con `fill`, sin snapshot con la clave escrita.
