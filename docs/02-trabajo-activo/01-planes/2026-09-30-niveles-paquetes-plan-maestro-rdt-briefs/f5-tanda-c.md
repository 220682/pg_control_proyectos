# F5-C · Verificación en vivo: RDT, permisos por rol, móvil y regresión

Lee primero `00-reglas-de-contexto.md`. **Carril de integración** · rama `local-worker-1`, puerto 3111. Único carril con navegador.
Fase F5 · **Depende de:** F5-B cerrada (el servicio de prueba ya tiene DP, cronograma, paquetes y Plan Maestro aprobado).
**Punto de commit:** solo el `resultados/F5-C.md`, que lo commitea el Orquestador.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F5C-1 | **RDT desde el Plan Maestro**: Crear RDT lista los paquetes y partidas del Plan Maestro (no el DP); se crea un RDT que declara en una partida repartida y en un paquete «por avance del paquete»; se valida; el **real aparece en el lienzo** por paquete × partida (físico, EV y HH) y el **PR** muestra la partida una sola vez con la suma | Capturas + números del PR |
| F5C-2 | **Permisos por rol** con «Ver como» (`POST /api/ver-como`): los 13 roles ven y pueden exactamente lo que dicen las tablas 1 y 2 del flujo 14 en Cronograma, Paquetes, Plan Maestro y Crear RDT, incluida la **versión nueva** del Plan Maestro (administrador y jefe de proyectos); APIs sin efecto para las acciones (403 por rol = rechazado) | Tabla rol × pantalla + resultados de API. Usa el Skill `verificar-permisos-por-rol` |
| F5C-3 | **Móvil (390 px) y estados**: paso de niveles, Paquetes, lienzo y Crear RDT en vacío, carga y error; lienzo con scroll horizontal y columnas fijas; icono del asistente sin tapar columnas | Capturas |
| F5C-4 | **Regresión** en un servicio existente (PS-0004 o PS-0005): DP, PR, Dashboard y Curva S se ven igual que antes del plan; los filtros del Consolidado y Status de RDTs siguen funcionando | Comparación con la línea base medida al inicio de la tanda |
| F5C-5 | **Limpieza de datos de prueba** solo con autorización expresa de Victor (el Orquestador la confirma en el prompt): se eliminan el servicio de prueba y los registros marcados por id exacto, con SELECT previo y verificación posterior; evidencia de lo eliminado | Lista de ids + verificación |

## Contrato técnico verificado (2026-09-30)

- «Ver como» cambia los **roles**, no el alcance por OT (`proyecto_miembros`): distingue `No autorizado` (rol) de `No tienes esta OT a cargo` (alcance). `403 por rol = rechazado`; `404/400` = pasó la guardia de rol.
- Permisos (flujos 06, 14): crear RDT: administrador, jefe de proyectos, jefe de oficina técnica, supervisor operativo; validar o rechazar: administrador, jefe de proyectos, jefe de oficina técnica; rechazar un RDT ya validado: administrador y jefe de proyectos. Ver Plan Maestro: roles con economía y planner; Cronograma, Paquetes y RDTs: los 13 roles.
- Navegador, cuentas y capturas: igual que F5-B. Un solo `browser_evaluate` puede recorrer varias rutas o los 13 roles.
- Mide la línea base de F5C-4 **antes** de probar otra cosa, en el servicio existente, solo lectura.

## Qué NO hacer

- No escribas en servicios existentes. No elimines nada sin la autorización de F5C-5. No cambies permisos. Sin push.
- Ante lo que falle: déjalo `Observado` con el síntoma y sigue.

## Cierre

`resultados/F5-C.md` (estado de F5C-1 a F5C-5, evidencia, hallazgos, handoff, llamadas).
