# 07 — Núcleo / auth
> Lee si: la tarea toca el login por correo/contraseña, la sesión con cookie, `NEXT_PUBLIC_SITE_URL`, o el cambio de la propia contraseña o del propio correo.


Login correo/contraseña, sesión cookie, `NEXT_PUBLIC_SITE_URL` en Vercel. Spec `2026-08-15-nucleo`.

## Cambio de la propia contraseña y del propio correo (Victor, 2026-10-17)

Los 13 roles cambian su contraseña y su correo desde el Perfil de Mi entorno ([flujo 03](03-entorno.md); permiso en la nota 14 del [flujo 14](14-accesos-y-restricciones.md)). No hay «olvidé mi contraseña» ni obligación de cambiarla en el primer ingreso: quien pierde la clave se la pide al administrador.

* **Cambiar la contraseña** (`PATCH /api/perfil/contrasena`): exige sesión, la **contraseña actual**, la nueva (**mínimo 8 caracteres**, distinta de la actual) y su confirmación. La actual se verifica en el servidor con un cliente aparte, sin tocar las cookies, así que la sesión del navegador no cambia. Se cambia siempre la del **id de la sesión** (nunca uno enviado en el cuerpo) y no se escribe ninguna contraseña en respuestas ni registros. Después se entra con la nueva y no con la anterior. Errores: sin sesión 401, rol desconocido 403, actual incorrecta, nueva corta, igual a la actual o confirmación distinta 400.
* **Cambiar el correo** (`PATCH /api/perfil/correo`): el correo es el identificador de ingreso y vive en el sistema de autenticación, no en la tabla de perfiles. Exige la contraseña actual y un correo nuevo válido, distinto del actual y no usado por otro usuario (409). El sistema envía un enlace de confirmación; **el correo cambia solo cuando se confirma** desde el buzón nuevo (el enlace lleva a Mi entorno) y hasta entonces sigue valiendo el anterior; el perfil muestra «pendiente de confirmar».
* **Por verificar en vivo:** el cambio de contraseña, la llegada y el efecto del enlace de confirmación del correo (si el proyecto de autenticación pide confirmar también el correo anterior) y que el celular se guarde con un rol que antes no podía; las pruebas del servidor usan dobles de Supabase. Si la verificación muestra otra cosa, manda lo observado y se corrige aquí.
