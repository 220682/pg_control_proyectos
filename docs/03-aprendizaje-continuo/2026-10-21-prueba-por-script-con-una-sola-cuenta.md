# 2026-10-21 — Las pruebas funcionales se hacen con un solo script y una sola cuenta, no con agentes

## Origen

Plan [`2026-10-21-correcciones-prueba-rdt-ps0001.md`](../02-trabajo-activo/01-planes/2026-10-21-correcciones-prueba-rdt-ps0001.md), apartado «Mejoras (de trabajo)», fila M2. Método de trabajo, no regla del sistema.

## Observación

La prueba del RDT en PS-0001 se hizo primero con agentes y varias cuentas: lenta, cara y pidiendo claves otra vez. Victor pidió scripts Python + Playwright, sin agentes, que revisen todo de una vez.

## Método que funcionó

- Un script por propósito (`ejecutar.py` carga, `comparar.py` contrasta con los esperados, `revisar_todo.py` revisa permisos, avisos, negativos y flujos de rechazo), en `scripts/prueba_rdt_ps0001/`. Un solo `revisar_todo.py` cubrió 54 comprobaciones con 0 diferencias.
- Una sola cuenta de administrador: los 13 roles se ven con «Ver como» y llamadas sin efecto (fecha futura, acción inválida), que distinguen 403 de 400.
- Credenciales solo en variables de entorno (`PG_CORREO`, `PG_CLAVE`) que el usuario guarda en su equipo; nunca en el repositorio ni en el chat. Si la sesión del agente no las ve, el usuario corre el script en su PowerShell y pega solo las líneas con diferencia.
- Lo que el script lee en pantalla (PR, Dashboard) se compara por texto; lo que es «al corte» (PV, SV, SPI) solo se compara el día de su fecha.

## Trampas encontradas

- «Ver como» deja la última simulación activa: volver al rol propio entre pasos y en un `finally`.
- La pantalla Notificaciones usa al usuario real, no el simulado: los avisos se verifican con la API (`direccion=enviados`), y esta agrupa por destinatario y RDT (campo `ids`).
- Una expectativa mal escrita parece un fallo de la app: ante una diferencia, confirmar primero la expectativa.
