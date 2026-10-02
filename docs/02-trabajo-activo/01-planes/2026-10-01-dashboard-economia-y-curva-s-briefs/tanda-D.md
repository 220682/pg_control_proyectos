# Brief — Tanda D (con Fase T) · Proyecto de prueba y verificación en vivo

## Rol, modelo y tanda

Worker 1 (código) · modelo **DeepSeek V4.1 Flash** (`opencode-go/deepseek-v4.1-flash`) · tanda **D**, carril único `local-worker-5`. «Worker 1 · D». Es la única tanda con **navegador** (Playwright). Incluye la **Fase T** (proyecto de prueba de extremo a extremo). Depende de A, B y C (hechas: commits `d40cd74`, `94a5f79`, `5e773c7`).

## Ítems de la tanda

**Fase T:** F12 (proyecto de prueba de extremo a extremo hasta ~50 % de avance, marcado y desactivable) y F13 (con ese proyecto se ve toda la estructura funcionando).
**Fase D:** F03, F04, F05, F06, F07, F09, F10, F11 (verificación en vivo con las dos caras), U02, U03, U04, U05, E01, E03, E04, V01, V04, R01, R02, R03, R05. Además, confirmar los dos matices que devolvió la tanda C: **(a)** el selector usa `aria-disabled` + `title` (accesible por teclado) en vez de `disabled`; **(b)** semántica de E01 (serie real vacía cuando todas las EV del rango son 0).

## Orden de trabajo (prioriza y reporta)

1. **Entorno:** en el worktree `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-5`, levantar `npm run dev -- --webpack -p 3115` (déjalo corriendo solo durante la verificación y deténlo al cerrar). `node_modules` es junction.
2. **Cuentas:** lee `C:\Users\BRANDY\.claude\projects\d--VICTOR-CLAUDE-CODE-pg-control-proyectos\memory\cuentas-prueba.md` con **Read** (nunca `grep`/`sed`/`cat`; no imprimas valores). Usa la cuenta A (rol con economía/administración) y, para la cara sin economía, la suplantación **«Ver como»** (`POST /api/ver-como`; cambia roles, no el alcance por OT). Al cerrar, restaura con `DELETE /api/ver-como`.
3. **Fase T:** crea (o reutiliza, si ya existe uno apto) un servicio/proyecto de prueba **marcado** (`PRUEBA-DASH-…`), desactivable, con: niveles del presupuesto/cronograma, Plan Maestro con asignaciones, partidas, HH/HM con costo y RDTs validados hasta ~50 % de avance. **No borres nada**; el borrado lo hace Victor. Si crear todo el proyecto excede tu presupuesto (~80 llamadas), haz lo máximo posible con datos marcados y **reporta exactamente qué falta**; usa los servicios existentes PS-0004/PS-0005 para lo que alcance.
4. **Verificación en vivo:** recorre los ítems de la Fase D que los datos permitan, con capturas (una por ítem) en `docs/02-trabajo-activo/03-evidencia/capturas/dashboard-economia-y-curva-s/` (créala). Verifica **las dos caras** (con y sin economía), móvil (390 px) y estados vacío/carga/error. Prueba el **403** forzando `GET /api/curva-s?modo=economica` con el rol sin economía (llamada directa) y que `modo=fisica` no exponga USD.
5. **Regresión:** `npm test`, `npx tsc --noEmit`, `npm run lint` (contra el baseline de `main`) y `npx next build --webpack`; comprueba que las pruebas del plan niveles siguen verdes (`integracion-permisos.test.ts`) y que el Dashboard del portafolio y el resto de economía no cambiaron.

## Qué leer, y qué no

1. Este brief y `00-reglas-de-contexto.md`.
2. App: `AGENTS.md` y `CLAUDE.md` (Next 16: consulta `node_modules/next/dist/docs/` con Grep si hace falta).
3. `docs/04-flujos-de-negocio/16-paneles.md` (patrón «ver no es acceder» y chips) y `11`, `21` solo para lo que verifiques.
4. `docs/05-diseno-y-referencias/design.md` solo las secciones que apliquen.
5. La memoria `cuentas-prueba.md` con Read cuando la necesites.
6. Del plan: solo ítems por Grep de su ID.

**No leer**: el plan completo ni el progreso/evidencia completos.

## Qué puede trabajar

Código: solo correcciones menores si la verificación destapa un fallo evidente, siempre en `local-worker-5` y con `git add` explícito. Datos: servicio/proyecto de prueba marcado (autorizado en el Gate 1). Capturas: en `03-evidencia/capturas/dashboard-economia-y-curva-s/`.
**No tocar**: `docs/04-flujos-de-negocio/**` (Fase E) · `db/**` (backend) · el motor (`evm.ts`, `dashboard.ts`, `curva-s.ts`) · `docs/02-trabajo-activo/**` salvo las capturas.

## Skills que debe usar

- `verificar-permisos-por-rol` (en vivo, con «Ver como»).
- `cerrar-tanda` al final.

## Límites y protocolo de navegador

- ~80 llamadas. **Un solo navegador**; no dos en paralelo. No tomes snapshot del login con el formulario relleno. Credenciales solo en el login (`browser_fill_form`/`browser_type`), nunca impresas ni copiadas. Una captura por ítem. Detén el servidor que iniciaste.
- Sin push ni merge. Commit solo en `local-worker-5`.

## Al terminar

Escribe `resultados/tanda-D.md` (estados de T y D, handoff ≤15 líneas, mejoras, reglas de negocio, huérfanos, llamadas) y devuélveme: ítems cerrados, pendientes con causa, preguntas, archivos tocados, comandos con resultado y llamadas.

## Criterios de salida

- Proyecto de prueba creado/marcado (o reporte exacto de lo que falta).
- Las dos caras verificadas con capturas; 403 del modo económico forzado confirmado; `modo=fisica` sin USD.
- Suite/`tsc`/lint/build verdes o explicados.
- `resultados/tanda-D.md` escrito.
