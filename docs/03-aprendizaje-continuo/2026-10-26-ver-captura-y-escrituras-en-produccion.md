# 2026-10-26 — Cambios visuales: ver una captura propia antes de entregar; escrituras en producción: las lanza Victor

## Origen

Plan [`2026-10-25-gestion-documentaria.md`](../02-trabajo-activo/01-planes/2026-10-25-gestion-documentaria.md), pantalla «Gestión de Email» (rondas 1 a 4) y agrupación de documentos por tema.

## Método que funcionó

- **Calcar la maqueta y mirar el resultado antes de decir «listo».** Victor rechazó tres versiones de la pantalla porque se entregaron sin verlas. Cuando la app real no se puede abrir (el MCP de Playwright y la extensión de Chrome no conectaron), se monta un banco temporal local: una página `src/app/zz-maqueta` con los datos de la maqueta y `fetch` simulado, una ruta pública temporal en `src/middleware.ts`, el servidor de desarrollo en `localhost:3100` y Chrome headless por CDP (`chrome.exe --headless=new --remote-debugging-port`, captura con `Page.captureScreenshot`) a 1366 px de ancho, que es la pantalla de Victor. Al terminar se borra el banco y se restaura el middleware con `git checkout --`.
- **Agrupar con una lista fija en vez de a mano.** Una regla que debe valer para todos los servicios y para los correos que lleguen después se escribe una sola vez como código puro (`src/lib/gestion-emails/familias.ts`, sin dependencias de la app) que usan tanto el sincronizador como el script de reagrupo. El script simula primero, guarda un respaldo y solo escribe con `--aplicar`; correrlo dos veces no cambia nada la segunda vez, y esa segunda simulación sirve de verificación.
- **Antes de fijar la lista, leer todos los servicios (solo lectura).** Del análisis de los otros tres servicios salieron seis familias que no estaban en el servicio piloto; la regla «un tema que aparece una sola vez queda como documento propio» evitó inventar familias de un solo caso.

## Trampas encontradas

- **El clasificador de permisos bloquea las escrituras del agente a la base de producción**, aunque el script sea correcto y tenga respaldo. No se elude: el agente prepara, simula y respalda, y Victor lo lanza con `!` en el chat.
- **Dar el comando completo, con rutas reales.** Con un marcador como `<ruta del respaldo>` el intérprete lo toma como redirección (`<`) y falla. Siempre la ruta literal entre comillas.
- **Una segunda ejecución con la misma ruta de respaldo lo pisa** (el script lo escribe antes de actuar). Para verificar después de aplicar, usar otra ruta.
- **Una palabra demasiado amplia en una pista arrastra casos ajenos.** «viabilidad» se llevaba una coordinación técnica y contractual de PS-0001 a «Plan de trabajo y memoria descriptiva»; lo detectó la simulación, no la prueba unitaria. La simulación sobre datos reales es parte de la verificación.
- **Un enlace de Gmail con el correo en la ruta (`/mail/u/{correo}/`) da 404** si esa cuenta no es la número de la sesión; `mail/?authuser={correo}#search/rfc822msgid:{Message-ID}` no depende del orden de las cuentas.
