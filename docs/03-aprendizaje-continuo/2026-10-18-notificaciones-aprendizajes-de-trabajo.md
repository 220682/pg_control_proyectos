# Aprendizajes de trabajo del plan Notificaciones y supervisor operativo (2026-10-18)

## Origen

Plan [`2026-10-16-notificaciones-estandar-y-supervisor-operativo.md`](../02-trabajo-activo/01-planes/2026-10-16-notificaciones-estandar-y-supervisor-operativo.md), apartado «Mejoras (de trabajo)» del libro de hallazgos, más las mejoras que los Workers dejaron en sus resúmenes de cierre (T1A, T1B, T1C, T2, T3, T4, T5, T6, T8A, T8B y T9). Trasladado en la tanda T8B. Solo método y herramientas; ninguna regla del sistema (las reglas de negocio fueron a los flujos 02, 03, 04, 05, 06, 07, 08, 12, 14 y 16).

## Observación

### 1. «Ver como» solo cambia la pantalla: para verificar avisos hay que entrar con la cuenta del rol

El «Ver como» no cambia la bandeja ni la campana: siguen siendo las del usuario real. Para comprobar qué recibe cada rol se inicia sesión con su cuenta de prueba, y cada aviso se verifica por los dos lados (quien ejecuta y quien no debería recibirlo). Contar siempre los avisos por **estado** y no por el filtro `?visto=false`, que devuelve solo los Pendiente: los «18 avisos» eran 17 pendientes y 1 revisado. La campana equivale a `GET /api/notificaciones/count` (solo Pendiente recibidos).

### 2. Cuentas de prueba: crear usuarios envía un correo y hay tope por hora

Crear un usuario envía un correo de invitación al correo indicado: usar solo buzones de Victor (alias con `+`). Para crear usuarios de prueba y asignarles OT sin pasar claves por el chat sirve `fetch` desde la sesión del administrador a `POST /api/admin/usuarios` y `PATCH /api/admin/usuarios/<id>` (`asignarProyectos`). El tope de invitaciones por hora de Supabase se agotó tras dos altas: espaciar las altas por horas.

### 3. Playwright: el login se rellena solo y los snapshots guardan la clave en texto

El formulario de login del navegador se rellena con la última cuenta usada y el snapshot guarda la clave en texto dentro de `.playwright-mcp/` del repositorio documental (carpeta sin seguimiento, publicada en GitHub si alguien hace `git add -A`). Antes de entrar con una cuenta, limpiar cookies y almacenamiento; la carpeta se excluyó de git en `.git/info/exclude` local. Cambiar de cuenta cuesta menos en **una sola llamada** `browser_run_code_unsafe` (limpiar cookies, login, leer la bandeja y capturar). Borrar los snapshots con claves es decisión de Victor.

### 4. Antes de afirmar «no hay choque» o fijar la base de una rama, comprobar contra `main` el mismo día

El «Sin choque hoy» del Spec se redactó por impresión y falló: el Planner lo corrigió con `git diff` entre ramas y al revisar se vio que `main` ya había avanzado. Usar `git branch --merged main`, `git diff --name-only main...<rama>` y el commit actual de `main`, el mismo día.

### 5. Pruebas de avisos: cobertura por texto y mocks parciales

* La prueba `cobertura-avisos.test.ts` obliga a registrar en `SITIOS` y en el catálogo cada llamada nueva a un creador de avisos: todo brief de código que toque avisos debe decirlo («si agregas o quitas una llamada a un creador de avisos, actualiza `SITIOS` y el catálogo»).
* Esa prueba busca el texto `avisar(` en todo `src/`: **no nombrar `avisar` a funciones locales** que no sean del catálogo (rompió con una función de `PerfilEntorno.tsx`).
* Un `vi.doMock` parcial de `permisos` rompe cualquier prueba cuya ruta pase a cargar `avisar` (cadena `grupo-proceso` → `registro-accesos`): partir del módulo real con `importActual`.
* Orden de despliegue: aplicar la migración 108 **antes** de desplegar; sin ella, `avisar` reintenta sin evento ni referencia (los avisos se crean igual) pero un aviso de «Entorno» falla.

