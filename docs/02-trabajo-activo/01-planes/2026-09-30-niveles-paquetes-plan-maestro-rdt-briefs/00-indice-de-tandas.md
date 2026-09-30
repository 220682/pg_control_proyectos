# Índice de tandas, carriles y propiedad de archivos

Plan: `../2026-09-30-niveles-paquetes-plan-maestro-rdt.md`. Reglas: `00-reglas-de-contexto.md`. Contratos: `00-contratos-tecnicos.md`. Una tanda = un Worker = una sesión (~80 llamadas). **Máximo 4 Workers a la vez.**

## Carriles

| Carril | Rama / worktree (a autorizar) | Tandas | Dueño de |
|---|---|---|---|
| 1 · Niveles | `local-worker-1` (existe, limpio, en `main`) | F1-A · F1-B · F1-C | importación del DP y del cronograma, mapa de niveles, bloqueo de recarga |
| 2 · Plan Maestro | `local-worker-2` (nuevo) | F3-A · F3-B · F3-C · F3-D | lienzo, API del Plan Maestro, ocultar paneles |
| 3 · Paquetes | `local-worker-3` (nuevo) | F2-A · F2-B · F2-C | pantalla y API de Paquetes, vínculos |
| 4 · RDT | `local-worker-4` (nuevo) | F4-A · F4-B · F4-C | Crear RDT, consolidado, real por clave |
| Diseño (sin rama de la app) | trabaja en `pg_control_proyectos` | F0-A · F0-B | maquetas y `design.md` |
| Integración y cierre | rama del carril 1 | F5-A · F5-B · F5-C · F5-D | pruebas cruzadas, verificación en vivo, flujos |

## Grafo de dependencias

```text
F0-A ──(Victor aprueba maquetas Niveles y Paquetes)──► F1-C , F2-B
F0-B ──(Victor aprueba maquetas lienzo, paneles y selector RDT)──► F3-C , F3-D , F4-C
F1-A ─► F1-B ─► F1-C
F2-A ─► F2-B ─► F2-C
F3-A ─► F3-B ─► F3-C ─► F3-D
F4-A ─► F4-B ─► F4-C
Todas las tandas de F1..F4 ─► [merge ordenado por el Orquestador] ─► F5-A ─► [Victor aplica migraciones 073..084] ─► F5-B ─► F5-C
F5-D (documentación) corre en paralelo con F5-B y F5-C y necesita la tabla en bloque aprobada en el Gate 1
F5-* ─► Auditoría ─► Gate 2
```
Entre carriles **no hay espera de código**: cada uno construye contra `00-contratos-tecnicos.md` y datos simulados; lo real se une en F5-A. Esperan solo las maquetas (tandas de interfaz) y las migraciones aplicadas (F5-B en adelante).

## Olas (cuántas a la vez)

| Ola | Workers simultáneos (≤ 4) | Qué queda esperando |
|---|---|---|
| 1 | F0-A · F1-A · F2-A · F3-A | — |
| 2 | F0-B · F1-B · F3-B · F4-A | Victor revisa maquetas A (Niveles, Paquetes) |
| 3 | F1-C · F2-B · F3-C · F4-B | requieren maquetas A y B aprobadas |
| 4 | F2-C · F3-D · F4-C | — |
| 5 | F5-A | merges de los 4 carriles |
| 6 | F5-B, luego F5-C · F5-D en paralelo | migraciones aplicadas por Victor |

El Orquestador puede adelantar una tanda si hay un cupo libre y sus dependencias están cerradas. F3-C y F4-C no empiezan sin la maqueta del lienzo y del selector RDT aprobadas.

## Matriz de propiedad de archivos (app; un solo carril por archivo en cada fase)

| Carril | Archivos que le pertenecen (todo lo nuevo dentro de sus carpetas también) |
|---|---|
| 1 Niveles | `src/lib/niveles/**` (nuevo) · `src/lib/proyectos/bloqueo-recarga.ts` (nuevo) · `src/lib/dp/**` · `src/lib/cronograma/**` · `src/app/api/proyectos/[id]/dp/route.ts` · `src/app/api/cronograma/**` · `src/app/(workspace)/proyectos/[id]/dp/**` · `src/app/(workspace)/proyectos/[id]/pr/page.tsx` (solo la agrupación por niveles) · `src/app/(workspace)/cronograma/page.tsx` · `src/components/ui/FormularioCronograma.tsx` · `db/073`–`075` |
| 2 Plan Maestro | `src/lib/plan-maestro/**` · `src/app/api/plan-maestro/route.ts` · `src/app/(workspace)/plan-maestro/page.tsx` · `src/components/ui/FormularioPlanMaestro.tsx` y `src/components/plan-maestro/**` (nuevo) · `src/components/ui/WorkspaceShell.tsx` (ocultar paneles) y sus pruebas nuevas · `db/076`–`078` |
| 3 Paquetes | `src/lib/paquetes-trabajo/**` · `src/app/api/paquetes-trabajo/**` (incluye `vinculos/route.ts`, nuevo) · `src/app/(workspace)/paquetes-trabajo/page.tsx` · `src/components/ui/FormularioPaquetesTrabajo.tsx` y `src/components/paquetes/**` (nuevo) · `db/079`–`081` |
| 4 RDT | `src/app/api/rdts/**` · `src/lib/rdts/**` (incluye `real-por-clave.ts`, nuevo) · `src/components/ui/FormularioCrearRdt.tsx`, `TablaConsolidadoRdts.tsx`, `TablaStatusRdts.tsx`, `TablaListadoRdts.tsx` · `src/app/(workspace)/rdts/**` · `db/082`–`084` |
| **Congelados hasta F5-A** | `src/lib/permisos/**` (**única excepción:** el carril 2 añade en F3-B la función `puedeCrearVersionPlanMaestro` —administrador y jefe de proyectos— con su prueba para los 13 roles; nadie más edita ese archivo) · `src/lib/config/**` (registro de accesos, nav, panel-*, matriz-*) y sus `*.test.ts` · `db/README.md` · `package.json` y configuraciones · `src/lib/pr/**`, `src/lib/dashboard/**`, `src/lib/curva-s/**` · `db/053`, `061`, `062`, `070` |
| F5-A | todo lo congelado, más resolver conflictos de integración |
| F0 | `docs/05-diseno-y-referencias/**` (maquetas y `design.md`) |
| F5-D | `docs/04-flujos-de-negocio/**` · `AGENTS.md` si la tabla lo exige · artefacto «Matriz de permisos» |
| Orquestador | `docs/02-trabajo-activo/**` (plan, progreso, evidencia, auditoría, `resultados/`) |

