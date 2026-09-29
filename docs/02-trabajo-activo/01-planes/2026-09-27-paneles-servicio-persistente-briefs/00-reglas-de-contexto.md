# Reglas de contexto para todo Worker de este plan

Vigentes desde 2026-09-29 (plan v8). Motivo: un Worker de fase entera con decenas de ítems no cabe en una sesión. En otro plan de Victor, los Workers de fase completa llegaron a 156–191 llamadas, 625–682k tokens de contexto y 83–97 millones de tokens leídos de caché; al repartir en tandas, el total bajó a unos 28M con contexto máximo de 186k. Este plan (181 ítems, 13 fases) se ejecuta con el mismo método. Ver `medicion.md`.

## Una tanda = un Worker = una sesión

- Cada fase se reparte en **tandas** (`f0-tanda-a.md`, `f2b-tanda-b.md`, etc.; el orden está en `00-indice-de-tandas.md`). Un Worker recibe **una sola tanda**, la termina y **cierra**. No continúa con la siguiente: el Orquestador lanza un Worker nuevo.
- **Meta: unas 80 llamadas a herramientas por tanda** (orientativa, no un muro). Al llegar a **~60** sin haber terminado, deja de abrir frentes nuevos, cierra lo que tiene y escribe el handoff con lo que falta. Si el ítem exige más, lo dice en el handoff y el Orquestador decide (tanda de continuación `<id>-2` o corrección); pasarse de la meta no es un fallo.
- Si la sesión se corta por límite de uso, el siguiente Worker retoma desde el handoff, no desde el plan.
- Una sola línea de trabajo a la vez: **un único worktree activo** (`local-worker-1`). Nada de ramas ni worktrees nuevos.

## Qué leer (y qué no)

1. Este archivo y **su brief** (único documento de tarea). No leas otros briefs.
2. Del repositorio de la app (`D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`): `AGENTS.md` (687 bytes) y `CLAUDE.md` (626 bytes), **enteros** (verificado el 2026-09-29: `AGENTS.md` solo contiene el bloque «This is NOT the Next.js you know» —Next 16, con cambios de API respecto de lo que conoces— y `CLAUDE.md` importa ese archivo y pide verificar contra el archivo o dato real antes de afirmar; **no existen** secciones «Code Shape Rules», «TypeScript style» ni «Testing»). Para Next 16 consulta la guía de `node_modules/next/dist/docs/` **con Grep del tema** (`searchParams` asíncronos, `useSearchParams` con `Suspense`, redirects), no entera.
3. Si la tanda toca interfaz: `docs/05-diseno-y-referencias/design.md` de `pg_control_proyectos` (31 KB) leyendo con `offset`/`limit` solo las secciones que el brief nombre (§3, §5, §9, §10, §12). Nunca entero.
4. Si el brief lo pide: las tablas 1 y 2 de `docs/04-flujos-de-negocio/14-accesos-y-restricciones.md` (19,7 KB; una vez) para las verificaciones de permisos. **No se copian** al plan, a los briefs ni a la evidencia: se leen del archivo.
5. Archivos de código con `offset`/`limit` o `Grep`; no releer un archivo ya leído salvo que haya cambiado.
6. Las tandas F7 (documentación en `pg_control_proyectos`) leen además, por Grep de sus títulos, `AGENTS.md` de `pg_control_proyectos` § «Políticas de coherencia y trazabilidad» y § «Límites y archivos prohibidos».

**No leer** el plan completo (221 KB), ni la evidencia ni el progreso completos. Si necesitas un dato del plan, **Grep por el ID** (`PL-123`, `C35`, `R28`, `A12`…) y lee solo esas líneas.

## Entorno

