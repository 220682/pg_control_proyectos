# Brief — Tanda G: Informes, descargas Word, PDF y Excel

## Rol, modelo y tanda

Worker 1, Sonnet, esfuerzo medio. Tanda G, Ola 3, carril W1 (después de D; corre en paralelo con E, F y Q de W3). Subagente «Worker 1 · G». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **G1**: instalar `docx`; `exportar/word.ts`.
- **G2**: `exportar/pdf.ts` con `pdfkit` y `hoja.ts`; marca de agua «BORRADOR»; fotos 2/4/6 por página.
- **G3**: `exportar/excel.ts`: una hoja por tabla y hoja «Fotos» con miniatura, descripción y partida.
- **G4**: ruta `descargar` con `alcance` completo/resumen/fotos y `maxDuration`.
- **G5**: medición con 20 fotos (ms y memoria) en PDF, Word y Excel; resultado en el resumen.
- **G6**: pruebas: PDF leído con `pdf-parse`, `.docx` abierto como zip con la imagen incrustada, `.xlsx` releído con `exceljs`; los tres muestran los mismos datos que la vista previa.
- **G7**: descarga de `COSTOS` sin economía → 403 (por URL directa).

Punto de corte: G1–G3 / G4–G7.

## Rama, worktree y puerto

Rama `local-worker-1`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-1`, continuando tras D (verifica con `git log --oneline -5` que D está; si no, detente y avisa). Puerto 3011 si levantas la app. W3 (E, F, Q, L) parte de `local-worker-3` con `local-worker-1` incorporada al cerrar D: eso lo hace el Worker git antes; **tú no tocas `local-worker-3`**.

## Qué leer, y qué no

1. `src/lib/informes/tipos.ts` (**contrato congelado de B**: `Informe`, `Bloque`, `TipoBloque`, `FotoFija` con `datos` por id de bloque y `fotos` por id de bloque, `FotoCampo.rutaStorage`), `formatos.ts` (`esBloqueEconomico`), `periodo.ts` (`columnasDeTabla`, `tituloDelPeriodo`, `MAX_DIAS_COLUMNAS_POR_DIA`), `estados.ts`.
2. Lo de C y D: `congelar.ts`, `armar-datos-*.ts`, y la ruta `informes/[informeId]/` de D. **Contrato por confirmar al incorporar D:** nombre real de la forma de los datos por bloque, de la función que devuelve el informe armado (borrador = datos en vivo, emitido = `fotoFija`) y del helper de URL firmada de fotos.
3. `src/lib/pdf/hoja.ts` (`crearPdf`, `celda`, `texto`, `cabeceraFormato`, `MARGEN`, `ANCHO`; **no se edita**), `src/lib/pdf/parche-fuentes-pdfkit.ts`, `src/lib/rdts/exportador-pdf.ts` y `exportador-parte-pdf.ts` como patrón; para Excel, el patrón de `src/lib/dp/exportador-excel.ts` (usa `exceljs`).
4. `src/lib/permisos/permisos.ts`: `puedeDescargarInforme`, `puedeVerInformeCostos`. `next.config.ts` (solo lectura; ya tiene `serverExternalPackages` con `pdfkit`, `pdf-parse`).

**Verifica con `grep` los nombres reales** antes de usarlos. **No leas** el plan completo ni otros flujos. Maqueta no necesaria.

## Qué puede trabajar

Crear: `src/lib/informes/exportar/word.ts`, `pdf.ts`, `excel.ts` (y un `comun.ts` si hace falta), sus pruebas, y `src/app/api/proyectos/[id]/informes/[informeId]/descargar/route.ts` (+ prueba). Editar `package.json` y `package-lock.json` **solo** para agregar `docx` (G1; esos archivos son de W1).

**No toca:** `src/lib/informes/tipos.ts`, `src/lib/pdf/hoja.ts`, `db/**`, `db/095*` (sin seguimiento: no lo agregues a ningún commit), `permisos.ts` salvo que falte algo (entonces pregunta), `next.config.ts`, `src/lib/rdts/**`, `api/rdts/**`, componentes de pantalla, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica migraciones.**

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-1` (nunca a `main`) al cerrar G1–G3 y al cerrar G4–G7. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/G.md`. **Lee y usa la plantilla** `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` (cinco grupos de hallazgos) e incluye la medición de G5. No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- Ruta: `GET /api/proyectos/[id]/informes/[informeId]/descargar?formato=pdf|docx|xlsx&alcance=completo|resumen|fotos`. Quien puede ver ese informe; `COSTOS` sin economía = 403 aunque llegue por URL directa; un borrador lleva marca «BORRADOR»; un emitido se imprime desde `fotoFija`, nunca desde datos en vivo.
- `pdfkit` y `pdf-parse` ya están en `package.json` (`pdfkit ^0.19.1`, `exceljs ^4.4.0`); `docx` **no está**: se instala en G1.
- Fotos: bucket `documentos-proyecto`, ruta `informes/{proyectoId}/fotos/{uuid}.jpg` (`admin.storage`); JPEG ≤ 3 MB. Hay un `maxDuration` por confirmar contra el plan de Vercel (riesgo del plan): pon `export const maxDuration = 60` explícito en la ruta `descargar` (mismo valor que la tanda K), mide el tiempo de generación de cada formato con datos de prueba y anótalo. Patrón de `exceljs` en el repositorio: `src/lib/dp/exportador-excel.ts` y el de cronograma (no `rdts/exportar`, que el plan cita por error); verifica con `grep`.
- Los formatos no `COSTOS` no llevan dinero en ningún byte (R5); la prueba de C7 lo verifica en los datos, aquí repítelo sobre el archivo generado.
- Las migraciones 098 a 102 pueden no estar aplicadas (P33): pruebas con datos de ejemplo; anota «no probado en base».
- **Conflicto por avisar:** `exportar/` no existe en `src/lib/rdts/` aunque el plan lo cita como patrón; usa los exportadores de `rdts/` y `dp/` indicados.

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). G7 toca accesos: **aplica `verificar-permisos-por-rol`** (`.claude/skills/verificar-permisos-por-rol/SKILL.md`) con pruebas de ruta por rol; queda «Observado» para la tanda L. Comandos: `npm test` (si solo cambia por fin de línea el `.snap` de curva-s, restaurarlo con `git checkout`); `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar nuevos, anota el conteo); `npx next build --webpack`. `.env.local`: copiar el principal al worktree (autorizado siempre). Ningún Worker puede leer las cuentas de prueba (P36): lo que pida captura o sesión queda «Observado».

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**.

## Criterios de salida

G1–G7 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen con la medición de G5. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
