# Mejora de trabajo — la política de red del entorno bloquea Supabase y con eso la autonomía real

> Origen: sesión `local_1.orquestador_cronograma-import-vinculo`, 2026-09-23. Registrado a pedido de Victor tras tener que correr él mismo una migración que el Worker no pudo aplicar.

## Qué pasó

El Worker completó la Tarea 2 (versatilidad partida↔tarea) y dejó la migración `db/071_cronograma_actividad_partidas_metrado.sql` lista, pero **sin aplicar** — no la corrió contra la base real. Al intentar reproducir el problema desde esta sesión (mismo entorno `vpc_local`), una conexión directa a Supabase fue rechazada por el proxy de salida: `connect_rejected (the egress proxy denied the CONNECT (organization policy))`.

**La política de red del entorno bloquea la salida a Supabase.** No es un problema de credenciales (las llaves están disponibles) ni de IPv6 (eso ya se había resuelto antes, ver `2026-09-21-acceso-postgres-sin-ipv6.md`) — es que el entorno, tal como está configurado hoy, no puede llegar a ese host en absoluto.

**Consecuencia más grave que la migración sola:** si el navegador tampoco puede llegar a Supabase, **la verificación en vivo con Playwright tampoco es posible** en este entorno — es decir, ningún Worker puede completar el paso de verificación que la política exige antes de dar algo por listo. Victor tuvo que correr la migración él mismo, a mano, en un horario en el que esperaba que el trabajo avanzara solo.

## Causa raíz

El entorno `vpc_local` no tiene el host de Supabase del proyecto en su lista de acceso de red permitido (o el nivel de acceso configurado es más restrictivo de lo necesario).

## Corrección pendiente (acción de Victor, no de un agente)

Ampliar el "Network access" del entorno `vpc_local` — menú del entorno en la barra de título de la sesión → Editar → Network access — para permitir la salida al host del proyecto de Supabase (`*.supabase.co`, o el específico del proyecto). Sin esto:

- Ningún Worker puede correr sus propias migraciones (tiene que quedar todo "listo pero sin aplicar", como pasó acá).
- Ningún Worker puede verificar en vivo con Playwright contra la app real — el requisito central de `docs/00-sistema/roles-y-flujo.md` § Worker queda estructuralmente imposible de cumplir en este entorno hasta que se arregle.
- La promesa de trabajo autónomo mientras Victor no está disponible (ej. durmiendo) no se puede cumplir — cualquier tarea que toque la base de datos o necesite verificación real termina esperándolo a él.

## Nota para el Worker/Orquestador mientras esto no se arregla

Si la migración o la verificación Playwright fallan por este bloqueo de red, **no es un bloqueo cualquiera** — es este problema conocido. Repórtalo así explícitamente (no como "no se pudo verificar" genérico) y remite a esta mejora, para que quede claro que la causa es de infraestructura del entorno, no del código ni del Worker.