- Código: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-1`, rama `local-worker-1` (creada desde `main` `1942b01`). El `.env.local` **ya está copiado** (autorización permanente de Victor): **no lo leas ni muestres sus valores** y no preguntes por copiarlo. Cualquier otro archivo de entorno o de secretos se consulta antes.
- `node_modules` es una Junction al del repositorio principal: dev y build llevan `--webpack` (`docs/01-contexto-repositorio/03-entorno-git-y-worktrees.md` § Worktrees y bundler). Dev: `npm run dev -- --webpack -p <puerto libre>`. Build: `npx next build --webpack`.
- Comandos verificados en `package.json`: `npm test` (`vitest run`; entorno `node`, `include: src/**/*.test.ts`, sin pruebas de componentes), `npm run lint` (`eslint`), `npm run build` (`next build`, solo en el checkout principal). **Baseline de F0-A (LB-01):** el lint se compara contra el total medido en `main` (`1942b01`), no contra cero; `npm test` debe seguir verde.
- Sin migraciones ni cambios en `db/`. Las escrituras de Recursos usan `crearClienteAdmin()` tras la guardia de rol (patrón de `api/recursos/personal/route.ts`); no requieren migración.
- En Windows: verifica puertos y procesos con PowerShell nativo (`Get-NetTCPConnection`), detén solo el servidor que iniciaste al cerrar la tanda. Los logs (`*.log`) no se commitean ni se leen enteros (últimas 30 líneas).
- Navegador: herramientas `mcp__playwright__*` (si no están conectadas, `claude-in-chrome`; si tampoco, verifica con vitest y `fetch` y deja lo demás `Observado` con lista de comprobación manual).

## Cuentas de prueba

- Cuenta A (permisos altos) y cuenta B (sin permisos de administración): las credenciales viven **solo en la memoria del agente** (`cuentas-prueba.md`, carpeta `memory` del proyecto en `%USERPROFILE%\.claude\projects`), **nunca en el repositorio**, ni en la evidencia, el progreso, los commits, capturas o el chat. No las imprimas. **No hagas `grep`/`sed`/`cat` sobre ese archivo** (el 2026-09-27 una herramienta imprimió valores que no debían mostrarse): el Orquestador te pasa en el prompt de lanzamiento lo mínimo, o lees el archivo con `Read` y usas solo el valor necesario.
- El rol de la cuenta B se lee del pie del panel izquierdo de la propia interfaz (no de un archivo de credenciales).
- **Solo lectura sobre datos reales.** Ninguna verificación guarda, borra ni sube datos. Las acciones se prueban hasta abrir su formulario; los permisos de acciones, con (1) estado del botón o chip, (2) prueba unitaria de la función para los 13 roles y (3) llamada a la API sin efecto (id inexistente o cuerpo inválido: **403 por rol = rechazado**; 404 o 400 = pasó la guardia de rol). «Ver como» (`POST /api/ver-como` con `{"rol":"<rol>"}`, solo administrador real) cambia los roles pero **no** el alcance por OT (`proyecto_miembros`): distingue `No autorizado` (rol) de `No tienes esta OT a cargo` (alcance).
- **Duda abierta para Victor:** los ítems de Recursos (PL-158 a PL-172) piden «crea/edita/desactiva sin error», lo que exige escribir. Mientras el Orquestador no confirme una autorización de Victor para registros de prueba marcados, no se escribe: el camino feliz queda `Observado`.

## Capturas y navegador

- Verifica con el **snapshot de texto** (`browser_snapshot`), con `browser_evaluate` y con aserciones, no con imágenes. Un solo `browser_evaluate` puede recorrer varias rutas o los 13 roles.
- **Una captura por ítem como máximo** como evidencia para el Responsable humano, guardada en `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\02-trabajo-activo\03-evidencia\capturas\paneles-servicio-persistente\<PL-xxx>.jpg` (ancho ≤ 1440; JPEG o PNG reducido). La miras **como máximo una vez**; no se relee.
- Playwright: leer con `textContent()` (hay etiquetas con `uppercase`), esperar la condición real (URL, atributo) y no un tiempo fijo, y encadenar las navegaciones una a una sobre el mismo navegador (en paralelo se pisan). Tamaños: escritorio 1440 px y móvil 390 px.

## Cierre de tanda (obligatorio)

1. Estado de la Punch List de **sus** ítems actualizado solo en el archivo del plan, con `Grep` del ID + `Edit` de esa fila (columna Estado: `Conforme` / `Observado` / `No aplica`). No reescribir el plan.
2. Evidencia de cada ítem **añadida al final** de `docs/02-trabajo-activo/03-evidencia/2026-09-27-paneles-servicio-persistente.md` (append, sin releer el archivo).
3. **Handoff** de máx. 15 líneas al final de `docs/02-trabajo-activo/02-progreso/2026-09-27-paneles-servicio-persistente.md`: qué quedó `Conforme`, qué `Observado`, qué falta, comandos exactos para retomar, hallazgos, decisiones técnicas tomadas. Si esos dos archivos aún no existen, avisa al Orquestador y detente (los crea él desde las plantillas `03-progreso.md` y `04-evidencia.md`).
4. Commit en `local-worker-1` con `git add` explícito de los archivos tocados (nunca `-A` ni `.`), sin logs ni capturas pesadas ni archivos temporales de prueba. **Sin push ni merge** (la rama no tiene upstream). Las tandas F7 commitean en `main` de `pg_control_proyectos` solo con la autorización vigente de Victor que confirme el Orquestador.
5. Registra en el plan, en el momento, mejoras de trabajo, reglas de negocio acordadas y carpetas huérfanas (apartados obligatorios), sin releer el plan: haz `Grep` del título del apartado y `Edit`.
6. Último mensaje al Orquestador: ítems cerrados, ítems pendientes, preguntas devueltas y **número de llamadas** usadas.

## Cuándo detenerte y devolver una pregunta

Eres un subagente y no hablas con Victor. **Detente** y devuelve la pregunta al Orquestador (con opciones y tu recomendación) si aparece: una contradicción con un flujo escrito, un cambio de permisos que las tablas 1 y 2 del flujo 14 no decidan, una acción destructiva o irreversible, infraestructura no autorizada (ramas, worktrees, paquetes, push, otros archivos de entorno) o una duda de negocio. Antes de devolver, deja hecho el commit de lo ya terminado y avanza con lo que no dependa de la pregunta.

## Restricciones heredadas del plan

No cambia quién puede hacer qué salvo lo decidido por Victor y escrito en el flujo 14 (tablas 1 y 2) y en el plan; en lo demás solo cambia cómo se muestra. No modificar `src/lib/pr`, `dashboard`, `curva-s`, `plan-maestro` ni `dp` (en las páginas de PR, Dashboard del servicio y del portafolio, DP, Curva S, Plan Maestro y Registro de costos solo cambia la guardia). No restringir `GET /api/proyectos/[id]/partidas` (lo usa Crear RQ). No conectar el asistente (chat) a datos ni a ninguna API (flujo 17: no habilitado); «asistente» en los permisos es el **rol** de usuario. No editar ningún flujo de `04-flujos-de-negocio/` fuera de F7 ni sin la respuesta registrada de Victor a cada contradicción. Sin credenciales en repositorios. Reutilizar componentes existentes; `design.md` y `05-diseno-y-ui.md` mandan en interfaz.
