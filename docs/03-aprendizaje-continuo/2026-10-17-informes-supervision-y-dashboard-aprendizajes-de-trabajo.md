# Aprendizajes de trabajo del plan Informes de supervisión y Dashboard

## Origen

Plan [`2026-10-15-informes-supervision-y-dashboard.md`](../02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md) (19 tandas, tres Workers en worktrees de Windows), apartado «Mejoras (de trabajo)» y hallazgos de los resúmenes de cierre de las tandas A a S. Trasladado por el Documentador en la tanda M, 2026-10-17. Solo método y herramientas; ninguna regla del sistema (esas están en los flujos).

## Observación

Diez grupos de aprendizajes de método. Los marcados **candidata a Skill** ya se repitieron en este plan o en planes anteriores.

### 1. Editar archivos en Windows desde Bash: usar la herramienta de escritura, no heredocs (candidata a Skill)

Los heredocs de Bash con comillas, acentos o `\r`/`\n` fallaron con «unexpected EOF» o corrompieron el contenido en siete tandas distintas (B, D, E, I, N, Q, R); un `python -` con heredoc también cuelga esperando entrada. Con la herramienta Write (y, para scripts, un archivo `.py` aparte ejecutado con `python archivo.py`) no hubo un solo fallo. En un archivo con acentos, los reemplazos puntuales se hacen con un script que lee y escribe en UTF-8 conservando el fin de línea que ya tenía el archivo. Reincide la nota [`2026-10-01-editar-archivos-sin-heredocs-largos.md`](2026-10-01-editar-archivos-sin-heredocs-largos.md): se repite en este plan en siete tandas, así que conviene promoverla a un Skill de entorno.

### 2. `npm test` reescribe el snapshot de la Curva S solo por fin de línea (candidata a corregir de raíz)

Correr la suite modifica `src/app/api/curva-s/__snapshots__/curva-s-route.test.ts.snap` (solo cambian los saltos de línea). Pasó en las tandas H, P, R y S y los Workers lo restauraron con `git checkout` antes de commitear. Conviene fijar `.gitattributes` (o el modo de escritura del snapshot) en la app para que deje de pasar; mientras no, se restaura siempre antes de commitear.

### 3. `node_modules` en worktrees: el enlace compartido es frágil y quitarlo en Windows tiene truco

- Con `node_modules` como enlace y Turbopack, `npm run build` falla; la verificación de build se hace con `npx next build --webpack`.
- Un `node_modules` compartido por enlace se rompe para todos si otro worktree limpia o reinstala: el repositorio principal quedó a medias (50 entradas, sin `vitest`) y los worktrees que lo enlazaban quedaron sin poder probar. Cada worktree de trabajo usa su propio `node_modules` con `npm ci`.
- Para quitar el enlace en Windows, `cmd /c rmdir` desde Bash de Git no actúa (abre un cmd interactivo) y el `npm ci` siguiente corre a través del enlace (EPERM a medias). Se usa PowerShell (`cmd.exe /c "rmdir node_modules"`) y se comprueba que `LinkType` quede vacío antes de `npm ci`.

### 4. Antes de afirmar, buscar en la app el nombre visible y listar la carpeta completa (reincide «verificar antes de afirmar»)

- Se afirmó que no había un responsable por servicio mirando solo la semilla de una migración; el campo «Supervisor operativo a cargo» existía en la pantalla Editar servicio. Antes de proponer un campo, se busca la etiqueta visible del dato en la app.
- Un Planner dio una migración como libre mirando solo `git status`; ya estaba en `main`. Al buscar el siguiente número de migración se lista `db/` completo y se revisa `git log`.
- Una prueba usó una lista de «roles con economía» inventada en vez de leer `puedeVerEconomia`; se corrigió leyendo la fuente.
Ya es un principio del estándar; aquí queda como evidencia de reincidencia.

### 5. Respaldo de navegador cuando Playwright está ocupado

Si otra sesión tiene el navegador de Playwright, las capturas de una maqueta se pueden hacer con Chrome sin ventana: `chrome --headless=new --screenshot`. El marco compartido de maquetas acepta `window.MARCO_AJUSTE` (opcional) para proponer chips en una maqueta sin cambiar las demás.

### 6. Pruebas de módulos nuevos y de roles

- La prueba `modulos-huerfanos` exige que todo módulo nuevo de `src/lib` sea alcanzable; un cargador sin consumidor aún necesita al menos una prueba que lo importe.
- Un cliente de servicio falso en memoria (`fake-admin-test.ts`) permitió probar las 13 combinaciones de rol sin base de datos.
- Con las migraciones sin aplicar, la tabla de los 13 roles del Skill `verificar-permisos-por-rol` queda en pruebas de ruta y «Observado» hasta la verificación en vivo con suplantación de rol.
- Las pruebas de PDF con `pdf-parse` superan 5 s cuando corre toda la suite en paralelo; el bloque se fijó con timeout de 30 s.
- En vitest, `beforeEach(() => mock.mockClear())` devuelve la función y vitest la ejecuta como teardown; se escribe con llaves.
- Los archivos `db/*.sql` existentes mezclan LF y CRLF (la `102` quedó en CRLF); las pruebas que leen SQL normalizan `\r\n`.

### 7. Una sola fuente de datos para vista previa y archivos

Word, PDF y Excel de un informe salen de un único modelo de documento (`armarDocumento`); la vista previa del editor consume el mismo modelo para que «mismos datos» sea cierto por construcción y no por revisión.

### 8. Reglas de lint de React 19 que condicionan el diseño

La regla de hooks prohíbe mutar refs durante el render: el guardado automático del editor se arma desde los manejadores (cola de promesas) y no desde efectos. La regla `react-hooks/set-state-in-effect` falla con `setState` dentro de `useEffect`: se usa el patrón de ajustar el estado durante el render.

### 9. Librería de PDF

`pdfkit.dash(0, …)` lanza error; no se llama con longitud 0, y `dash` solo se usa cuando aplica.

### 10. Medir en el peor caso antes de aceptar un límite de plataforma

Con 20 fotos de 2,5 MB cada archivo de informe pesaba ~50 MB, por encima del límite de respuesta de una función de servidor (~4,5 MB, por confirmar). Se redujo cada foto al incrustarla y se volvió a medir con fotos de ruido (peor caso, 6 MB) y luego en vivo (~360 KB con 6 fotos). Medir primero con el caso más pesado y después con datos reales evita aceptar o descartar una solución con un número que no representa el uso.

## Evidencia

Apartado «Mejoras (de trabajo)» del plan (filas M1 a M19) y los resúmenes de cierre de las tandas A, B, C, D, E, F, G, H, I, J, K, N, O, P, Q, R, S y L en `02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/`.

## Clasificación

Mejora de trabajo (método y herramientas). Ninguna regla de negocio.

## Etiqueta de categoría

`herramientas/windows`, `worktrees/node_modules`, `tests`, `verificación`

## Destino propuesto

`docs/03-aprendizaje-continuo/` (este archivo). Candidatas a promoción: el punto 1 a un Skill de entorno Windows, el punto 2 a una corrección de la app (`.gitattributes`) y el punto 3 a `docs/01-contexto-repositorio/03-entorno-git-y-worktrees.md`; las decide el Auditor y Victor.

## Cambio propuesto

Ninguno por parte del Documentador: no se edita el estándar, `AGENTS.md` ni los Skills.

## Estado

`Pendiente`

## Referencia a la aprobación

Pendiente del Gate 2 del plan.
