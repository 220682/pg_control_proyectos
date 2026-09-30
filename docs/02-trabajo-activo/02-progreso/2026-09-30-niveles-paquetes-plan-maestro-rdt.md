# Progreso — Niveles, Paquetes, Plan Maestro (lienzo) y RDT desde el Plan Maestro

## Referencia al plan

- Plan: `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt.md` (19 tandas, 109 ítems, 4 carriles).
- Encargos: `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/` (índice de tandas, reglas de contexto, contratos por carril, protocolo de migraciones, un brief por tanda, carpeta `resultados/`).
- Specs aprobados: `…/2026-09-30-niveles-presupuesto-y-cronograma.md`, `…/2026-09-30-paquetes-y-plan-maestro-grilla.md`, `…/2026-09-30-rdt-desde-plan-maestro.md`.
- Evidencia y auditoría: se crean cuando haya algo que registrar (`03-evidencia/` y `04-auditoria/`, mismo nombre de archivo).

## Estado general y fase actual

- Gate Spec: aprobado por Victor (2026-09-30), los tres Specs.
- Gate 1: aprobado por Victor (2026-09-30): plan, tabla de cambios a flujos en bloque, carpetas de trabajo, migraciones aplicadas por los Workers.
- Carpetas de trabajo creadas (2026-09-30, autorizadas por Victor). **La ola 1 todavía NO se lanzó.** El estado del plan sigue en «Planificando»; pasa a «Implementando» al lanzar la ola 1.

## Tabla de roles / Workers y estado

| Rol | Estado |
|---|---|
| Orquestador | Activo. Este chat llegó a ~564k de contexto; se recomienda traspaso a un chat nuevo antes de lanzar la ola 1. |
| Planner | Terminó el plan (y sus dos ajustes). No tiene más trabajo pendiente. |
| Workers | Ninguno lanzado. Ola 1: F0-A, F1-A, F2-A, F3-A. |
| Auditor | No asignado (va después de F5). |

## Skills revisados

