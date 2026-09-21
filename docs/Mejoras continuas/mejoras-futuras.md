# Mejoras futuras

Archivo permanente — siempre el último de `Mejoras continuas/` (sin fecha en el nombre a propósito, para quedar al final en cualquier listado). No es un lote: no lleva checklist ni se cierra nunca. Es un lugar de espera para mejoras que Victor decide posponer indefinidamente, sin fecha de retomar.

## Cómo se usa

- Solo se agrega algo aquí cuando **Victor lo indica explícitamente** como pendiente a futuro — no es donde el agente guarda por su cuenta algo que no alcanzó a hacer.
- Cada ítem anota: de qué archivo/sesión salió, en qué consiste, y por qué se pospuso (si se sabe).
- Cuando Victor decide retomarlo, se saca de aquí y se convierte en un archivo nuevo de `Mejoras continuas/` con la fecha del día en que se retoma.

## Pendientes a futuro

### Paquetes de trabajo como filtro operativo (Plan Maestro / flujo 20)

- **Origen:** `docs/Mejoras continuas/2026-09-20-control-avance-plan-maestro.md` (Pendiente Fase 2 del flujo 20-plan-maestro).
- **Qué es:** paquetes de trabajo, área, disciplina y frente como filtros operativos del Plan Maestro, sin reemplazar las partidas DP.
- **Pospuesto:** 2026-09-20.

### 3WLA como plan operativo separado

- **Origen:** `docs/Mejoras continuas/2026-09-20-control-avance-plan-maestro.md` (Pendiente Fase 2 del flujo 20-plan-maestro).
- **Qué es:** construir el 3WLA/Plan semanal como interfaz propia (compromisos, restricciones, condiciones de satisfacción, cumplido/no cumplido, causa, PPC/CNC), según lo describe `18-control-avance.md`.
- **Por qué se pospone:** el objetivo actual del flujo 18 es la cadena de datos RDT validado → PR → Dashboard (métricas EVM: EV, AC, SPI, CPI). El 3WLA no alimenta esa cadena — mide PPC (LPS), un indicador aparte que `18-control-avance.md` marca explícitamente que no debe mezclarse con SPI. No es indispensable para que el dato de RDT llegue al Dashboard.
- **Pospuesto:** 2026-09-20.

### Apartado "Inasistencias" al final del RDT

- **Origen:** pedido directo de Victor, 2026-09-20 (sesión de trabajo del sub-lote de RDT rechazo/historial).
- **Qué es:** un apartado nuevo al final del RDT (Crear RDTs), listado tipo desplegable con: personal (elegido del catálogo `recursos_personal`, igual que el Tareo), motivo de inasistencia, y lo que haga falta — diseño y campos exactos quedan a criterio de quien lo retome (Victor lo dejó abierto explícitamente).
- **Ojo — confirmar antes de construir:** Victor escribió "RDO", pero toda la sesión fue sobre **RDT** (Crear RDTs, PROM-GP-002) — "RDO" en este repo históricamente se refiere a otro formato distinto (reporte con fotos/personal de cantera, `Informacion para pruebas/RDO`). Antes de implementar, confirmar si es el RDT (más probable, por contexto) o si de verdad es el flujo RDO aparte.
- **Pospuesto:** 2026-09-20.

### Acceso directo a Postgres/Supabase para correr SQL

- **Origen:** decisión pendiente registrada el 2026-09-17 (antes en `docs/memoria-sesion.md`, ya retirado).
- **Qué es:** hoy Claude solo tiene las llaves REST de Supabase (leer/escribir filas de tablas existentes), no la cadena de conexión directa de Postgres — por eso Victor sigue pegando y corriendo el SQL él mismo en el SQL Editor de Supabase. Si se agrega la cadena de conexión directa (Project Settings → Database → Connection string, en `.env.local`), Claude podría correr migraciones (`CREATE TABLE`, etc.) directamente. Aun con esa llave, se confirma con Victor antes de correr cada migración — es un cambio difícil de deshacer.
- **Pospuesto:** 2026-09-20.