### 6. Edición de archivos en Windows: heredocs, CRLF y rutas con `[id]` (reincide, candidata a Skill)

Los heredocs de Bash con comillas, barras invertidas o paréntesis fallan al analizarse o duplican/pierden las barras (T3, T4 y T8A; ya había pasado en los planes de Informes y Lote 4): escribir el script o el archivo con la herramienta de escritura y ejecutarlo. `sed` con saltos de línea sobre archivos CRLF y la herramienta de edición que exige leer antes de escribir enlentecen: ediciones de una línea y archivos nuevos con la herramienta de escritura. `git add` con rutas que contienen `[id]` falla o toma patrones: usar `GIT_LITERAL_PATHSPECS=1`.

### 7. Comitear solo los hunks propios en un archivo con cambios ajenos: aplicar las mismas sustituciones a la versión del índice

Tres técnicas funcionaron: (a) copia previa + `diff -u` + `git apply --cached` (T8A; sirve si los hunks propios y ajenos no se solapan ni comparten contexto); (b) `git diff -U0` + parche filtrado + `git apply --cached --unidiff-zero` (Lote 4); (c) **la más robusta y la usada en T8B**: un script que aplica la misma lista de sustituciones (texto antiguo, texto nuevo; cada ancla debe aparecer una sola vez) al archivo de trabajo **y** a `git show :archivo`, y escribe el resultado como objeto con `git hash-object -w` + `git update-index --cacheinfo`. No depende del contexto de líneas, y el índice queda con solo los cambios propios. Regla práctica: elegir anclas que existan idénticas en ambas versiones (fuera de las zonas con cambios ajenos). Verificar con `git diff --cached --stat` y que el `git diff` restante sea exactamente lo ajeno. La técnica se repitió en tres planes: candidata a Skill.

### 8. Sin navegador, la verificación visual queda diferida

Una tanda sin navegador (T1C, T9) deja la verificación en sintaxis, compilación y revisión de código: las capturas a 1440 y 390 px se hacen en la tanda de verificación en vivo antes de aprobar. Se queda como práctica ya recogida en el plan (T7).

## Evidencia

Hallazgos de origen en el libro del plan (M1 a M9 y los de los resúmenes T1A-H2, T1A-H4, T1B-H5, T1B-H6, T1C-H3, T2-H6, T2-H8, T3-H6, T4-H5, T5-H7, T6-H5, T6-H6, T8A-H8, T9-H3) y en [`resultados/T8B.md`](../02-trabajo-activo/01-planes/2026-10-16-notificaciones-estandar-y-supervisor-operativo-briefs/resultados/T8B.md).

## Clasificación

| # | Tipo | Destino propuesto |
|---|---|---|
| 1 | Técnica de verificación | Candidata a `01-contexto-repositorio/04-pruebas-y-evidencia.md` |
| 2 | Procedimiento de cuentas de prueba | Candidata a `01-contexto-repositorio/04-pruebas-y-evidencia.md` (protocolo de cuentas) |
| 3 | Seguridad de credenciales y técnica de Playwright | Candidata a `00-estandar-agentes/01-principios-y-seguridad.md` y a `04-pruebas-y-evidencia.md` |
| 4 | Reincidencia de «verificar antes de afirmar» | Ya está en `00-estandar-agentes/01-principios-y-seguridad.md`; queda como evidencia |
| 5 | Pruebas del repositorio de la app | Se queda como aprendizaje (briefs de código sobre avisos) |
| 6 | Entorno Windows | Reincidencia: candidata a Skill (ver los aprendizajes de Informes y Lote 4) |
| 7 | Técnica de Git | Reincidencia: candidata a Skill y a `01-contexto-repositorio/03-entorno-git-y-worktrees.md` |
| 8 | Método | Se queda como aprendizaje |

## Etiqueta de categoría

`verificación`, `seguridad`, `git`, `herramientas/windows`, `playwright`

## Estado

`Pendiente` de revisión del Auditor y de Victor (promoción a estándar o a Skill).
