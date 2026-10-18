# Verificación en producción (solo lectura)

Fecha: 2026-10-18. Sitio: https://py-control-proyectos-web.vercel.app (código del commit b056f62 de la app). Cuenta: administrador (Victor). Ancho de ventana: 1440 px. Capturas en `docs/02-trabajo-activo/03-evidencia/2026-10-16-notificaciones-estandar-y-supervisor-operativo/produccion/`.

| Punto | Resultado | Captura |
|---|---|---|
| 1. `/notificaciones` carga sin error; filtro «Tipo de aviso»; grupo «Jefatura»; insignia N° OT / «Entorno»; opción «Solo Entorno» en el filtro de OT | Conforme. El filtro «Tipo de aviso» existe (lista: Requerimientos, RDT, Servicio, Checklist, Mensajes, Otros; se ve como «Todos los tipos de aviso»). «Jefatura» está en el filtro de grupos. Los avisos muestran la insignia PS-xxxx (28) y «Entorno» (1). El filtro de OT trae «Solo Entorno (sin servicio)». | `prod-01-notificaciones.png` |
| 2. El aviso «PRUEBA T7 mensaje de Entorno» se abre sin error | Conforme. Se despliega con el texto del mensaje, el enlace «Ir a mi entorno», el cuadro de respuesta y «Marcar atendido». Al abrirlo pasó de Pendiente a Revisado (comportamiento de la propia pantalla: «Al abrir pasa a Revisado»; no se hizo clic en Marcar atendido ni se respondió). | `prod-02-aviso-entorno.png` |
| 3. `/mi-entorno` (perfil) muestra celular, correo y contraseña | Observado (parcial). Con el botón «Mi perfil» se ve la ficha de solo lectura con NOMBRE, CORREO, CARGO, ÁREA, CELULAR y ROLES: celular y correo conformes. El bloque de contraseña (y los controles de editar celular y cambiar correo) no se vio: está tras el botón «Editar mi perfil», cuyo clic fue denegado por el clasificador de permisos del entorno por considerarlo una edición. Queda por mirar por Victor o con autorización explícita. | `prod-03-mi-entorno.png` |
| 4. Consola sin errores de la app | Conforme. 0 errores en la sesión de producción. Los avisos (warnings) que aparecen en el registro son de una sesión previa en localhost (preload de CSS), no de producción. No hubo 4xx de recursos ajenos anotables. | n/a |

## Notas

- El 1.er snapshot del navegador (`page-2026-10-18T23-00-55-426Z.yml`, pantalla de ingreso) guardó la clave en texto; se redactó en el archivo (reemplazada por `[CLAVE-REDACTADA]`). Los otros 5 archivos nuevos de `.playwright-mcp/` (1 log de consola y 4 snapshots) no contienen ninguna de las claves de `cuentas-prueba.md`. `.playwright-mcp/` no figura como ignorado por git: no se debe comitear.
- Solo lectura: no se hizo clic en Aprobar, Devolver, Guardar, Eliminar ni en ningún botón de escritura; el único cambio de datos es el paso automático Pendiente a Revisado del aviso de Entorno al abrirlo.
- Navegador cerrado al terminar. Sin commits.
