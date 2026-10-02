# Contratos comunes a las dos tandas (Lote 2)

Lo leen los dos Workers. Datos verificados por el Orquestador (2026-10-02) y respuestas del Gate 1.

## Entorno

- App: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`. Tus comandos, **desde tu worktree**.
- Comandos (verificados en `package.json`): `npm test` (`vitest run`), `npm run lint` (`eslint`), `npx tsc --noEmit`, `npx next build --webpack`, dev `npm run dev -- --webpack -p <tu puerto>` (Node v24; `--env-file` disponible).
- Puertos: carril 1 (`local-worker-1`) = **3111**, carril 2 (`local-worker-2`) = **3112**. Detén solo el servidor que tú iniciaste.
- `.env.local` ya está en los dos worktrees (y copiarlo si faltara está autorizado): **nunca leas ni muestres sus valores**.
- Ambas ramas están en `ce5623e` (= `main`), limpias. Sin archivos compartidos entre carriles.

## Datos de prueba

- Proyecto de prueba (Gate 1, Q1): **`PS-0006` — «PRUEBA-F5B Servicio de verificacion»**.
- Cronograma: `docs/06-material-de-apoyo/Informacion para pruebas/CRON-PROMCOSER-AESA-001.pdf` y `Cron-prueba N°01.xlsx` (del repo de documentación `D:\VICTOR\CLAUDE CODE\pg_control_proyectos`).

## Credenciales y sesión para smokes (navegador NO)

- Cuentas: archivo `cuentas-prueba.md` en la memoria del proyecto (`C:\Users\BRANDY\.claude\projects\d--VICTOR-CLAUDE-CODE-pg-control-proyectos\memory\`). **Léelo con `Read` solo cuando lo necesites; prohibido `grep`/`sed`/`cat`, imprimir valores, o escribirlos en el repo, commits, resultados, capturas o chat.** Usa la cuenta A (administrador).
- Sesión sin navegador (patrón **por confirmar** contra el código antes de usarlo):
  1. `POST <NEXT_PUBLIC_SUPABASE_URL>/auth/v1/token?grant_type=password` con header `apikey: <NEXT_PUBLIC_SUPABASE_ANON_KEY>` y body `{"email":...,"password":...}` → JSON de sesión.
  2. Enviar esa sesión como cookie `sb-<project-ref>-auth-token` en cada llamada a `http://localhost:<puerto>/api/...`. **Verifica nombre y formato (¿base64 de JSON?) en `node_modules/@supabase/ssr`** (`parse`/`serialize`) antes de asumirlo.
  3. El servidor lo valida igual que el login normal (`src/middleware.ts`, `src/lib/auth/usuario-actual.ts`). Imprime solo estados y cuerpos de la app, nunca tokens ni contraseñas.
- Si ninguna vía de sesión funciona: **detente y devuelve la pregunta**; no inventes bypass de autenticación.

## Migración 089 (solo tanda A)

- Sigue `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/00-protocolo-migraciones.md` (autorizado por Victor): credenciales en `C:\Users\BRANDY\Downloads\DIARIO\entorno_variable.txt` (nombres `PR_DB_URL`/`SUPABASE_ACCESS_TOKEN`; **nunca abras ni imprimas el archivo**), script `migrar_tanda_A.py` con psycopg2 **fuera del repositorio**, transacción por archivo, conteos antes/después, borrado al terminar.
- Candado: archivo `resultados/CANDADO-MIGRACIONES.txt` **en esta carpeta** (misma regla: si existe, no aplicas y vuelves al final).
- Si el clasificador deniega el script: **no lo rodees**; déjalo listo, anota el comando exacto en tu resultado y detente.
- El mismo script (modo solo lectura, p. ej. `check`) sirve para la consulta A7.

## Al cerrar tu tanda

- Commit en **tu rama** con `git add` explícito (nunca `-A`/`.`), sin secretos, logs ni temporales; ~35% de avance, nunca a medias de un ítem. **Nunca a `main`; sin merge.** Push a tu rama al cerrar: permitido.
- Tu cierre va en `resultados/<tanda>.md` (A o B), plantilla `12-resumen-de-cierre-de-tanda.md`: estado de tus ítems con evidencia, handoff ≤15 líneas, hallazgos de los cinco grupos **en el momento**, número de llamadas. **No edites el plan, la evidencia, el progreso ni los flujos de negocio** — el Orquestador consolida.
- Pregunta de negocio o conflicto con un flujo → **detente y devuélvela al Orquestador en el momento** (con opciones y recomendación).
