# Índice de tandas, carriles y propiedad de archivos

Plan: `../2026-09-30-niveles-paquetes-plan-maestro-rdt.md`. Reglas: `00-reglas-de-contexto.md`. Contratos: `00-contratos-tecnicos.md` (índice de los `contrato-c*.md`). Una tanda = un Worker = una sesión (~80 llamadas). **Máximo 4 Workers a la vez.**

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
Todas las tandas de F1..F4 (cada carril aplica y verifica sus migraciones) ─► [merge ordenado por el Orquestador] ─► F5-A ─► F5-B ─► F5-C
F5-D (documentación) corre en paralelo con F5-B y F5-C y necesita la tabla en bloque aprobada en el Gate 1
F5-* ─► Auditoría ─► Gate 2
```
Entre carriles **no hay espera de código** (cada uno construye contra sus `contrato-c*.md` y datos simulados; lo real se une en F5-A). Esperan solo las maquetas (tandas de interfaz) y las migraciones aplicadas (F5-B en adelante).

## Olas (cuántas a la vez)

| Ola | Workers simultáneos (≤ 4) | Qué queda esperando |
|---|---|---|
| 1 | F0-A · F1-A · F2-A · F3-A | — |
| 2 | F0-B · F1-B · F3-B · F4-A | Victor revisa maquetas A (Niveles, Paquetes) |
| 3 | F1-C · F2-B · F3-C · F4-B | requieren maquetas A y B aprobadas |
| 4 | F2-C · F3-D · F4-C | — |
| 5 | F5-A | merges de los 4 carriles |
| 6 | F5-B, luego F5-C · F5-D en paralelo | migraciones aplicadas por Victor |

El Orquestador puede adelantar una tanda si hay cupo y sus dependencias están cerradas.

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

Choques evitados: el carril 1 retira del cronograma el vínculo con metrado y el carril 3 crea su propia API (`paquetes-trabajo/vinculos`); los carriles 2 a 4 consumen los niveles por el contrato `NodoEstructura` y no importan `src/lib/niveles/` hasta F5-A; `dashboard/page.tsx` y `pr/page.tsx` (salvo la agrupación del carril 1) los lee el carril 2 solo en pruebas.

## Migraciones reservadas (hoy la última es la `072`)

Carril 1: **073–075** · carril 2: **076–078** · carril 3: **079–081** · carril 4: **082–084** · F5: 085–086 (reserva). Su contenido previsto está en el plan («Migraciones reservadas») y en el contrato de cada carril. Ninguna depende de otra (las claves foráneas solo apuntan a tablas que ya existen). Las **aplica el Worker de cada carril** al terminar su tanda, una a la vez, en este orden: Paquetes (079–081), RDT (082–084), Niveles (073–075) y Plan Maestro (076–078), con las credenciales y el candado que describe `00-protocolo-migraciones.md` (autorizado por Victor el 2026-09-30).

## Orden de integración (lo hace el Orquestador, nunca un Worker)

1. Al cerrar F1–F4, los merges se hacen **en la rama del carril 1** (`local-worker-1`; no se crea otra rama): primero 3 (Paquetes), luego 2 (Plan Maestro), luego 4 (RDT). No se esperan conflictos; si aparece uno, se resuelve en F5-A.
2. F5-A corre sobre esa rama: suite, `tsc`, lint contra `main`, build, pruebas cruzadas y `db/README.md`.
3. Las migraciones 073–084 ya están aplicadas y verificadas por sus carriles (constan en los `resultados/`); F5-A lo comprueba. Luego F5-B y F5-C.
4. El merge de esa rama a `main` ocurre **solo tras el Gate 2**, con el push de la app autorizado por Victor en ese momento.

## Plantilla del prompt de lanzamiento (el Orquestador la completa por tanda)

```text
Eres el Worker de la tanda <ID> del plan niveles-paquetes-plan-maestro-rdt. Lee, en este orden: 00-reglas-de-contexto.md y <ID>.md de
docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/. Carril <N>, rama <rama>, worktree <ruta>, puerto <p>.
<Si aplica: turno de navegador concedido / maqueta aprobada: <archivo>.>
Skills: lista .claude/skills/ de ambos repositorios y usa los que tu brief nombra (cerrar-tanda al final).
Cierra escribiendo resultados/<ID>.md según las reglas. No leas otros briefs ni el plan completo.
```

## Skills por tanda (flujo paso 8: el Orquestador los nombra aquí y en cada brief)

| Skill | Quién | Cuándo |
|---|---|---|
| `cerrar-tanda` | todo Worker | al final de **toda** tanda (los 19 briefs); adaptado: estados, evidencia y traspaso van en `resultados/<tanda>.md` |
| `verificar-permisos-por-rol` | Worker | F3-B (añade una función a `permisos.ts`), F5-A (edita `permisos.ts` y el registro de accesos) y F5-C (permisos por rol en vivo) |
| `seguir-flujo-de-planes` | Orquestador | al lanzar **cada ola** y antes de escribir el mensaje de cierre |
| Comprobación | Auditor | paso 12: verifica que se usaron los Skills citados, o por qué no |

Todo Worker lista `.claude/skills/` de ambos repositorios al empezar (el de la app hoy no tiene carpeta de Skills) y anota «Skills revisados» en su `resultados/<tanda>.md`. Ítems por tanda: Punch List del plan.
