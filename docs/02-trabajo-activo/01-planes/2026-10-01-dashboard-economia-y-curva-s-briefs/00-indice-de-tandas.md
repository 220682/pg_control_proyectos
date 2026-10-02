# Índice de tandas y carril

Plan: `../2026-10-01-dashboard-economia-y-curva-s.md`. Reglas: `00-reglas-de-contexto.md`. Una tanda = un Worker = una sesión (~80 llamadas). **Un solo Worker de código** (A→T→B→C→D), porque las fases tocan `permisos.ts`/`registro-accesos.ts`; el Documentador (E) y el Auditor trabajan en `pg_control_proyectos`.

## Carril

| Carril | Rama / worktree | Puerto | Tandas |
|---|---|---|---|
| Único (código) | `local-worker-5` · `.worktrees/local-worker-5` | 3115 | A · T · B · C · D |
| Documentación (sin worktree de la app) | `pg_control_proyectos` `main` | — | E |
| Auditoría (sin worktree) | `pg_control_proyectos` `main` | — | tras E |

## Grafo de dependencias

```text
A (permisos/accesos) ─► T (proyecto de prueba) ─► B (Dashboard) ─┐
                          └──────────────────────► C (Curva S) ──┴─► D (verificación en vivo) ─► E (documentación) ─► Auditoría ─► Gate 2
```

## Matriz de propiedad de archivos (app)

| Tanda | Archivos |
|---|---|
| A | `src/lib/permisos/permisos.ts` (+test) · `src/lib/config/registro-accesos.ts` (+test) · `src/lib/config/matriz-base-flujo14.ts` (+`matriz-accesos.test.ts`) · `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx` (gate de 13 roles y Parcial forzado) · `src/components/dashboard/ToggleTipoDashboard.tsx` (opción deshabilitada con `title`) |
| T | Datos de prueba en la base (proyecto nuevo hasta ~50 % de avance); sin código |
| B | `src/components/dashboard/**` (Bloque E, bloque «Costo real de recursos», ocultado PD5) · gate de dinero en `dashboard/page.tsx` · query de `pr_recursos` (+`descripcion`) |
| C | `src/components/curva-s/PantallaCurvaS.tsx`, `GraficoCurvaS.tsx` · `src/lib/curva-s/curva-s.ts` (+test) · `src/app/api/curva-s/route.ts` (+test) · `curva-s/page.tsx` |
| D | Verificación en vivo con Playwright; sin cambios de código salvo correcciones menores |
| E | `docs/04-flujos-de-negocio/11`, `14`, `16`, `21`; índice de planes; `planes-futuros.md`; traslado de hallazgos (Documentador) |
| **No tocar** | `docs/04-flujos-de-negocio/**` fuera de E · `db/**` (sin migraciones en este plan) · `evm.ts`, `dashboard.ts`, `curva-s.ts` (motor) y funciones SQL · `docs/02-trabajo-activo/**` (lo escribe el Orquestador) |

## Plantilla del prompt de lanzamiento (el Orquestador la completa por tanda)

```text
Eres el Worker de la tanda <ID> del plan dashboard-economia-y-curva-s. Lee, en este orden: 00-reglas-de-contexto.md y <ID>.md de
docs/02-trabajo-activo/01-planes/2026-10-01-dashboard-economia-y-curva-s-briefs/. Rama local-worker-5, worktree
D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-5, puerto 3115.
<Turno de navegador solo en D.>
Skills: lista .claude/skills/ de ambos repositorios y usa los que tu brief nombra (cerrar-tanda al final).
Cierra escribiendo resultados/<ID>.md según las reglas. No leas otros briefs ni el plan completo.
```

## Resultados

Los resúmenes de cierre viven en `...-dashboard-economia-y-curva-s-briefs/resultados/<tanda>.md` (los crea cada Worker; el Orquestador los consolida en el progreso/evidencia).
