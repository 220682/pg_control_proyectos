# Índice de tandas — Lote 2 observaciones de Victor

| Tanda | Worker | Carril | Rama / worktree | Puerto | Archivos dueño | Estado |
|---|---|---|---|---|---|---|
| A (O5 + O7) | Worker 1 | 1 · Checklist | `local-worker-1` / `.worktrees/local-worker-1` | 3111 | `db/089_*`, `page.tsx`, `acciones-checklist.ts` (+test), `editor-checklist.tsx`, `confirmar-transicion/route.ts`, `documentos/[documentoId]/route.ts`, `checklist/route.ts` (solo si hace falta) | En curso |
| B (O6) | Worker 2 | 2 · Cronograma | `local-worker-2` / `.worktrees/local-worker-2` | 3112 | `api/cronograma/route.ts`, `lib/cronograma/*`, `lib/errores/traducir-error.ts` (+test), `FormularioCronograma.tsx`, `scripts/smoke-cronograma.mjs` | En curso |

- Briefs: `tanda-a.md`, `tanda-b.md` + `00-contratos-comunes.md`. Un Worker, una tanda, una sesión; no leas el brief de la otra tanda.
- **Prohibido para ambos:** `db/README.md` (integración C), `src/lib/checklist/checklist.ts`, flujos de negocio, estándar, `AGENTS.md`, el plan y este índice (los consulta el Orquestador). Sin permisos por rol nuevos: si tu parte exige tocar `permisos.ts` o `registro-accesos.ts`, **detente y devuelve la pregunta**.
- Meta: ~80 llamadas; a las ~60 cierras lo que tienes y escribes el handoff.
- Cierre en `resultados/A.md` / `resultados/B.md`; los commitea el Orquestador.