Skills de `.claude/skills/` de `pg_control_proyectos`: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`. El repositorio de la app no tiene carpeta de Skills (comprobado). El Orquestador usó `seguir-flujo-de-planes` al pasar el Gate 1.

## Avances terminados

- Specs, plan, Punch List, briefs y contratos por carril; subidos a `main` de `pg_control_proyectos`.
- Política nueva aplicada al estándar: carpeta `04-auditoria`, revisión de Skills, resumen de cierre por tanda, flujo SDD con enlace al artefacto visual y primera lectura obligatoria en `AGENTS.md`, Skill `seguir-flujo-de-planes`.
- Protocolo de migraciones y credenciales escrito (`00-protocolo-migraciones.md`).
- Carpetas de trabajo de la app `local-worker-2`, `-3` y `-4` creadas desde `main`; `local-worker-1` ya existía. Las cuatro en `45c9e0a`, limpias, con `node_modules` enlazado al del repositorio principal y `.env.local` copiado (autorización permanente).

## Trabajo actual

Preparar el traspaso a un Orquestador con contexto limpio y lanzar la ola 1.

## Pendientes

1. **Lanzar la ola 1** (hasta 4 Workers a la vez): F0-A (maquetas de Niveles y Paquetes, trabaja en `pg_control_proyectos`, sin carpeta de la app), F1-A (carril 1, `local-worker-1`), F3-A (carril 2, `local-worker-2`), F2-A (carril 3, `local-worker-3`; escribe **y aplica** las migraciones 079–081: es la primera en el orden). Usar la «Plantilla del prompt de lanzamiento» del índice de tandas. Cada Worker usa `cerrar-tanda` y deja `resultados/<tanda>.md`.
2. **Reglas de permiso:** el sistema de permisos denegó al Planner tocar lo relacionado con credenciales; puede bloquear también a los Workers al aplicar migraciones. Victor pidió «ir viendo lo de las reglas». Revisar la configuración de permisos y proponerle reglas concretas **antes de la ola 2** (F1-B y F4-A aplican migraciones); no escribir reglas sin su aprobación.
3. Victor revisa las maquetas de F0-A antes de las tandas de interfaz de Niveles y Paquetes, y las de F0-B antes del lienzo y del selector del RDT.
4. Medir cada sesión de Worker con el script de `…-paneles-servicio-persistente-briefs/medicion.md` (meta: ≤ 80 llamadas, ≤ 200k de contexto).

## Commits, ramas y worktrees usados

- `pg_control_proyectos`: `main`, último commit de este trabajo `f90090d`, sincronizado con GitHub.
- `py_control_proyectos_web`: `main` = `45c9e0a`, igual a `origin/main`. Ramas y carpetas: `local-worker-1` a `local-worker-4` en `.worktrees/`, todas en `45c9e0a`. Turbopack no corre con el `node_modules` enlazado: usar `--webpack` (por eso el navegador va solo en F5).

## Hallazgos registrados en el momento

- PS-0006 ya no existe (eliminado en la limpieza del plan de paneles). Quedan PS-0004 y PS-0005; todos los servicios existentes son de prueba; F5-B crea un servicio de prueba dedicado.
- Credenciales: están en `C:\Users\BRANDY\Downloads\DIARIO\entorno_variable.txt` (nombres `PR_DB_URL` y `SUPABASE_ACCESS_TOKEN`). **No abrir ni mostrar ese archivo.** El `.env.local` de la app no las trae.
- El servidor de base de datos de Claude (`postgresql`) no conecta porque su ruta en la configuración de Victor no existe; el real está en `D:\VICTOR\CLAUDE CODE\mcp_postgresql`. No hace falta para este plan. Victor decide si se corrige.
- El artefacto «Flujo SDD a Cierre» está desactualizado (no incluye `04-auditoria` ni la revisión de Skills). Victor decide si se actualiza.
- Otra sesión dejó sin subir un cambio en `04-flujos-de-negocio/14-accesos-y-restricciones.md` (sincronización del artefacto de la matriz). No es de este plan: no tocarlo ni incluirlo en commits.
- `Trazabilidad.xlsx` (Victor lo edita) aparece modificado: no incluirlo en ningún commit.

## Bloqueos, riesgos y decisiones requeridas

- Riesgo: permisos para migraciones (ver pendiente 2).
- Abierto sin bloquear: nombre del rol extra cuando un archivo trae más de 5 niveles.
- La nota sobre el plan semanal (3WLA) en `planes-futuros.md` no se agregó; solo si Victor lo pide.

## Próximo paso verificable

Con contexto limpio: leer este archivo y el índice de tandas, lanzar la ola 1 y comprobar que cada Worker crea su `resultados/<tanda>.md`.

## Última actualización y responsable

2026-09-30, Orquestador.

## Handoffs

### Handoff del 2026-09-30 (Orquestador → Orquestador con contexto limpio)

- **Objetivo y estado:** ver «Estado general». Gate 1 cumplido; carpetas listas; ola 1 sin lanzar.
- **Qué leer, en este orden:** la sección «Flujo con Orquestador» de `AGENTS.md` (con su primera lectura obligatoria) y el Skill `seguir-flujo-de-planes`; este archivo; `…-briefs/00-indice-de-tandas.md`, `00-reglas-de-contexto.md` y `00-protocolo-migraciones.md`. **No** releer los 21 flujos ni los tres Specs completos: los Workers leen solo lo que su brief nombra.
- **Terminado y no terminado:** ver «Avances terminados» y «Pendientes».
- **Pruebas ejecutadas:** ninguna de código todavía (no hay Workers lanzados). Se verificó: sincronización de ambos repositorios, carpetas de trabajo limpias, tamaños de briefs ≤ 8 KB.
- **Cómo habla Victor y cómo hay que hablarle:** lenguaje simple, sin códigos internos de ítems ni siglas, una decisión por pregunta con recomendación; verificar antes de afirmar; no declarar cerrado nada sin la lista de verificación del Skill.
- **Límites:** el Orquestador no implementa, no hace merge ni push de la app sin autorización en el Gate 2, no edita `AGENTS.md` ni los flujos por su cuenta.
- **Próximo paso concreto:** lanzar F0-A, F1-A, F2-A y F3-A con la plantilla del índice.