Archivos **compartidos de hecho** y cómo se evita el choque: `api/cronograma/route.ts` y `FormularioCronograma.tsx` (carril 1 los retira del vínculo con metrado; carril 3 crea su propia API en `paquetes-trabajo/vinculos`); `rdts/catalogos` (carril 4) y `FormularioCrearRdt.tsx` (carril 4) consumen el mapa de niveles por el contrato `NodoEstructura`, no importan `src/lib/niveles/` hasta F5-A; `pr/page.tsx` y `dashboard/page.tsx` solo los lee el carril 2 en pruebas, no los edita.

## Migraciones reservadas (hoy la última es la `072`)

| Carril | Rango | Contenido previsto |
|---|---|---|
| 1 | 073–075 | niveles y encabezados por servicio y origen; `reemplazar_dp` (firma de 13 parámetros, como `db/071`) |
| 2 | 076–078 | relajar `unique (plan_maestro_id, wbs)` (autorización expresa); columnas de línea y copia del paquete |
| 3 | 079–081 | `paquete_trabajo_vinculos`; `orden` y `nivel` en `paquetes_trabajo` |
| 4 | 082–084 | `paquete_trabajo_id` en `rdt_actividades` y `rdt_actividad_partidas`; campos de derivadas (por confirmar) |
| F5 | 085–086 | reserva |

Ninguna depende de otra (las claves foráneas solo apuntan a tablas que ya existen). Se aplican **en orden numérico**, a mano por Victor, una por una con su confirmación. Nadie las aplica desde el código.

## Orden de integración (lo hace el Orquestador, nunca un Worker)

1. Al cerrar F1–F4, se crean los merges **en la rama del carril 1** (`local-worker-1`, rama de integración; no se crea una rama nueva): primero 3 (Paquetes), luego 2 (Plan Maestro), luego 4 (RDT). Por la matriz no se esperan conflictos; si aparece uno, se resuelve en F5-A con el dueño del archivo.
2. F5-A corre sobre esa rama: suite, `tsc`, lint contra `main`, build, pruebas cruzadas y `db/README.md`.
3. Victor aplica las migraciones 073–084 (checkpoint). Luego F5-B y F5-C.
4. El merge de esa rama a `main` ocurre **solo tras el Gate 2**, con el push de la app autorizado por Victor en ese momento.

## Plantilla del prompt de lanzamiento (el Orquestador la completa por tanda)

```text
Eres el Worker de la tanda <ID> del plan niveles-paquetes-plan-maestro-rdt. Lee, en este orden: 00-reglas-de-contexto.md y <ID>.md de
docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/. Carril <N>, rama <rama>, worktree <ruta>, puerto <p>.
<Si aplica: turno de navegador concedido / maqueta aprobada: <archivo>.>
Cierra escribiendo resultados/<ID>.md según las reglas. No leas otros briefs ni el plan completo.
```

## Lista de tandas

| Tanda | Carril | Ítems | Brief |
|---|---|---|---|
| F0-A | Diseño | 7 | `f0-tanda-a.md` |
| F0-B | Diseño | 7 | `f0-tanda-b.md` |
| F1-A | 1 | 6 | `f1-tanda-a.md` |
| F1-B | 1 | 6 | `f1-tanda-b.md` |
| F1-C | 1 | 5 | `f1-tanda-c.md` |
| F2-A | 3 | 6 | `f2-tanda-a.md` |
| F2-B | 3 | 6 | `f2-tanda-b.md` |
| F2-C | 3 | 5 | `f2-tanda-c.md` |
| F3-A | 2 | 7 | `f3-tanda-a.md` |
| F3-B | 2 | 6 | `f3-tanda-b.md` |
| F3-C | 2 | 6 | `f3-tanda-c.md` |
| F3-D | 2 | 5 | `f3-tanda-d.md` |
| F4-A | 4 | 5 | `f4-tanda-a.md` |
| F4-B | 4 | 5 | `f4-tanda-b.md` |
| F4-C | 4 | 5 | `f4-tanda-c.md` |
| F5-A | integración | 6 | `f5-tanda-a.md` |
| F5-B | integración | 5 | `f5-tanda-b.md` |
| F5-C | integración | 5 | `f5-tanda-c.md` |
| F5-D | documentación | 6 | `f5-tanda-d.md` |
