# Cambio de proveedor a Cloud Run y otros aprendizajes del plan RDT del 2026-11-06

Fecha: 2026-11-08. Origen: plan [RDT: validación opcional, edición, cargos y Tecnet sin paquetes](../02-trabajo-activo/01-planes/2026-11-06-rdt-validacion-edicion-cargos-y-tecnet-sin-paquetes.md).

- **Mensajes dictados por voz:** si no se entienden del todo, mirar primero la captura que manda Victor (qué pantalla y qué equipo) antes de construir. La primera lectura («la galería del celular») no era lo pedido (sus chats de WhatsApp en la PC). Lo que no se entiende, se dice y no se ejecuta.
- **Lo que arranca con Windows** (accesos de Inicio, scripts al iniciar) no lo cambia el agente: se entrega un instalador en la app y Victor lo corre.
- **Antes de aprobar un Plan Maestro desde la app,** guardar el PV por partida y fecha y el Consolidado, y compararlos después: demuestra que la versión nueva no cambió nada que no debía. Aprobar la versión no recalcula el Dashboard al instante; verificar el Dashboard (no solo la Curva S) o forzar el recálculo.
- **Cambiar de proveedor de la app:** Vercel no entrega sus variables secretas (salen como «[SENSITIVE]»). Las claves se sacan nuevas en cada servicio (Cloudflare, Google) y se guardan solo en el equipo de Victor (`%USERPROFILE%\.control-proyectos\claves-nube.env`), nunca en los repositorios. Las capturas de Playwright que muestran una clave se borran en cuanto se lee el valor.
- **Publicar desde la carpeta de la app:** excluir `.worktrees/`, `.superpowers/` y `.almacen-local/`. Con ellas la subida pesaba 192 MB y 33 mil archivos y se trababa sin dar error.
- **Lo que escribe claves** (secretos de GitHub, archivos de claves) puede quedar bloqueado para el agente: se le da a Victor el comando exacto con `!` y el agente vigila el resultado.
- **Contraseñas:** el agente no las escribe en la app publicada ni en paneles externos; Victor inicia sesión en la ventana de Playwright y el agente sigue desde ahí.
- **Prueba de punta a punta sin dejar rastro:** crear el RDT desde un borrador (camino normal del formulario), validarlo, mirarlo en Dashboard e informe y luego borrar informe, RDT, borrador y sus avisos; comprobar que los números vuelven.
