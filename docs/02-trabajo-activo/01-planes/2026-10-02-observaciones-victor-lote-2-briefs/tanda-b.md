# Tanda B · Worker 2 — Importación de cronograma de punta a punta (O6)

Carril **2 · Cronograma** · rama `local-worker-2` en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-2` (fast-forward a `main` `ce5623e` hecho por el Orquestador; limpia) · puerto 3112. Lanzamiento: subagente «Worker 2 · tanda B».

Lee primero `00-contratos-comunes.md` y `00-indice-de-tandas.md`.

## Ítems de la tanda (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| B1 | **Reproduce el fallo** con `scripts/smoke-cronograma.mjs` (nuevo, fuera de `src/`) contra `npm run dev -- --webpack -p 3112`, con `soloAnalizar=true` (verifica el parámetro real en `api/cronograma/route.ts`) y **cada** archivo de prueba (`CRON-PROMCOSER-AESA-001.pdf`, `Cron-prueba N°01.xlsx`): registra el cuerpo HTTP y **el string exacto que vería Victor en pantalla** (cadena de `traducirErrorApi` sobre ese cuerpo, sin navegador). | Salida completa del script |
| B2 | **Aísla la causa raíz:** carga del XLSX real con `exceljs` → `parsearExcelCronograma(hoja)`; del PDF real con `PDFParse.getText()` → `parsearTextoPdfCronograma(texto)` (el camino que hoy solo se prueba con el fixture `.txt`); compara con los tests verdes actuales. Diagnóstico escrito: formato, fase y mensaje del fallo. | Diagnóstico + salida |
| B3 | **Corrige la causa raíz** en la ruta de importación (`api/cronograma/route.ts` y/o `lib/cronograma/*`). | Diff + tests |
| B4 | **Loguea en servidor todos** los caminos de fallo de la importación (hoy solo el `catch` de lectura, línea ~314) con formato, nombre del archivo y mensaje (`console.error` con contexto). | Salida del log en la prueba de fallo |
| B5 | **Mensaje específico en pantalla:** `src/lib/errores/traducir-error.ts` deja de devolver el fallback genérico para mensajes que ya traen motivo (quita el prefijo técnico `Error: …` y conserva el resto) y `FormularioCronograma.tsx` pasa su fallback real en las líneas ~133 y ~164 (hoy el `??` es código muerto). Prueba unitaria de `traducirErrorApi` (+test nuevo si no existe). | `npm test` + smoke de fallo mostrando el motivo |
| B6 | **Smoke de éxito de punta a punta** (análisis + guardado) con los dos archivos sobre **PS-0006** (verifica que no tenga Plan Maestro aprobado ni cronograma previo que bloquee la recarga; si lo tiene, **detente y devuelve la pregunta**), verificando el informe de extracción; y **smoke de fallo** (archivo inválido) con motivo específico y log en servidor. | Salidas de ambos smokes (contadores de actividades) |
| B7 | `npm test`, `npx tsc --noEmit`, `npm run lint` (sin deuda nueva), `npx next build --webpack` verdes en el carril. | Salida de comandos |

## Contexto verificado (no lo redescubras)

- O6 **reabre O4**: `9ad0640` solo añadió detección de formato por extensión, `console.error` y devolución del mensaje; **los parsers no cambiaron y el éxito end-to-end nunca se verificó**. Ese es exactamente lo que tu tanda cierra.
- Mecanismo que oculta el motivo en pantalla: `traducir-error.ts` devuelve el fallback genérico cuando el mensaje empieza con prefijo técnico (`identificador:` / `Error: …`), y el `?? 'No se pudo leer el cronograma'` de `FormularioCronograma.tsx` nunca llega a aplicarse.
- Si al diagnosticar aparece una causa distinta a la esperada, **corrige donde esté** (ruta de importación) sin tocar nada ajeno; si exige cambiar un contrato o archivo de otro carril, **detente y devuelve la pregunta**.

## Regla de negocio resuelta (RB4, Gate 1)

Si la importación falla, la pantalla muestra el **motivo específico** (sin mensaje genérico) y el error queda **logueado en servidor** con formato, nombre de archivo y mensaje. Evidencia obligatoria: **smoke real de éxito y de fallo** (lo que faltó en el Lote 1); sin ella la tanda no cierra.

## Qué leer

`AGENTS.md` y `CLAUDE.md` de la app (enteros); de este plan **solo** tus ítems B1–B7 por ID; flujo `04-flujos-de-negocio/15-cronograma.md` (regla de mensaje/log); `docs/03-aprendizaje-continuo/2026-10-01-clasificador-bloquea-scripts-de-migracion.md` solo si te deniega algo. **No leas** el plan completo, el brief A, la evidencia ni el progreso.

## Qué puedes y qué no

- **Puedes crear/editar:** los archivos dueño de tu fila en `00-indice-de-tandas.md`, más `scripts/smoke-cronograma.mjs` y scripts temporales **fuera** del repositorio.
- **No tocas:** `db/README.md`, ninguna migración, archivos del carril 1 (`page.tsx`, checklist, editor, catálogo), `permisos.ts`/`registro-accesos.ts` (si algo exige tocarlos: **detente y devuelve la pregunta**), flujos de negocio, estándar, plan, progreso o evidencia.
- Escribe en PS-0006 solo lo que el smoke necesite y **anota en tu resultado qué se importó** para que Victor lo revise.

## Skills

Al empezar: lista `.claude/skills/` de `pg_control_proyectos` y comprueba que la app no tiene carpeta de Skills; anota «Skills revisados» en tu resultado (`verificar-permisos-por-rol` **no aplica**: ningún cambio de permisos). Al terminar: **usa `cerrar-tanda`** (sus pasos 1, 3 y 4 van en `resultados/B.md`).

## Criterios de salida

B1–B7 `Conforme` con su evidencia; **ambos smokes reales** (éxito con contadores + fallo con motivo en pantalla y log); tests/tsc/lint/build verdes; `resultados/B.md` escrito con handoff, hallazgos de los cinco grupos y número de llamadas; commit (y push) en `local-worker-2`. Sin evidencia de smoke, la tanda no cierra.
